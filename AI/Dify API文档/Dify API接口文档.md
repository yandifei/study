# Dify 对话型应用 API 接口文档

> 基于 Dify 自托管版本 (SELF_HOSTED)，应用类型：聊天助手  
> 基础 URL: `http://localhost/v1`  
> 文档来源：微信小程序-ACG画廊鉴赏 应用

---

## 目录

1. [概述](#概述)
2. [鉴权方式](#鉴权方式)
3. [API 接口列表](#api-接口列表)
   - [1. 发送对话消息](#1-发送对话消息)
   - [2. 上传文件](#2-上传文件)
   - [3. 获取终端用户](#3-获取终端用户)
   - [4. 文件预览](#4-文件预览)
   - [5. 停止响应](#5-停止响应)
   - [6. 消息反馈（点赞）](#6-消息反馈点赞)
   - [7. 获取APP的消息点赞和反馈](#7-获取app的消息点赞和反馈)
   - [8. 获取下一轮建议问题列表](#8-获取下一轮建议问题列表)
   - [9. 获取会话历史消息](#9-获取会话历史消息)
   - [10. 获取会话列表](#10-获取会话列表)
   - [11. 删除会话](#11-删除会话)
   - [12. 会话重命名](#12-会话重命名)
   - [13. 获取对话变量](#13-获取对话变量)
   - [14. 更新对话变量](#14-更新对话变量)
   - [15. 语音转文字](#15-语音转文字)
   - [16. 文字转语音](#16-文字转语音)
   - [17. 获取应用基本信息](#17-获取应用基本信息)
   - [18. 获取应用参数](#18-获取应用参数)
   - [19. 获取应用Meta信息](#19-获取应用meta信息)
   - [20. 获取应用 WebApp 设置](#20-获取应用-webapp-设置)
4. [通用数据结构](#通用数据结构)
5. [错误码汇总](#错误码汇总)

---

## 概述

对话型应用 API 支持会话持久化，可将之前的聊天记录作为上下文进行回答，适用于聊天/客服 AI 等场景。

- **API 服务器**: `http://localhost/v1`
- **Content-Type**: `application/json`（文件上传类接口使用 `multipart/form-data`）
- **响应模式**: 
  - `streaming`（流式模式，推荐）：基于 SSE (Server-Sent Events) 实现类似打字机输出方式的流式返回
  - `blocking`（阻塞模式）：等待执行完毕后返回结果（请求若流程较长可能会被中断，Cloudflare 限制 100 秒超时；Agent模式下不允许blocking）

---

## 鉴权方式

Service API 使用 `API-Key` 进行鉴权。

> ⚠️ **强烈建议开发者把 `API-Key` 放在后端存储，而非分享或者放在客户端存储，以免 `API-Key` 泄露，导致财产损失。**

所有 API 请求都应在 **`Authorization`** HTTP Header 中包含您的 `API-Key`：

```
Authorization: Bearer {API_KEY}
```

---

## API 接口列表

---

### 1. 发送对话消息

创建会话消息，支持流式和阻塞两种模式。

| 项目 | 内容 |
|------|------|
| **方法** | `POST` |
| **路径** | `/chat-messages` |

#### 请求体 (Request Body)

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| `query` | string | 是 | 用户输入/提问内容 |
| `inputs` | object | 否 | 允许传入 App 定义的各变量值。inputs 参数包含多组键值对（Key/Value pairs），每组的键对应一个特定变量，每组的值则是该变量的具体值。默认 `{}` |
| `response_mode` | string | 是 | 响应模式：`streaming`（流式模式，推荐）或 `blocking`（阻塞模式，Agent模式下不允许） |
| `user` | string | 是 | 用户标识，用于定义终端用户的身份，方便检索、统计。由开发者定义规则，需保证用户标识在应用内唯一。服务 API 不会共享 WebApp 创建的对话 |
| `conversation_id` | string | 否 | 会话 ID，需要基于之前的聊天记录继续对话时，必须传之前消息的 conversation_id |
| `files` | array[object] | 否 | 文件列表，适用于传入文件结合文本理解并回答问题，仅当模型支持 Vision/Video 能力时可用 |
| `auto_generate_name` | bool | 否 | 自动生成标题，默认 `true`。若设置为 `false`，则可通过调用会话重命名接口并设置 `auto_generate` 为 `true` 实现异步生成标题 |
| `workflow_id` | string | 否 | 工作流ID，用于指定特定版本，如果不提供则使用默认的已发布版本。获取方式：在版本历史界面，点击每个版本条目右侧的复制图标即可复制完整的工作流 ID |
| `trace_id` | string | 否 | 链路追踪ID。适用于与业务系统已有的trace组件打通，实现端到端分布式追踪等场景。如果未指定，系统会自动生成。支持三种方式传递（优先级依次降低）：<br>1. Header：通过 HTTP Header `X-Trace-Id` 传递，优先级最高<br>2. Query 参数：通过 URL 查询参数 `trace_id` 传递<br>3. Request Body：通过请求体字段 `trace_id` 传递 |

##### `files` 数组对象结构

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| `type` | string | 是 | 文件类型，支持：<br>• `document` — TXT, MD, MARKDOWN, MDX, PDF, HTML, XLSX, XLS, VTT, PROPERTIES, DOC, DOCX, CSV, EML, MSG, PPTX, PPT, XML, EPUB<br>• `image` — JPG, JPEG, PNG, GIF, WEBP, SVG<br>• `audio` — MP3, M4A, WAV, WEBM, MPGA<br>• `video` — MP4, MOV, MPEG, WEBM<br>• `custom` — 其他文件类型 |
| `transfer_method` | string | 是 | 传递方式：`remote_url`（文件地址）或 `local_file`（上传文件） |
| `url` | string | 条件 | 文件地址（仅当 `transfer_method` 为 `remote_url` 时必填） |
| `upload_file_id` | string | 条件 | 上传文件 ID（仅当 `transfer_method` 为 `local_file` 时必填） |

#### 响应：阻塞模式 (blocking)

返回完整的 App 结果，`Content-Type` 为 `application/json`。

**ChatCompletionResponse 结构：**

| 字段名 | 类型 | 描述 |
|--------|------|------|
| `event` | string | 事件类型，固定为 `message` |
| `task_id` | string | 任务 ID，用于请求跟踪和停止响应接口 |
| `id` | string | 唯一ID |
| `message_id` | string | 消息唯一 ID |
| `conversation_id` | string | 会话 ID |
| `mode` | string | App 模式，固定为 `chat` |
| `answer` | string | 完整回复内容 |
| `metadata` | object | 元数据（见下方详细结构） |
| `created_at` | int | 消息创建时间戳，如：1705395332 |

**metadata 结构：**

| 字段名 | 类型 | 描述 |
|--------|------|------|
| `usage` | Usage | 模型用量信息（见通用数据结构） |
| `retriever_resources` | array[RetrieverResource] | 引用和归属分段列表（见通用数据结构） |

#### 响应：流式模式 (streaming)

返回 App 输出的流式块，`Content-Type` 为 `text/event-stream`。每个流式块均以 `data:` 开头，块之间以 `\n\n`（两个换行符）分隔。

**流式事件类型：**

##### `event: message` — LLM 返回文本块事件

| 字段名 | 类型 | 描述 |
|--------|------|------|
| `task_id` | string | 任务 ID，用于请求跟踪和停止响应接口 |
| `message_id` | string | 消息唯一 ID |
| `conversation_id` | string | 会话 ID |
| `answer` | string | LLM 返回文本块内容 |
| `created_at` | int | 创建时间戳，如：1705395332 |

##### `event: agent_message` — Agent模式下返回文本块事件（仅Agent模式）

| 字段名 | 类型 | 描述 |
|--------|------|------|
| `task_id` | string | 任务 ID |
| `message_id` | string | 消息唯一 ID |
| `conversation_id` | string | 会话 ID |
| `answer` | string | LLM 返回文本块内容 |
| `created_at` | int | 创建时间戳 |

##### `event: agent_thought` — Agent思考步骤事件（仅Agent模式）

涉及工具调用，每轮Agent迭代都会有一个唯一的id。

| 字段名 | 类型 | 描述 |
|--------|------|------|
| `id` | string | agent_thought ID，每一轮Agent迭代都会有一个唯一的id |
| `task_id` | string | 任务ID |
| `message_id` | string | 消息唯一ID |
| `position` | int | agent_thought在消息中的位置，如第一轮迭代position为1 |
| `thought` | string | agent的思考内容 |
| `observation` | string | 工具调用的返回结果 |
| `tool` | string | 使用的工具列表，以 `;` 分割多个工具 |
| `tool_input` | string | 工具的输入，JSON格式的字符串(object)。如：`{"dalle3": {"prompt": "a cute cat"}}` |
| `created_at` | int | 创建时间戳 |
| `message_files` | array[string] | 当前 agent_thought 关联的文件ID |
| `conversation_id` | string | 会话ID |

##### `event: message_file` — 文件事件

| 字段名 | 类型 | 描述 |
|--------|------|------|
| `id` | string | 文件唯一ID |
| `type` | string | 文件类型，目前仅为`image` |
| `belongs_to` | string | 文件归属，`user`或`assistant`，该接口返回仅为 `assistant` |
| `url` | string | 文件访问地址 |
| `conversation_id` | string | 会话ID |

##### `event: message_end` — 消息结束事件

收到此事件则代表流式返回结束。

| 字段名 | 类型 | 描述 |
|--------|------|------|
| `task_id` | string | 任务 ID |
| `message_id` | string | 消息唯一 ID |
| `conversation_id` | string | 会话 ID |
| `metadata` | object | 元数据（含 usage 和 retriever_resources） |

##### `event: tts_message` — TTS 音频流事件

内容是Mp3格式的音频块，使用 base64 编码后的字符串。（开启自动播放才有此消息）

| 字段名 | 类型 | 描述 |
|--------|------|------|
| `task_id` | string | 任务 ID |
| `message_id` | string | 消息唯一 ID |
| `audio` | string | 语音合成之后的音频块使用 Base64 编码之后的文本内容，播放时直接 base64 解码送入播放器即可 |
| `created_at` | int | 创建时间戳 |

##### `event: tts_message_end` — TTS 音频流结束事件

| 字段名 | 类型 | 描述 |
|--------|------|------|
| `task_id` | string | 任务 ID |
| `message_id` | string | 消息唯一 ID |
| `audio` | string | 结束事件无音频，空字符串 |
| `created_at` | int | 创建时间戳 |

##### `event: message_replace` — 消息内容替换事件

开启内容审查和审查输出内容时，若命中了审查条件，则会通过此事件替换消息内容为预设回复。

| 字段名 | 类型 | 描述 |
|--------|------|------|
| `task_id` | string | 任务 ID |
| `message_id` | string | 消息唯一 ID |
| `conversation_id` | string | 会话 ID |
| `answer` | string | 替换内容（直接替换 LLM 所有回复文本） |
| `created_at` | int | 创建时间戳 |

##### `event: error` — 错误事件

流式输出过程中出现的异常会以 stream event 形式输出，收到异常事件后即结束。

| 字段名 | 类型 | 描述 |
|--------|------|------|
| `task_id` | string | 任务 ID |
| `message_id` | string | 消息唯一 ID |
| `status` | int | HTTP 状态码 |
| `code` | string | 错误码 |
| `message` | string | 错误消息 |

##### `event: ping` — 心跳事件

每 10s 一次的 ping 事件，保持连接存活。

#### 错误码

| HTTP状态码 | 错误码 | 描述 |
|-----------|--------|------|
| 404 | — | 对话不存在 |
| 400 | `invalid_param` | 传入参数异常 |
| 400 | `app_unavailable` | App 配置不可用 |
| 400 | `provider_not_initialize` | 无可用模型凭据配置 |
| 400 | `provider_quota_exceeded` | 模型调用额度不足 |
| 400 | `model_currently_not_support` | 当前模型不可用 |
| 400 | `workflow_not_found` | 指定的工作流版本未找到 |
| 400 | `draft_workflow_error` | 无法使用草稿工作流版本 |
| 400 | `workflow_id_format_error` | 工作流ID格式错误，需要UUID格式 |
| 400 | `completion_request_error` | 文本生成失败 |
| 500 | — | 服务内部异常 |

#### 请求示例

```bash
curl -X POST 'http://localhost/v1/chat-messages' \
  --header 'Authorization: Bearer {api_key}' \
  --header 'Content-Type: application/json' \
  --data-raw '{
    "inputs": {},
    "query": "What are the specs of the iPhone 13 Pro Max?",
    "response_mode": "streaming",
    "conversation_id": "",
    "user": "abc-123",
    "files": [
      {
        "type": "image",
        "transfer_method": "remote_url",
        "url": "https://cloud.dify.ai/logo/logo-site.png"
      }
    ]
  }'
```

#### 阻塞模式响应示例

```json
{
    "event": "message",
    "task_id": "c3800678-a077-43df-a102-53f23ed20b88",
    "id": "9da23599-e713-473b-982c-4328d4f5c78a",
    "message_id": "9da23599-e713-473b-982c-4328d4f5c78a",
    "conversation_id": "45701982-8118-4bc5-8e9b-64562b4555f2",
    "mode": "chat",
    "answer": "iPhone 13 Pro Max specs are listed here:...",
    "metadata": {
        "usage": {
            "prompt_tokens": 1033,
            "prompt_unit_price": "0.001",
            "prompt_price_unit": "0.001",
            "prompt_price": "0.0010330",
            "completion_tokens": 128,
            "completion_unit_price": "0.002",
            "completion_price_unit": "0.001",
            "completion_price": "0.0002560",
            "total_tokens": 1161,
            "total_price": "0.0012890",
            "currency": "USD",
            "latency": 0.7682376249867957
        },
        "retriever_resources": [
            {
                "position": 1,
                "dataset_id": "101b4c97-fc2e-463c-90b1-5261a4cdcafb",
                "dataset_name": "iPhone",
                "document_id": "8dd1ad74-0b5f-4175-b735-7d98bbbb4e00",
                "document_name": "iPhone List",
                "segment_id": "ed599c7f-2766-4294-9d1d-e5235a61270a",
                "score": 0.98457545,
                "content": "\"Model\",\"Release Date\",\"Display Size\"..."
            }
        ]
    },
    "created_at": 1705407629
}
```

#### 流式模式响应示例（基础助手）

```
data: {"event": "message", "message_id": "5ad4cb98-f0c7-4085-b384-88c403be6290", "conversation_id": "45701982-8118-4bc5-8e9b-64562b4555f2", "answer": " I", "created_at": 1679586595}
data: {"event": "message", "message_id": "5ad4cb98-f0c7-4085-b384-88c403be6290", "conversation_id": "45701982-8118-4bc5-8e9b-64562b4555f2", "answer": "'m", "created_at": 1679586595}
data: {"event": "message", "message_id": "5ad4cb98-f0c7-4085-b384-88c403be6290", "conversation_id": "45701982-8118-4bc5-8e9b-64562b4555f2", "answer": " glad", "created_at": 1679586595}
data: {"event": "message_end", "id": "5e52ce04-874b-4d27-9045-b3bc80def685", "conversation_id": "45701982-8118-4bc5-8e9b-64562b4555f2", "metadata": { ... }}
```

---

### 2. 上传文件

上传文件（支持图片等）并在发送消息时使用，可实现图文多模态理解。支持 `png, jpg, jpeg, webp, gif` 格式。

> 上传的文件仅供当前终端用户使用。

| 项目 | 内容 |
|------|------|
| **方法** | `POST` |
| **路径** | `/files/upload` |
| **Content-Type** | `multipart/form-data` |

#### 请求体

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| `file` | file | 是 | 要上传的文件 |
| `user` | string | 是 | 用户标识，用于定义终端用户的身份，必须和发送消息接口传入 user 保持一致。服务 API 不会共享 WebApp 创建的对话 |

#### 响应

| 字段名 | 类型 | 描述 |
|--------|------|------|
| `id` | uuid | 文件ID |
| `name` | string | 文件名 |
| `size` | int | 文件大小（byte） |
| `extension` | string | 文件后缀 |
| `mime_type` | string | 文件 mime-type |
| `created_by` | uuid | 上传人 ID |
| `created_at` | timestamp | 上传时间 |

#### 错误码

| HTTP状态码 | 错误码 | 描述 |
|-----------|--------|------|
| 400 | `no_file_uploaded` | 必须提供文件 |
| 400 | `too_many_files` | 目前只接受一个文件 |
| 400 | `unsupported_preview` | 该文件不支持预览 |
| 400 | `unsupported_estimate` | 该文件不支持估算 |
| 413 | `file_too_large` | 文件太大 |
| 415 | `unsupported_file_type` | 不支持的扩展名，当前只接受文档类文件 |
| 503 | `s3_connection_failed` | 无法连接到 S3 服务 |
| 503 | `s3_permission_denied` | 无权限上传文件到 S3 |
| 503 | `s3_file_too_large` | 文件超出 S3 大小限制 |

#### 请求示例

```bash
curl -X POST 'http://localhost/v1/files/upload' \
  --header 'Authorization: Bearer {api_key}' \
  --form 'file=@localfile;type=image/[png|jpeg|jpg|webp|gif]' \
  --form 'user=abc-123'
```

#### 响应示例

```json
{
  "id": "72fa9618-8f89-4a37-9b33-7e1178a24a67",
  "name": "example.png",
  "size": 1024,
  "extension": "png",
  "mime_type": "image/png",
  "created_by": 123,
  "created_at": 1577836800
}
```

---

### 3. 获取终端用户

通过终端用户 ID 获取终端用户信息。当其他 API 返回终端用户 ID（例如：上传文件接口返回的 `created_by`）时，可使用该接口查询对应的终端用户信息。

| 项目 | 内容 |
|------|------|
| **方法** | `GET` |
| **路径** | `/end-users/:end_user_id` |

#### 路径参数

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| `end_user_id` | uuid | 是 | 终端用户 ID |

#### 响应（EndUser 对象）

| 字段名 | 类型 | 描述 |
|--------|------|------|
| `id` | uuid | ID |
| `tenant_id` | uuid | 工作空间（Tenant）ID |
| `app_id` | uuid | 应用 ID |
| `type` | string | 终端用户类型 |
| `external_user_id` | string | 外部用户 ID |
| `name` | string | 名称 |
| `is_anonymous` | boolean | 是否匿名 |
| `session_id` | string | 会话 ID |
| `created_at` | string | ISO 8601 时间 |
| `updated_at` | string | ISO 8601 时间 |

#### 错误码

| HTTP状态码 | 错误码 | 描述 |
|-----------|--------|------|
| 404 | `end_user_not_found` | 终端用户不存在 |
| 500 | — | 内部服务器错误 |

#### 请求示例

```bash
curl -X GET 'http://localhost/v1/end-users/6ad1ab0a-73ff-4ac1-b9e4-cdb312f71f13' \
  --header 'Authorization: Bearer {api_key}'
```

---

### 4. 文件预览

预览或下载已上传的文件。此端点允许访问先前通过文件上传 API 上传的文件。

> 文件只能在属于请求应用程序的消息范围内访问。

| 项目 | 内容 |
|------|------|
| **方法** | `GET` |
| **路径** | `/files/:file_id/preview` |

#### 路径参数

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| `file_id` | string | 是 | 要预览的文件的唯一标识符，从文件上传 API 响应中获得 |

#### 查询参数

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| `as_attachment` | boolean | 否 | 是否强制将文件作为附件下载。默认为 `false`（在浏览器中预览） |

#### 响应头

- `Content-Type` — 根据文件 MIME 类型设置
- `Content-Length` — 文件大小（以字节为单位，如果可用）
- `Content-Disposition` — 如果 `as_attachment=true` 则设置为 "attachment"
- `Cache-Control` — 用于性能的缓存标头
- `Accept-Ranges` — 对于音频/视频文件设置为 "bytes"

#### 错误码

| HTTP状态码 | 错误码 | 描述 |
|-----------|--------|------|
| 400 | `invalid_param` | 参数输入异常 |
| 403 | `file_access_denied` | 文件访问被拒绝或文件不属于当前应用程序 |
| 404 | `file_not_found` | 文件未找到或已被删除 |
| 500 | — | 服务内部错误 |

#### 请求示例

```bash
# 预览模式
curl -X GET 'http://localhost/v1/files/72fa9618-8f89-4a37-9b33-7e1178a24a67/preview' \
  --header 'Authorization: Bearer {api_key}'

# 下载模式
curl -X GET 'http://localhost/v1/files/72fa9618-8f89-4a37-9b33-7e1178a24a67/preview?as_attachment=true' \
  --header 'Authorization: Bearer {api_key}' \
  --output downloaded_file.png
```

---

### 5. 停止响应

仅支持流式模式。

| 项目 | 内容 |
|------|------|
| **方法** | `POST` |
| **路径** | `/chat-messages/:task_id/stop` |

#### 路径参数

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| `task_id` | string | 是 | 任务 ID，可在流式返回 Chunk 中获取 |

#### 请求体

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| `user` | string | 是 | 用户标识，必须和发送消息接口传入 user 保持一致 |

#### 响应

| 字段名 | 类型 | 描述 |
|--------|------|------|
| `result` | string | 固定返回 `success` |

#### 请求示例

```bash
curl -X POST 'http://localhost/v1/chat-messages/:task_id/stop' \
  -H 'Authorization: Bearer {api_key}' \
  -H 'Content-Type: application/json' \
  --data-raw '{ "user": "abc-123"}'
```

---

### 6. 消息反馈（点赞）

消息终端用户反馈、点赞，方便应用开发者优化输出预期。

| 项目 | 内容 |
|------|------|
| **方法** | `POST` |
| **路径** | `/messages/:message_id/feedbacks` |

#### 路径参数

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| `message_id` | string | 是 | 消息 ID |

#### 请求体

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| `rating` | string | 是 | 点赞 `like`，点踩 `dislike`，撤销点赞 `null` |
| `user` | string | 是 | 用户标识，需保证用户标识在应用内唯一 |
| `content` | string | 否 | 消息反馈的具体信息 |

#### 响应

| 字段名 | 类型 | 描述 |
|--------|------|------|
| `result` | string | 固定返回 `success` |

#### 请求示例

```bash
curl -X POST 'http://localhost/v1/messages/:message_id/feedbacks' \
  --header 'Authorization: Bearer {api_key}' \
  --header 'Content-Type: application/json' \
  --data-raw '{
    "rating": "like",
    "user": "abc-123",
    "content": "message feedback information"
  }'
```

---

### 7. 获取APP的消息点赞和反馈

获取应用的终端用户反馈、点赞。

| 项目 | 内容 |
|------|------|
| **方法** | `GET` |
| **路径** | `/app/feedbacks` |

#### 查询参数

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| `page` | string | 否 | 分页，默认值：1 |
| `limit` | string | 否 | 每页数量，默认值：20 |

#### 响应

| 字段名 | 类型 | 描述 |
|--------|------|------|
| `data` | List | 返回该APP的点赞、反馈列表 |

#### 请求示例

```bash
curl -X GET 'http://localhost/v1/app/feedbacks?page=1&limit=20'
```

#### 响应示例

```json
{
    "data": [
        {
            "id": "8c0fbed8-e2f9-49ff-9f0e-15a35bdd0e25",
            "app_id": "f252d396-fe48-450e-94ec-e184218e7346",
            "conversation_id": "2397604b-9deb-430e-b285-4726e51fd62d",
            "message_id": "709c0b0f-0a96-4a4e-91a4-ec0889937b11",
            "rating": "like",
            "content": "message feedback information-3",
            "from_source": "user",
            "from_end_user_id": "74286412-9a1a-42c1-929c-01edb1d381d5",
            "from_account_id": null,
            "created_at": "2025-04-24T09:24:38",
            "updated_at": "2025-04-24T09:24:38"
        }
    ]
}
```

---

### 8. 获取下一轮建议问题列表

| 项目 | 内容 |
|------|------|
| **方法** | `GET` |
| **路径** | `/messages/{message_id}/suggested` |

#### 路径参数

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| `message_id` | string | 是 | 消息 ID |

#### 查询参数

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| `user` | string | 是 | 用户标识，需保证用户标识在应用内唯一 |

#### 请求示例

```bash
curl --location --request GET 'http://localhost/v1/messages/{message_id}/suggested?user=abc-123' \
  --header 'Authorization: Bearer {api_key}' \
  --header 'Content-Type: application/json'
```

#### 响应示例

```json
{
  "result": "success",
  "data": ["a", "b", "c"]
}
```

---

### 9. 获取会话历史消息

滚动加载形式返回历史聊天记录，第一页返回最新 `limit` 条，即：倒序返回。

| 项目 | 内容 |
|------|------|
| **方法** | `GET` |
| **路径** | `/messages` |

#### 查询参数

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| `conversation_id` | string | 是 | 会话 ID |
| `user` | string | 是 | 用户标识，需保证用户标识在应用内唯一 |
| `first_id` | string | 否 | 当前页第一条聊天记录的 ID，默认 null |
| `limit` | int | 否 | 一次请求返回多少条聊天记录，默认 20 条 |

#### 响应

| 字段名 | 类型 | 描述 |
|--------|------|------|
| `data` | array[object] | 消息列表（见下方详细结构） |
| `has_more` | bool | 是否存在下一页 |
| `limit` | int | 返回条数，若传入超过系统限制，返回系统限制数量 |

##### data 数组对象结构

| 字段名 | 类型 | 描述 |
|--------|------|------|
| `id` | string | 消息 ID |
| `conversation_id` | string | 会话 ID |
| `inputs` | object | 用户输入参数 |
| `query` | string | 用户输入/提问内容 |
| `message_files` | array[object] | 消息文件（含 id, type, url, belongs_to） |
| `answer` | string | 回答消息内容 |
| `created_at` | timestamp | 创建时间 |
| `feedback` | object | 反馈信息（含 rating：like/dislike） |
| `retriever_resources` | array[RetrieverResource] | 引用和归属分段列表 |
| `agent_thoughts` | array[object] | Agent思考内容（仅Agent模式下不为空，见通用数据结构） |

#### 请求示例

```bash
curl -X GET 'http://localhost/v1/messages?user=abc-123&conversation_id=' \
  --header 'Authorization: Bearer {api_key}'
```

---

### 10. 获取会话列表

获取当前用户的会话列表，默认返回最近的 20 条。

| 项目 | 内容 |
|------|------|
| **方法** | `GET` |
| **路径** | `/conversations` |

#### 查询参数

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| `user` | string | 是 | 用户标识，需保证用户标识在应用内唯一 |
| `last_id` | string | 否 | 当前页最后面一条记录的 ID，默认 null |
| `limit` | int | 否 | 一次请求返回多少条记录，默认 20 条，最大 100 条，最小 1 条 |
| `sort_by` | string | 否 | 排序字段，默认 `-updated_at`（按更新时间倒序排列）。可选值：`created_at`, `-created_at`, `updated_at`, `-updated_at`（`-` 代表倒序） |

#### 响应

| 字段名 | 类型 | 描述 |
|--------|------|------|
| `data` | array[object] | 会话列表 |
| `has_more` | bool | 是否有更多 |
| `limit` | int | 返回条数 |

##### data 数组对象结构

| 字段名 | 类型 | 描述 |
|--------|------|------|
| `id` | string | 会话 ID |
| `name` | string | 会话名称，默认为会话中用户最开始问题的截取 |
| `inputs` | object | 用户输入参数 |
| `status` | string | 会话状态 |
| `introduction` | string | 开场白 |
| `created_at` | timestamp | 创建时间 |
| `updated_at` | timestamp | 更新时间 |

#### 请求示例

```bash
curl -X GET 'http://localhost/v1/conversations?user=abc-123&last_id=&limit=20' \
  --header 'Authorization: Bearer {api_key}'
```

---

### 11. 删除会话

| 项目 | 内容 |
|------|------|
| **方法** | `DELETE` |
| **路径** | `/conversations/:conversation_id` |

#### 路径参数

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| `conversation_id` | string | 是 | 会话 ID |

#### 请求体

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| `user` | string | 是 | 用户标识，需保证用户标识在应用内唯一 |

#### 响应

```
204 No Content
```

#### 请求示例

```bash
curl -X DELETE 'http://localhost/v1/conversations/:conversation_id' \
  --header 'Authorization: Bearer {api_key}' \
  --header 'Content-Type: application/json' \
  --data-raw '{
    "user": "abc-123"
  }'
```

---

### 12. 会话重命名

对会话进行重命名，会话名称用于显示在支持多会话的客户端上。

| 项目 | 内容 |
|------|------|
| **方法** | `POST` |
| **路径** | `/conversations/:conversation_id/name` |

#### 路径参数

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| `conversation_id` | string | 是 | 会话 ID |

#### 请求体

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| `name` | string | 否 | 名称，若 `auto_generate` 为 `true` 时，该参数可不传 |
| `auto_generate` | bool | 否 | 自动生成标题，默认 false |
| `user` | string | 是 | 用户标识，需保证用户标识在应用内唯一 |

#### 响应

| 字段名 | 类型 | 描述 |
|--------|------|------|
| `id` | string | 会话 ID |
| `name` | string | 会话名称 |
| `inputs` | object | 用户输入参数 |
| `status` | string | 会话状态 |
| `introduction` | string | 开场白 |
| `created_at` | timestamp | 创建时间 |
| `updated_at` | timestamp | 更新时间 |

#### 请求示例

```bash
curl -X POST 'http://localhost/v1/conversations/:conversation_id/name' \
  --header 'Authorization: Bearer {api_key}' \
  --header 'Content-Type: application/json' \
  --data-raw '{
    "name": "",
    "auto_generate": true,
    "user": "abc-123"
  }'
```

---

### 13. 获取对话变量

从特定对话中检索变量。此端点对于提取对话过程中捕获的结构化数据非常有用。

| 项目 | 内容 |
|------|------|
| **方法** | `GET` |
| **路径** | `/conversations/:conversation_id/variables` |

#### 路径参数

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| `conversation_id` | string | 是 | 要从中检索变量的对话ID |

#### 查询参数

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| `user` | string | 是 | 用户标识符，在应用程序内必须唯一 |
| `last_id` | string | 否 | 当前页最后面一条记录的 ID，默认 null |
| `limit` | int | 否 | 一次请求返回多少条记录，默认 20 条，最大 100 条，最小 1 条 |
| `variable_name` | string | 否 | 按变量名称过滤 |

#### 响应

| 字段名 | 类型 | 描述 |
|--------|------|------|
| `limit` | int | 每页项目数 |
| `has_more` | bool | 是否有更多项目 |
| `data` | array[object] | 变量列表 |

##### data 数组对象结构

| 字段名 | 类型 | 描述 |
|--------|------|------|
| `id` | string | 变量 ID |
| `name` | string | 变量名称 |
| `value_type` | string | 变量类型（string、number、json 等） |
| `value` | string/any | 变量值 |
| `description` | string | 变量描述 |
| `created_at` | int | 创建时间戳 |
| `updated_at` | int | 最后更新时间戳 |

#### 错误码

| HTTP状态码 | 错误码 | 描述 |
|-----------|--------|------|
| 404 | `conversation_not_exists` | 对话不存在 |

#### 请求示例

```bash
# 获取所有变量
curl -X GET 'http://localhost/v1/conversations/{conversation_id}/variables?user=abc-123' \
  --header 'Authorization: Bearer {api_key}'

# 按变量名过滤
curl -X GET 'http://localhost/v1/conversations/{conversation_id}/variables?user=abc-123&variable_name=customer_name' \
  --header 'Authorization: Bearer {api_key}'
```

---

### 14. 更新对话变量

更新特定对话变量的值。此端点允许您修改在对话过程中捕获的变量值，同时保留其名称、类型和描述。

| 项目 | 内容 |
|------|------|
| **方法** | `PUT` |
| **路径** | `/conversations/:conversation_id/variables/:variable_id` |

#### 路径参数

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| `conversation_id` | string | 是 | 包含要更新变量的对话ID |
| `variable_id` | string | 是 | 要更新的变量ID |

#### 请求体

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| `value` | any | 是 | 变量的新值。必须匹配变量的预期类型（字符串、数字、对象等） |
| `user` | string | 是 | 用户标识符，在应用程序内必须唯一 |

#### 响应

| 字段名 | 类型 | 描述 |
|--------|------|------|
| `id` | string | 变量ID |
| `name` | string | 变量名称 |
| `value_type` | string | 变量类型 |
| `value` | any | 更新后的变量值 |
| `description` | string | 变量描述 |
| `created_at` | int | 创建时间戳 |
| `updated_at` | int | 最后更新时间戳 |

#### 错误码

| HTTP状态码 | 错误码 | 描述 |
|-----------|--------|------|
| 400 | `Type mismatch` | 值类型与变量的预期类型不匹配 |
| 404 | `conversation_not_exists` | 对话不存在 |
| 404 | `conversation_variable_not_exists` | 变量不存在 |

#### 请求示例

```bash
curl -X PUT 'http://localhost/v1/conversations/{conversation_id}/variables/{variable_id}' \
  --header 'Authorization: Bearer {api_key}' \
  --header 'Content-Type: application/json' \
  --data-raw '{
    "value": "Updated Value",
    "user": "abc-123"
  }'
```

---

### 15. 语音转文字

| 项目 | 内容 |
|------|------|
| **方法** | `POST` |
| **路径** | `/audio-to-text` |
| **Content-Type** | `multipart/form-data` |

#### 请求体

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| `file` | file | 是 | 语音文件。支持格式：`mp3, mp4, mpeg, mpga, m4a, wav, webm`。文件大小限制：15MB |
| `user` | string | 是 | 用户标识，需保证用户标识在应用内唯一 |

#### 响应

| 字段名 | 类型 | 描述 |
|--------|------|------|
| `text` | string | 输出文字 |

#### 请求示例

```bash
curl -X POST 'http://localhost/v1/audio-to-text' \
  --header 'Authorization: Bearer {api_key}' \
  --form 'file=@localfile;type=audio/[mp3|mp4|mpeg|mpga|m4a|wav|webm]'
```

#### 响应示例

```json
{
  "text": "hello"
}
```

---

### 16. 文字转语音

文字转语音，生成语音内容。

| 项目 | 内容 |
|------|------|
| **方法** | `POST` |
| **路径** | `/text-to-audio` |

#### 请求体

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| `message_id` | string | 否 | Dify 生成的文本消息ID。后台会通过 message_id 查找相应的内容直接合成语音信息。如果同时传 message_id 和 text，优先使用 message_id |
| `text` | string | 否 | 语音生成内容。如果没有传 message_id 的话，则会使用这个字段的内容 |
| `user` | string | 是 | 用户标识，需保证用户标识在应用内唯一 |

#### 响应头

```
Content-Type: audio/wav
```

> 响应体为音频文件的二进制流数据。

#### 请求示例

```bash
curl --location --request POST 'http://localhost/v1/text-to-audio' \
  --header 'Authorization: Bearer {api_key}' \
  --form 'text=你好Dify;user=abc-123;message_id=5ad4cb98-f0c7-4085-b384-88c403be6290'
```

---

### 17. 获取应用基本信息

| 项目 | 内容 |
|------|------|
| **方法** | `GET` |
| **路径** | `/info` |

#### 响应

| 字段名 | 类型 | 描述 |
|--------|------|------|
| `name` | string | 应用名称 |
| `description` | string | 应用描述 |
| `tags` | array[string] | 应用标签 |
| `mode` | string | 应用模式（如：`chat`） |
| `author_name` | string | 作者名称 |

#### 请求示例

```bash
curl -X GET 'http://localhost/v1/info' \
  -H 'Authorization: Bearer {api_key}'
```

#### 响应示例

```json
{
  "name": "My App",
  "description": "This is my app.",
  "tags": ["tag1", "tag2"],
  "mode": "chat",
  "author_name": "Dify"
}
```

---

### 18. 获取应用参数

用于进入页面一开始，获取功能开关、输入参数名称、类型及默认值等使用。

| 项目 | 内容 |
|------|------|
| **方法** | `GET` |
| **路径** | `/parameters` |

#### 响应

| 字段名 | 类型 | 描述 |
|--------|------|------|
| `opening_statement` | string | 开场白 |
| `suggested_questions` | array[string] | 开场推荐问题列表 |
| `suggested_questions_after_answer` | object | 启用回答后给出推荐问题（含 `enabled` 字段） |
| `speech_to_text` | object | 语音转文本配置（含 `enabled` 字段） |
| `text_to_speech` | object | 文本转语音配置（含 `enabled`, `voice`, `language`, `autoPlay`） |
| `retriever_resource` | object | 引用和归属配置（含 `enabled` 字段） |
| `annotation_reply` | object | 标记回复配置（含 `enabled` 字段） |
| `user_input_form` | array[object] | 用户输入表单配置 |
| `file_upload` | object | 文件上传配置 |
| `system_parameters` | object | 系统参数 |

##### `user_input_form` 支持的控件类型

**text-input（文本输入控件）：**

| 字段名 | 类型 | 描述 |
|--------|------|------|
| `label` | string | 控件展示标签名 |
| `variable` | string | 控件 ID |
| `required` | bool | 是否必填 |
| `max_length` | int | 最大长度 |
| `default` | string | 默认值 |

**paragraph（段落文本输入控件）：**

| 字段名 | 类型 | 描述 |
|--------|------|------|
| `label` | string | 控件展示标签名 |
| `variable` | string | 控件 ID |
| `required` | bool | 是否必填 |
| `default` | string | 默认值 |

**select（下拉控件）：**

| 字段名 | 类型 | 描述 |
|--------|------|------|
| `label` | string | 控件展示标签名 |
| `variable` | string | 控件 ID |
| `required` | bool | 是否必填 |
| `default` | string | 默认值 |
| `options` | array[string] | 选项值 |

##### `file_upload` 配置结构

| 字段名 | 类型 | 描述 |
|--------|------|------|
| `document` | object | 文档设置（`enabled`, `number_limits`, `transfer_methods`） |
| `image` | object | 图片设置（`enabled`, `number_limits`, `transfer_methods`） |
| `audio` | object | 音频设置（`enabled`, `number_limits`, `transfer_methods`） |
| `video` | object | 视频设置（`enabled`, `number_limits`, `transfer_methods`） |
| `custom` | object | 自定义文件设置（`enabled`, `number_limits`, `transfer_methods`） |

##### `system_parameters` 结构

| 字段名 | 类型 | 描述 |
|--------|------|------|
| `file_size_limit` | int | 文档上传大小限制 (MB) |
| `image_file_size_limit` | int | 图片文件上传大小限制（MB） |
| `audio_file_size_limit` | int | 音频文件上传大小限制 (MB) |
| `video_file_size_limit` | int | 视频文件上传大小限制 (MB) |

#### 请求示例

```bash
curl -X GET 'http://localhost/v1/parameters' \
  --header 'Authorization: Bearer {api_key}'
```

---

### 19. 获取应用Meta信息

用于获取工具的 icon 信息。

| 项目 | 内容 |
|------|------|
| **方法** | `GET` |
| **路径** | `/meta` |

#### 响应

| 字段名 | 类型 | 描述 |
|--------|------|------|
| `tool_icons` | object[string] | 工具图标映射。key 为工具名称，value 为图标信息 |

**tool_icons 中每个工具的值结构：**

| 字段名 | 类型 | 描述 |
|--------|------|------|
| — | object | 图标对象，含 `background`（hex 格式的背景色）和 `content`（emoji） |
| — | string | 图标 URL |

#### 请求示例

```bash
curl -X GET 'http://localhost/v1/meta' \
  -H 'Authorization: Bearer {api_key}'
```

#### 响应示例

```json
{
  "tool_icons": {
    "dalle2": "https://cloud.dify.ai/console/api/workspaces/current/tool-provider/builtin/dalle/icon",
    "api_tool": {
      "background": "#252525",
      "content": "😁"
    }
  }
}
```

---

### 20. 获取应用 WebApp 设置

用于获取应用的 WebApp 设置。

| 项目 | 内容 |
|------|------|
| **方法** | `GET` |
| **路径** | `/site` |

#### 响应

| 字段名 | 类型 | 描述 |
|--------|------|------|
| `title` | string | WebApp 名称 |
| `chat_color_theme` | string | 聊天颜色主题，hex 格式 |
| `chat_color_theme_inverted` | bool | 聊天颜色主题是否反转 |
| `icon_type` | string | 图标类型，`emoji`（表情）或 `image`（图片） |
| `icon` | string | 图标。如果是 emoji 类型则是 emoji 表情符号；如果是 image 类型则是图片 URL |
| `icon_background` | string | hex 格式的背景色 |
| `icon_url` | string \| null | 图标 URL |
| `description` | string | 描述 |
| `copyright` | string | 版权信息 |
| `privacy_policy` | string | 隐私政策链接 |
| `custom_disclaimer` | string | 自定义免责声明 |
| `default_language` | string | 默认语言 |
| `show_workflow_steps` | bool | 是否显示工作流详情 |
| `use_icon_as_answer_icon` | bool | 是否使用 WebApp 图标替换聊天中的 🤖 |

#### 请求示例

```bash
curl -X GET 'http://localhost/v1/site' \
  -H 'Authorization: Bearer {api_key}'
```

#### 响应示例

```json
{
  "title": "My App",
  "chat_color_theme": "#ff4a4a",
  "chat_color_theme_inverted": false,
  "icon_type": "emoji",
  "icon": "😄",
  "icon_background": "#FFEAD5",
  "icon_url": null,
  "description": "This is my app.",
  "copyright": "all rights reserved",
  "privacy_policy": "",
  "custom_disclaimer": "All generated by AI",
  "default_language": "en-US",
  "show_workflow_steps": false,
  "use_icon_as_answer_icon": false
}
```

---

## 通用数据结构

### Usage（模型用量信息）

| 字段名 | 类型 | 描述 |
|--------|------|------|
| `prompt_tokens` | int | 提示词 token 数 |
| `prompt_unit_price` | string | 提示词单价 |
| `prompt_price_unit` | string | 提示词价格单位 |
| `prompt_price` | string | 提示词总价 |
| `completion_tokens` | int | 补全 token 数 |
| `completion_unit_price` | string | 补全单价 |
| `completion_price_unit` | string | 补全价格单位 |
| `completion_price` | string | 补全总价 |
| `total_tokens` | int | 总 token 数 |
| `total_price` | string | 总价格 |
| `currency` | string | 货币单位（如：USD） |
| `latency` | float | 延迟（秒） |

### RetrieverResource（引用和归属分段）

| 字段名 | 类型 | 描述 |
|--------|------|------|
| `position` | int | 引用位置 |
| `dataset_id` | string | 数据集 ID |
| `dataset_name` | string | 数据集名称 |
| `document_id` | string | 文档 ID |
| `document_name` | string | 文档名称 |
| `segment_id` | string | 分段 ID |
| `score` | float | 相关性分数 |
| `content` | string | 分段内容 |

### AgentThought（Agent思考内容）

| 字段名 | 类型 | 描述 |
|--------|------|------|
| `id` | string | agent_thought ID |
| `chain_id` | string \| null | 链 ID |
| `message_id` | string | 消息唯一ID |
| `position` | int | 在消息中的位置 |
| `thought` | string | agent的思考内容 |
| `observation` | string | 工具调用的返回结果 |
| `tool` | string | 使用的工具列表，以 `;` 分割多个工具 |
| `tool_input` | string | 工具的输入，JSON格式的字符串 |
| `created_at` | int | 创建时间戳 |
| `files` | array[string] | 关联的文件ID列表 |
| `conversation_id` | string | 会话ID |

### MessageFile（消息文件）

| 字段名 | 类型 | 描述 |
|--------|------|------|
| `id` | string | 文件ID |
| `type` | string | 文件类型（`image` 等） |
| `url` | string | 文件预览地址，使用文件预览 API (`/files/{file_id}/preview`) 访问 |
| `belongs_to` | string | 文件归属方，`user` 或 `assistant` |

---

## 错误码汇总

### 通用错误

| HTTP状态码 | 错误码 | 描述 |
|-----------|--------|------|
| 400 | `invalid_param` | 传入参数异常 |
| 400 | `app_unavailable` | App 配置不可用 |
| 404 | — | 资源不存在 |
| 500 | — | 服务内部异常 |

### 发送消息相关

| HTTP状态码 | 错误码 | 描述 |
|-----------|--------|------|
| 400 | `provider_not_initialize` | 无可用模型凭据配置 |
| 400 | `provider_quota_exceeded` | 模型调用额度不足 |
| 400 | `model_currently_not_support` | 当前模型不可用 |
| 400 | `workflow_not_found` | 指定的工作流版本未找到 |
| 400 | `draft_workflow_error` | 无法使用草稿工作流版本 |
| 400 | `workflow_id_format_error` | 工作流ID格式错误，需要UUID格式 |
| 400 | `completion_request_error` | 文本生成失败 |
| 404 | — | 对话不存在 |

### 文件上传相关

| HTTP状态码 | 错误码 | 描述 |
|-----------|--------|------|
| 400 | `no_file_uploaded` | 必须提供文件 |
| 400 | `too_many_files` | 目前只接受一个文件 |
| 400 | `unsupported_preview` | 该文件不支持预览 |
| 400 | `unsupported_estimate` | 该文件不支持估算 |
| 413 | `file_too_large` | 文件太大 |
| 415 | `unsupported_file_type` | 不支持的扩展名 |
| 503 | `s3_connection_failed` | 无法连接到 S3 服务 |
| 503 | `s3_permission_denied` | 无权限上传文件到 S3 |
| 503 | `s3_file_too_large` | 文件超出 S3 大小限制 |

### 文件预览相关

| HTTP状态码 | 错误码 | 描述 |
|-----------|--------|------|
| 403 | `file_access_denied` | 文件访问被拒绝 |
| 404 | `file_not_found` | 文件未找到或已被删除 |

### 终端用户相关

| HTTP状态码 | 错误码 | 描述 |
|-----------|--------|------|
| 404 | `end_user_not_found` | 终端用户不存在 |

### 对话变量相关

| HTTP状态码 | 错误码 | 描述 |
|-----------|--------|------|
| 400 | `Type mismatch` | 值类型与变量的预期类型不匹配 |
| 404 | `conversation_not_exists` | 对话不存在 |
| 404 | `conversation_variable_not_exists` | 变量不存在 |

---

## 支持的传输方式

### 文件传递方式 (transfer_method)

| 值 | 描述 |
|----|------|
| `remote_url` | 远程文件地址 |
| `local_file` | 本地上传文件 |

### 支持的文件类型

| 类别 | 扩展名 |
|------|--------|
| **文档** | TXT, MD, MARKDOWN, MDX, PDF, HTML, XLSX, XLS, VTT, PROPERTIES, DOC, DOCX, CSV, EML, MSG, PPTX, PPT, XML, EPUB |
| **图片** | JPG, JPEG, PNG, GIF, WEBP, SVG |
| **音频** | MP3, M4A, WAV, WEBM, MPGA |
| **视频** | MP4, MOV, MPEG, WEBM |

### 音频转文字支持的格式

`mp3, mp4, mpeg, mpga, m4a, wav, webm`（文件大小限制：15MB）

---

> 📌 **提示**：本文档基于 Dify 自托管版本 (SELF_HOSTED) 的「访问 API」页面内容整理而成，应用 ID 为 `df9442f3-3e66-4dd9-8215-516e95685f73`。所有 API 端点以 `http://localhost/v1` 为基础路径，实际使用时请替换为您的 Dify 服务地址。
