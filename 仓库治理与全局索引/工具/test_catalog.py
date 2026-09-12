"""Regression tests against disposable Git repositories; no app code is executed."""
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('catalog', Path(__file__).with_name('catalog.py'))
catalog = importlib.util.module_from_spec(spec)
spec.loader.exec_module(catalog)


class CatalogTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix='knowledge-catalog-')
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name).resolve()
        self.index = self.root / '仓库治理与全局索引/索引'
        self.index.mkdir(parents=True)
        self.git('init', '--quiet')
        self.git('config', 'core.autocrlf', 'false')
        self.write('.gitignore', '.env\n.env.*\n!.env.example\ncache/\n')
        self.write('notes/article.md', '# Article\n')
        self.write('notes/nested/new.md', '# New note\n')
        self.write('notes/assets/picture.txt', 'Attachment\n')
        self.write('notes/.env.example', 'KEY=\n')
        self.files = [{'id': 'article.stable', 'path': 'notes/article.md',
                       'oldPath': 'old/article.md'}]
        self.nodes = [{'id': 'topic.notes', 'path': 'notes', 'kind': 'topic'},
                      {'id': 'assets.stable', 'path': 'notes/assets',
                       'kind': 'topic', 'site': True}]
        self.mappings = [{'oldPath': 'old', 'targetPath': 'notes'},
                         {'oldPath': 'collection/first', 'targetPath': 'notes/article.md'},
                         {'oldPath': 'collection/second', 'targetPath': 'notes/nested/new.md'},
                         {'oldPath': 'collection/secret', 'targetPath': 'notes/.env'},
                         {'oldPath': 'collection/missing', 'targetPath': 'missing/file.md'}]
        self.save_indexes()
        self.git('add', '.')
        for name, value in [('ROOT', self.root), ('INDEX', self.index)]:
            context = patch.object(catalog, name, value)
            context.start()
            self.addCleanup(context.stop)

    def git(self, *args):
        return subprocess.run(['git', '-C', str(self.root), *args],
                              capture_output=True, check=True).stdout

    def write(self, path, content):
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding='utf-8')

    def save_indexes(self):
        for name, value in [('文件索引.json', {'files': self.files}),
                            ('目录索引.json', {'nodes': self.nodes}),
                            ('路径映射.json', {'mappings': self.mappings})]:
            (self.index / name).write_text(json.dumps(value), encoding='utf-8')

    def test_every_exported_file_and_directory_id_can_be_opened(self):
        data = catalog.export()
        failures = []
        for item in data['files'] + data['nodes']:
            try:
                result = catalog.resolve(item['id'])
            except KeyError:
                failures.append(item['path'])
            else:
                self.assertEqual(result['path'], item['path'])
        self.assertEqual(failures, [])
        self.assertEqual(catalog.resolve('old/article.md')['id'], 'article.stable')

    def test_aliases_reject_ignored_untracked_and_nonexistent_files(self):
        self.write('notes/.env', 'PLACEHOLDER=not-a-real-secret\n')
        self.write('notes/local.md', 'Untracked\n')
        for path in ['old/.env', 'notes/.env', 'old/local.md', 'old/absent.md',
                     'old/../outside', '../outside', 'B:/outside']:
            with self.subTest(path=path), self.assertRaises(KeyError):
                catalog.resolve(path)
        self.assertEqual(catalog.resolve('old/.env.example')['path'], 'notes/.env.example')

    def test_force_added_ignored_files_are_not_exported_or_resolved(self):
        self.write('notes/.env', 'PLACEHOLDER=\n')
        self.write('notes/cache/output.txt', 'Cache\n')
        self.git('add', '--force', 'notes/.env', 'notes/cache/output.txt')
        paths = {x['path'] for x in catalog.export()['files']}
        self.assertNotIn('notes/.env', paths)
        self.assertNotIn('notes/cache/output.txt', paths)
        with self.assertRaises(KeyError):
            catalog.resolve('old/cache/output.txt')

    def test_stale_saved_ids_do_not_bypass_live_file_filter(self):
        self.write('notes/.env', 'PLACEHOLDER=\n')
        self.files.append({'id': 'stale.secret', 'path': 'notes/.env', 'oldPath': 'old/.env'})
        self.save_indexes()
        for value in ['stale.secret', 'old/.env']:
            with self.subTest(value=value), self.assertRaises(KeyError):
                catalog.resolve(value)

    def test_missing_worktree_files_are_omitted_without_crashing_export(self):
        (self.root / 'notes/nested/new.md').unlink()
        paths = {x['path'] for x in catalog.export()['files']}
        self.assertNotIn('notes/nested/new.md', paths)
        with self.assertRaises(KeyError):
            catalog.resolve('old/nested/new.md')

    def test_collection_alias_lists_only_readable_targets(self):
        self.write('notes/.env', 'PLACEHOLDER=\n')
        self.assertEqual(catalog.resolve('collection')['targets'],
                         ['notes/article.md', 'notes/nested/new.md'])

    def test_assets_stay_out_of_main_graph_without_changing_ids(self):
        data = catalog.export()
        node = next(x for x in data['nodes'] if x['path'] == 'notes/assets')
        self.assertEqual(node['id'], 'assets.stable')
        self.assertEqual(node['kind'], 'asset')
        self.assertIs(node['site'], False)
        attachment = next(x for x in data['files'] if x['path'] == 'notes/assets/picture.txt')
        self.assertEqual(attachment['parentId'], 'assets.stable')
        self.assertIs(attachment['site'], False)

    def test_inherited_git_literal_path_setting_does_not_break_ignore_checks(self):
        with patch.dict(os.environ, {'GIT_LITERAL_PATHSPECS': '1'}):
            paths = {x['path'] for x in catalog.export()['files']}
            self.assertIn('notes/article.md', paths)


if __name__ == '__main__':
    unittest.main()
