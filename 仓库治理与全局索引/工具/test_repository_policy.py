"""Exercise the actual ignore rules and commit guard in disposable repositories."""
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
GUARD = ROOT / '仓库治理与全局索引/工具/check_staged_files.py'


class RepositoryPolicyTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory(prefix='knowledge-policy-')
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        self.git('init', '--quiet')
        self.git('config', 'core.autocrlf', 'false')
        (self.root / '.gitignore').write_bytes((ROOT / '.gitignore').read_bytes())

    def git(self, *args):
        return subprocess.run(['git', '-C', str(self.root), *args], capture_output=True, check=True)

    def test_dependencies_credentials_and_runtime_state_are_ignored(self):
        paths = ['app/node_modules/a.js', 'app/.venv/pyvenv.cfg', 'app/oh_modules/a.ets',
                 'app/.env', 'app/.env.production', 'app/local.properties',
                 'app/db.sqlite3', 'app/user_data/email_tasks.db',
                 'app/user_data/chrome_data/content_data.json', 'app/dump.rdb',
                 'app/lib/dependency.jar', 'app/lib/native.dll', 'app/weights/model.pt',
                 'app/.ipynb_checkpoints/note.ipynb', 'app/.claude/settings.local.json']
        for path in paths:
            with self.subTest(path=path):
                result = subprocess.run(['git', '-C', str(self.root), 'check-ignore', '--quiet', '--', path])
                self.assertEqual(result.returncode, 0)

    def test_knowledge_sources_lockfiles_templates_and_wrappers_are_allowed(self):
        paths = ['notes/研究.md', 'notes/assets/cat.jpg', 'notes/课程.zip',
                 'notes/data/table.hdf5', 'notes/data/example.bin', 'app/.env.example',
                 'app/uv.lock', 'app/package-lock.json', 'app/oh-package-lock.json5',
                 'app/.mvn/wrapper/maven-wrapper.jar', 'app/gradle/wrapper/gradle-wrapper.jar',
                 'app/fixtures/db.sqlite3', 'app/.claude/skills/demo/SKILL.md',
                 'app/CLAUDE.md', 'app/AGENTS.md', 'app/settings.json',
                 'app/VMware 25汉化问题/zh_CN/vmui-zh_CN.dll']
        for path in paths:
            with self.subTest(path=path):
                result = subprocess.run(['git', '-C', str(self.root), 'check-ignore', '--quiet', '--', path])
                self.assertEqual(result.returncode, 1)

    def test_guard_rejects_force_added_ignored_dependency(self):
        target = self.root / 'node_modules/dependency.js'
        target.parent.mkdir()
        target.write_text('example', encoding='utf-8')
        self.git('add', '--force', '--', 'node_modules/dependency.js')
        result = subprocess.run(['python', '-X', 'utf8', str(GUARD)], cwd=self.root, capture_output=True)
        self.assertEqual(result.returncode, 1)

    def test_guard_rejects_oversized_lfs_payload_and_accepts_small_files(self):
        (self.root / 'article.md').write_text('# Article\n', encoding='utf-8')
        self.git('add', '--', 'article.md')
        result = subprocess.run(['python', '-X', 'utf8', str(GUARD)], cwd=self.root, capture_output=True)
        self.assertEqual(result.returncode, 0)
        (self.root / 'large.pointer').write_text('version https://git-lfs.github.com/spec/v1\n'
            + 'oid sha256:' + 'a' * 64 + '\nsize 100000001\n', encoding='utf-8')
        self.git('add', '--', 'large.pointer')
        result = subprocess.run(['python', '-X', 'utf8', str(GUARD)], cwd=self.root, capture_output=True)
        self.assertEqual(result.returncode, 1)


if __name__ == '__main__':
    unittest.main()
