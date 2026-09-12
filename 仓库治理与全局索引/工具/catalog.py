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
from pathlib import Path
import subprocess
import sys
import uuid

ROOT = Path(__file__).resolve().parents[2]
INDEX = ROOT / '仓库治理与全局索引/索引'


def read(name):
    return json.loads((INDEX / name).read_text(encoding='utf-8'))


def tracked():
    data = subprocess.run(['git', '-C', str(ROOT), 'ls-files', '-z'],
                          capture_output=True, check=True).stdout
    return [p.decode('utf-8') for p in data.split(b'\0') if p]


def resolve(value):
    """Exact immutable content IDs first, then longest old-path prefix."""
    value = value.replace('\\', '/').removeprefix('./').rstrip('/')
    if value.startswith('/') or '..' in value.split('/') or ':' in value or '\0' in value:
        raise KeyError(value)
    files = read('文件索引.json')['files']
    for item in files:
        if value in (item['id'], item['oldPath'], item['path']):
            return {'id': item['id'], 'path': item['path'], 'oldPath': item['oldPath']}
    nodes = read('目录索引.json')['nodes']
    for item in nodes:
        if value in (item['id'], item['path']):
            return item
    for item in sorted(read('路径映射.json')['mappings'], key=lambda m: -len(m['oldPath'])):
        old = item['oldPath']
        if value == old or value.startswith(old + '/'):
            path = item['targetPath'] + value[len(old):]
            return {'path': path, 'oldPath': value}
    # Old aggregate directories have several destinations, not a guessed single ID.
    children = sorted({item['targetPath'] for item in read('路径映射.json')['mappings']
                       if item['oldPath'].startswith(value + '/')})
    if children:
        return {'oldPath': value, 'targets': children}
    raise KeyError(value)


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


def export():
    """Live inventory; migrated IDs persist, new fallback IDs must be stored on import."""
    saved = {item['path']: item for item in read('文件索引.json')['files']}
    nodes = read('目录索引.json')['nodes']
    by_path = {n['path']: n for n in nodes}
    paths = tracked()
    for path in paths:
        parent = path.rpartition('/')[0]
        while parent:
            if parent not in by_path:
                by_path[parent] = {'id': 'node.' + uuid.uuid5(uuid.NAMESPACE_URL,
                    'knowledge-directory:' + parent).hex, 'path': parent,
                    'title': parent.rsplit('/', 1)[-1], 'kind': 'topic', 'site': False}
            parent = parent.rpartition('/')[0]
    for path, node in by_path.items():
        parent = path.rpartition('/')[0]
        node['parentId'] = by_path[parent]['id'] if parent else None
    result = []
    for path in paths:
        old = saved.get(path)
        parent = path.rpartition('/')[0]
        result.append({'id': old['id'] if old else 'content.' + uuid.uuid5(
            uuid.NAMESPACE_URL, 'knowledge-repository:' + path).hex,
            'path': path, 'oldPath': old['oldPath'] if old else None,
            'parentId': by_path[parent]['id'] if parent else None,
            'size': (ROOT / path).stat().st_size})
    return {'schemaVersion': 1, 'nodes': list(by_path.values()), 'files': result}


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
