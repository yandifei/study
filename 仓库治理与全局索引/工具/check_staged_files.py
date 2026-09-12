"""Check the complete Git index, including LFS payload sizes, before a commit.

Run with Python 3 from any directory inside the repository. No dependencies.
The conservative limit is 100,000,000 bytes (100 MB, smaller than 100 MiB).
"""
import os
import re
import subprocess
import sys

LIMIT = 100_000_000


def git(*args, data=None):
    return subprocess.run(["git", *args], input=data, stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE, check=True).stdout


def check():
    entries = []
    errors = []
    for record in git("ls-files", "--stage", "-z").split(b"\0"):
        if not record:
            continue
        meta, raw_path = record.split(b"\t", 1)
        mode, oid, stage = meta.split()
        path = os.fsdecode(raw_path)
        if stage != b"0":
            errors.append(f"unmerged entry: {path}")
        if mode != b"160000":
            entries.append((oid, path))
        name = path.rsplit("/", 1)[-1]
        if (name == ".env" or name.startswith(".env.")) and name not in {
                ".env.example", ".env.sample", ".env.template"}:
            errors.append(f"local environment file: {path}")
    oids = sorted({oid for oid, _ in entries})
    sizes = {}
    if oids:
        output = git("cat-file", "--batch-check=%(objectname) %(objectsize)",
                     data=b"\n".join(oids) + b"\n")
        for line in output.splitlines():
            oid, size = line.split()
            sizes[oid] = int(size)
    # Batch-read small blobs to detect LFS pointers without one process per file.
    small = [oid for oid in oids if sizes[oid] <= 1024]
    lfs_sizes = {}
    if small:
        output = git("cat-file", "--batch", data=b"\n".join(small) + b"\n")
        pos = 0
        for oid in small:
            end = output.index(b"\n", pos)
            size = int(output[pos:end].split()[-1])
            content = output[end + 1:end + 1 + size]
            pos = end + size + 2
            if content.startswith(b"version https://git-lfs.github.com/spec/v1\n"):
                match = re.search(rb"(?m)^size (\d+)$", content)
                if not match:
                    errors.append(f"invalid LFS pointer: {oid.decode()}")
                else:
                    lfs_sizes[oid] = int(match[1])
    for oid, path in entries:
        size = max(sizes[oid], lfs_sizes.get(oid, 0))
        if size > LIMIT:
            errors.append(f"over 100 MB ({size} bytes): {path}")
    if errors:
        print("Commit blocked:\n" + "\n".join(errors), file=sys.stderr)
        return 1
    print(f"Index verified: {len(entries)} files; no blob or LFS payload over {LIMIT} bytes.")
    return 0


if __name__ == "__main__":
    sys.exit(check())
