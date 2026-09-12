"""Read-only catalog adapter for the knowledge backend (Python standard library).

Examples:
  python -X utf8 仓库治理与全局索引/工具/catalog.py --verify
  python -X utf8 仓库治理与全局索引/工具/catalog.py --resolve "工具链研究和记录/ComfyUI/ComfyUI学习.md"
  python -X utf8 仓库治理与全局索引/工具/catalog.py --export

--export returns current Git-tracked paths; ignored dependencies are never crawled.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import subprocess
import sys
import uuid

ROOT = Path(__file__).resolve().parents[2]
INDEX = ROOT / '仓库治理与全局索引/索引'


def read(name):
    return json.loads((INDEX / name).read_text(encoding='utf-8'))


def tracked():
    """Only existing regular files admitted by Git and the read policy."""
    data = subprocess.run(['git', '-C', str(ROOT), 'ls-files', '--stage', '-z'],
                          capture_output=True, check=True).stdout
    candidates = []
    for entry in data.split(b'\0'):
        if not entry:
            continue
        metadata, path = entry.split(b'\t', 1)
        mode, _, stage = metadata.split()
        if stage != b'0':
            raise ValueError('Resolve Git conflicts before reading the catalog')
        if mode in (b'100644', b'100755'):
            candidates.append(path.decode('utf-8'))
    if not candidates:
        return []
    # --no-index applies ignore rules even to files previously added with -f.
    # check-ignore accepts literal stdin paths but rejects Git pathspec magic,
    # including GIT_LITERAL_PATHSPECS inherited from migration tooling.
    ignore_env = {key: value for key, value in os.environ.items() if key not in {
        'GIT_LITERAL_PATHSPECS', 'GIT_GLOB_PATHSPECS',
        'GIT_NOGLOB_PATHSPECS', 'GIT_ICASE_PATHSPECS'}}
    ignored = subprocess.run(
        ['git', '-C', str(ROOT), 'check-ignore', '--no-index', '-z', '--stdin'],
        input=b'\0'.join(p.encode('utf-8') for p in candidates) + b'\0',
        capture_output=True, env=ignore_env)
    if ignored.returncode not in (0, 1):
        raise RuntimeError('Cannot determine Git ignore rules')
    excluded = {p.decode('utf-8') for p in ignored.stdout.split(b'\0') if p}
    return [p for p in candidates if p not in excluded and safe_file(p)]


def safe_file(path):
    """Do not follow symlinks or Windows junctions, including in parent folders."""
    parts = PurePosixPath(path).parts
    if not parts or path.startswith('/') or '..' in parts or ':' in path or '\0' in path:
        return False
    name = parts[-1].casefold()
    if (name == '.env' or name.startswith('.env.')) and name not in {
            '.env.example', '.env.sample', '.env.template'}:
        return False
    current = ROOT
    try:
        for part in parts:
            current = current / part
            if current.is_symlink() or current.is_junction():
                return False
        return (current.resolve().is_relative_to(ROOT) and current.is_file()
                and current.stat().st_size <= 100_000_000)
    except (OSError, RuntimeError):
        return False


def resolve(value):
    """Resolve against a fresh readable inventory; never concatenate an unchecked path."""
    return Catalog().resolve(value)


def verify():
    tracked_paths = set(tracked())
    items = read('文件索引.json')['files']
    errors, ids = [], set()
    raw = subprocess.run(['git', '-C', str(ROOT), 'ls-files', '--stage', '-z'],
                         capture_output=True, check=True).stdout
    blobs = {entry.split(b'\t', 1)[1].decode('utf-8'): entry.split()[1].decode('ascii')
             for entry in raw.split(b'\0') if entry}
    dirty_raw = subprocess.run(['git', '-C', str(ROOT), 'diff', '--name-only', '-z'],
                               capture_output=True, check=True).stdout
    dirty = {p.decode('utf-8') for p in dirty_raw.split(b'\0') if p}
    for item in items:
        p = (ROOT / item['path']).resolve()
        if not p.is_relative_to(ROOT) or not p.is_file():
            errors.append('Missing or invalid path: ' + item['path'])
            continue
        if item['id'] in ids:
            errors.append('Duplicate ID: ' + item['id'])
        ids.add(item['id'])
        if item['path'] not in tracked_paths:
            errors.append('Not tracked: ' + item['path'])
        with p.open('rb') as f:
            digest = hashlib.file_digest(f, 'sha256').hexdigest()
        # Git blob identity is portable across CRLF/LF checkouts. Raw SHA256 is
        # retained as evidence of the original local migration, not a URL key.
        if 'gitBlob' in item:
            changed = blobs.get(item['path']) != item['gitBlob'] or item['path'] in dirty
        else:
            changed = digest != item['sha256'] or p.stat().st_size != item['size']
        if changed:
            errors.append('Snapshot changed; update catalog: ' + item['path'])
    for node in read('目录索引.json')['nodes']:
        if node['id'] in ids:
            errors.append('Duplicate node ID: ' + node['id'])
        ids.add(node['id'])
        if not (ROOT / node['path']).is_dir():
            errors.append('Missing node: ' + node['path'])
    print(json.dumps({'filesVerified': len(items), 'errors': errors}, ensure_ascii=False))
    return bool(errors)


def build_inventory():
    """Live inventory; migrated IDs persist, new fallback IDs must be stored on import."""
    saved = {item['path']: item for item in read('文件索引.json')['files']}
    nodes = read('目录索引.json')['nodes']
    curated = {n['path']: n for n in nodes}
    by_path = {}
    paths = tracked()
    for path in paths:
        parent = path.rpartition('/')[0]
        while parent:
            if parent not in by_path:
                by_path[parent] = dict(curated[parent]) if parent in curated else {
                    'id': 'node.' + uuid.uuid5(uuid.NAMESPACE_URL,
                    'knowledge-directory:' + parent).hex, 'path': parent,
                    'title': parent.rsplit('/', 1)[-1], 'kind': 'topic', 'site': False}
            parent = parent.rpartition('/')[0]
    for path, node in by_path.items():
        parent = path.rpartition('/')[0]
        node['parentId'] = by_path[parent]['id'] if parent else None
        if 'assets' in path.split('/'):
            node.update(kind='asset', site=False)
    result = []
    for path in paths:
        old = saved.get(path)
        parent = path.rpartition('/')[0]
        item = {'id': old['id'] if old else 'content.' + uuid.uuid5(
            uuid.NAMESPACE_URL, 'knowledge-repository:' + path).hex,
            'path': path, 'oldPath': old['oldPath'] if old else None,
            'parentId': by_path[parent]['id'] if parent else None,
            'size': (ROOT / path).stat().st_size}
        if 'assets' in path.split('/')[:-1]:
            item.update(kind='asset', site=False)
        result.append(item)
    return {'schemaVersion': 1, 'nodes': list(by_path.values()), 'files': result}


class Catalog:
    """One sync snapshot, shared by export and O(1) ID/path lookups.

    Create a new instance after Git or worktree changes. The website must perform
    content parsing and safe file opening itself; this adapter returns metadata.
    """

    def __init__(self):
        self.data = build_inventory()
        self.by_id = {}
        self.by_path = {}
        self.by_old_path = {}
        for item in self.data['nodes'] + self.data['files']:
            if item['id'] in self.by_id:
                raise ValueError('Duplicate catalog ID: ' + item['id'])
            self.by_id[item['id']] = item
            self.by_path[item['path']] = item
            if item.get('oldPath'):
                self.by_old_path[item['oldPath']] = item
        self.mappings = sorted(read('路径映射.json')['mappings'],
                               key=lambda m: -len(m['oldPath']))

    def resolve(self, value):
        value = value.replace('\\', '/').removeprefix('./').rstrip('/')
        if not value or value.startswith('/') or '..' in value.split('/') or ':' in value or '\0' in value:
            raise KeyError(value)
        value = str(PurePosixPath(value))
        for index in (self.by_id, self.by_path, self.by_old_path):
            if value in index:
                return dict(index[value])
        for item in self.mappings:
            old = item['oldPath']
            if value == old or value.startswith(old + '/'):
                target = item['targetPath'] + value[len(old):]
                if target in self.by_path:
                    return dict(self.by_path[target], oldPath=value)
                raise KeyError(value)
        targets = sorted({item['targetPath'] for item in self.mappings
                          if item['oldPath'].startswith(value + '/')
                          and item['targetPath'] in self.by_path})
        if targets:
            return {'oldPath': value, 'targets': targets}
        raise KeyError(value)


def export():
    return Catalog().data


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--verify', action='store_true')
    group.add_argument('--resolve')
    group.add_argument('--export', action='store_true')
    args = parser.parse_args()
    if args.verify:
        return verify()
    try:
        result = resolve(args.resolve) if args.resolve else export()
    except KeyError:
        print('Content or path not found', file=sys.stderr)
        return 1
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    sys.exit(main())
