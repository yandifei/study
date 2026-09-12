# rename-command SELECT "" 与 AOF 兼容性分析

## 配置组合

```conf
databases 1
rename-command SELECT ""
```

## 影响分析

| 场景 | 是否受影响 | 说明 |
|------|-----------|------|
| 客户端执行 `SELECT 1` | ✅ 被阻止 | 无法切换数据库，实现误切防护 |
| **AOF 日志写入** | ⚠️ 视情况而定 | `databases 1` 时只存在 db0，不会产生 `SELECT` 日志 |
| **AOF 文件回放** | ⚠️ 视情况而定 | 如果旧 AOF 文件中有 `SELECT` 命令，回放会失败 |
| **AOF 重写 (BGREWRITEAOF)** | ✅ 不受影响 | 内部通过 C 函数直调，不经过命令名查找 |

## 安全性结论

`databases 1` + `rename-command SELECT ""` **组合在一起是安全的**：

1. 只有一个数据库（db0），不会发生数据库切换，AOF 日志中不会产生 `SELECT` 命令
2. AOF 重写时，Redis 内部通过 C 函数直接调用，不经过命令名查找，`rename-command` 无法拦截

## 注意事项：旧 AOF 文件的处理

如果 AOF 文件是旧数据（之前 `databases` 不是 1 时产生的），里面可能残留 `SELECT` 命令，重启回放时会报错：

```
ERR unknown command 'SELECT'
```

### 解决方法

修改配置后，执行一次 AOF 重写清理旧日志：

```bash
redis-cli -a root BGREWRITEAOF
```

这会基于当前内存数据生成一份全新的、不含 `SELECT` 命令的 AOF 文件。

## 最佳实践

这是一个合理的生产环境安全加固实践，适用于：
- 单数据库部署（`databases 1`）
- 需要防止 `SELECT` 误切数据库的场景
- 开启 AOF 持久化的环境（需配合 `BGREWRITEAOF` 清理旧数据）

## 相关命令

```bash
# 查看当前数据库数量
redis-cli -a root CONFIG GET databases

# 查看键空间信息
redis-cli -a root INFO keyspace
```
