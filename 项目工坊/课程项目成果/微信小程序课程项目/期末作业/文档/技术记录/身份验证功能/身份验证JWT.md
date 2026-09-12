# 身份验证 —— JWT 设计

## JWT 载荷结构

**Access Token（15 分钟有效）：**
```json
{
    "iss": "AGC鉴赏画廊",
    "sub": "507f1f77bcf86cd799439011",
    "jti": "a1b2c3d4-e5f6-...",
    "type": "access",
    "iat": "2026-06-09T10:00:00Z",
    "nbf": "2026-06-09T10:00:00Z",
    "exp": "2026-06-09T10:15:00Z"
}
```

**Refresh Token（30 天有效）：**
```json
{
    "iss": "AGC鉴赏画廊",
    "sub": "507f1f77bcf86cd799439011",
    "jti": "b2c3d4e5-f6a7-...",
    "type": "refresh",
    "iat": "2026-06-09T10:00:00Z",
    "nbf": "2026-06-09T10:00:00Z",
    "exp": "2026-07-09T10:00:00Z"
}
```

| 字段 | 含义 | 说明 |
|------|------|------|
| `iss` | 签发者 | 防止跨应用滥用，值与 `APP_NAME` 一致 |
| `sub` | 用户 ID | MongoDB ObjectId 字符串，业务主体标识 |
| `jti` | Token 唯一 ID | UUID4，用于 Redis 精确撤销和重放检测 |
| `type` | Token 类型 | `access` 或 `refresh`，防止互换攻击 |
| `iat` | 签发时间 | UTC |
| `nbf` | 生效时间 | 与 iat 相同，即签即用 |
| `exp` | 过期时间 | access: +15min，refresh: +30day |

> 注意：JWT 载荷中**不包含** `email`、`role` 等业务字段。用户信息通过 `sub`（用户 ID）按需从 MongoDB 查询，保持 Token 轻量且避免过期数据。

---

## 关键安全原则

### 双密钥分离

Access Token 和 Refresh Token 使用**不同的密钥**签名：

| Token 类型 | 环境变量 |
|-----------|---------|
| Access | `ACCESS_TOKEN_SECRET_KEY` + `ACCESS_TOKEN_ALGORITHM`（HS256） |
| Refresh | `REFRESH_TOKEN_SECRET_KEY` + `REFRESH_TOKEN_ALGORITHM`（HS256） |

**为什么分离？** 如果只用一个密钥，一旦泄露，攻击者可以同时伪造 Access 和 Refresh Token。分离后，即使 Access 密钥泄露，Refresh Token 仍然安全。

### Refresh Token 轮换与重放检测

每次刷新请求都必须颁发全新的 Refresh Token，同时立即作废旧 Token：

- 正常流程：用户用旧 Refresh Token 换取新 Token 对 → 旧 Token 立即从 Redis 删除
- **重放检测**：当系统检测到已被用过的旧 Refresh Token 被再次提交，意味着该 Token 可能被盗取 → 立即撤销该用户的**所有**会话，强制全部设备重新登录
- 在 Redis 中存储 Key：`refresh:{user_id}:{jti}` → `"1"`，TTL 与 Refresh Token JWT 一致

### Token 类型校验

`type` 字段防止 Access/Refresh Token 互换攻击——用 Refresh Token 访问 API 或 Access Token 请求刷新都会被拒绝。
