#!/bin/bash

# 1. 找出最大的文件
BIG_FILE=$(git rev-list --objects --all | \
           git cat-file --batch-check='%(objectsize) %(rest)' | \
           sort -n -r | head -1 | cut -d' ' -f2-)

# 2. 自动清理
if [ -n "$BIG_FILE" ]; then
  echo "🔥 正在清理大文件: $BIG_FILE"
  git filter-branch -f --index-filter "git rm --cached --ignore-unmatch '$BIG_FILE'" --prune-empty --tag-name-filter cat -- --all
  rm -rf .git/refs/original/
  git reflog expire --expire=now --all
  git gc --prune=now
  echo "✅ 清理完成！运行 git push --force 更新远程仓库"
else
  echo "⚠️ 未找到大文件，直接运行常规清理:"
  git gc --aggressive --prune=now
fi