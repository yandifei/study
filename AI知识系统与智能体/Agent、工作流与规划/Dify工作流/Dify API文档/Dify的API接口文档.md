# 对话型应用 API

对话应用支持会话持久化，可将之前的聊天记录作为上下文进行回答，可适用于聊天/客服 AI 等。

### 基础 URL

```bash
http://localhost/v1
```

### 鉴权

Service API 使用 `API-Key` 进行鉴权。
**强烈建议开发者把 `API-Key` 放在后端存储，而非分享或者放在客户端存储，以免 `API-Key` 泄露，导致财产损失。**
所有 API 请求都应在 **`Authorization`** HTTP Header 中包含您的 `API-Key`，如下所示：

```bash
Authorization: Bearer {API_KEY}
```

---

## 发送对话消息

**POST** `/chat-messages`

创建会话消息。

### Request Body

- **query** (string) 用户输入/提问内容。
- **inputs** (object) 允许传入 App 定义的各变量值。默认 `{}`
- **response_mode** (string)
  - `streaming` 流式模式（推荐）。基于 SSE 实现类似打字机输出方式的流式返回。
  - `blocking` 阻塞模式，等待执行完毕后返回结果。（请求若流程较长可能会被中断）。
    *由于 Cloudflare 限制，请求会在 100 秒超时无返回后中断。*
    注：Agent 模式下不允许 blocking。
- **user** (string) 用户标识，用于定义终端用户的身份，方便检索、统计。由开发者定义规则，需保证用户标识在应用内唯一。Service API 不会共享 WebApp 创建的对话。
- **conversation_id** (string)（选填）会话 ID，需要基于之前的聊天记录继续对话，必须传之前消息的 conversation_id。
- **files** (array[object]) 文件列表，适用于传入文件结合文本理解并回答问题，仅当模型支持 Vision/Video 能力时可用。
  - `type` (string) 支持类型：`document` (TXT, MD, MARKDOWN, MDX, PDF, HTML, XLSX, XLS, VTT, PROPERTIES, DOC, DOCX, CSV, EML, MSG, PPTX, PPT, XML, EPUB), `image` (JPG, JPEG, PNG, GIF, WEBP, SVG), `audio` (MP3, M4A, WAV, WEBM, MPGA), `video` (MP4, MOV, MPEG, WEBM), `custom` (其他文件类型)
  - `transfer_method` (string) 传递方式: `remote_url` (文件地址), `local_file` (上传文件)
  - `url` 文件地址（仅当传递方式为 `remote_url` 时）
  - `upload_file_id` 上传文件 ID（仅当传递方式为 `local_file` 时）
- **auto_generate_name** (bool)（选填）自动生成标题，默认 `true`。若设置为 `false`，则可通过调用会话重命名接口并设置 `auto_generate` 为 `true` 实现异步生成标题。
- **workflow_id** (string)（选填）工作流ID，用于指定特定版本，如果不提供则使用默认的已发布版本。
  获取方式：在版本历史界面，点击每个版本条目右侧的复制图标即可复制完整的工作流 ID。
- **trace_id** (string)（选填）链路追踪ID。适用于与业务系统已有的trace组件打通，实现端到端分布式追踪等场景。如果未指定，系统会自动生成 `trace_id`。支持以下三种方式传递，具体优先级依次为：
  - Header：通过 HTTP Header `X-Trace-Id` 传递，优先级最高。
  - Query 参数：通过 URL 查询参数 `trace_id` 传递。
  - Request Body：通过请求体字段 `trace_id` 传递（即本字段）。

### Response

当 `response_mode` 为 `blocking` 时，返回 ChatCompletionResponse object。
当 `response_mode` 为 `streaming` 时，返回 ChunkChatCompletionResponse object 流式序列。

**ChatCompletionResponse** (application/json)

- `event` (string) 事件类型，固定为 `message`
- `task_id` (string) 任务 ID，用于请求跟踪和下方的停止响应接口
- `id` (string) 唯一ID
- `message_id` (string) 消息唯一 ID
- `conversation_id` (string) 会话 ID
- `mode` (string) App 模式，固定为 chat
- `answer` (string) 完整回复内容
- `metadata` (object) 元数据
  - `usage` (Usage) 模型用量信息
  - `retriever_resources` (array[RetrieverResource]) 引用和归属分段列表
- `created_at` (int) 消息创建时间戳，如：1705395332

**ChunkChatCompletionResponse** (text/event-stream)

每个流式块均为 data: 开头，块之间以 \n\n 即两个换行符分隔，如下所示：

```
data: {"event": "message", "task_id": "900bbd43-dc0b-4383-a372-aa6e6c414227", "id": "663c5084-a254-4040-8ad3-51f2a3c1a77c", "answer": "Hi", "created_at": 1705398420}\n\n
```

流式块中根据 event 不同，结构也不同：

- `event: message` LLM 返回文本块事件：完整文本以分块的方式输出。
  - `task_id`, `message_id`, `conversation_id`, `answer`, `created_at`
- `event: agent_message` Agent模式下返回文本块事件（仅Agent模式下使用）
  - 字段同上
- `event: agent_thought` Agent模式下有关Agent思考步骤的相关内容，涉及到工具调用（仅Agent模式下使用）
  - `id`, `task_id`, `message_id`, `position`, `thought`, `observation`, `tool`, `tool_input`, `created_at`, `message_files`, `conversation_id`
- `event: message_file` 文件事件，表示有新文件需要展示
  - `id`, `type`, `belongs_to`, `url`, `conversation_id`
- `event: message_end` 消息结束事件，收到此事件则代表流式返回结束。
  - `task_id`, `message_id`, `conversation_id`, `metadata`
- `event: tts_message` TTS 音频流事件，即语音合成输出。内容是Mp3格式的音频块，使用 base64 编码后的字符串，播放的时候直接解码即可。(开启自动播放才有此消息)
  - `task_id`, `message_id`, `audio`, `created_at`
- `event: tts_message_end` TTS 音频流结束事件，收到这个事件表示音频流返回结束。
  - `task_id`, `message_id`, `audio` (空字符串), `created_at`
- `event: message_replace` 消息内容替换事件。开启内容审核和审核输出内容时，若命中了审核条件，则会通过此事件替换消息内容为预设回复。
  - `task_id`, `message_id`, `conversation_id`, `answer`, `created_at`
- `event: error` 流式输出过程中出现的异常会以 stream event 形式输出，收到异常事件后即结束。
  - `task_id`, `message_id`, `status`, `code`, `message`
- `event: ping` 每 10s 一次的 ping 事件，保持连接存活。

**Errors**

- 404：对话不存在
- 400：`invalid_param`，传入参数异常
- 400：`app_unavailable`，App 配置不可用
- 400：`provider_not_initialize`，无可用的模型凭证配置
- 400：`provider_quota_exceeded`，模型调用额度不足
- 400：`model_currently_not_support`，当前模型不可用
- 400：`workflow_not_found`，指定的工作流版本未找到
- 400：`draft_workflow_error`，无法使用草稿工作流版本
- 400：`workflow_id_format_error`，工作流ID格式错误，需要UUID格式
- 400：`completion_request_error`，文本生成失败
- 500：服务内部异常

### 请求示例（阻塞模式）

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

### 阻塞模式响应示例

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
                "content": "\"Model\",\"Release Date\",\"Display Size\",\"Resolution\",\"Processor\",\"RAM\",\"Storage\",\"Camera\",\"Battery\",\"Operating System\"\n\"iPhone 13 Pro Max\",\"September 24, 2021\",\"6.7 inch\",\"1284 x 2778\",\"Hexa-core (2x3.23 GHz Avalanche + 4x1.82 GHz Blizzard)\",\"6 GB\",\"128, 256, 512 GB, 1TB\",\"12 MP\",\"4352 mAh\",\"iOS 15\""
            }
        ]
    },
    "created_at": 1705407629
}
```

### 流式模式响应示例（基础助手）

```
data: {"event": "message", "message_id": "5ad4cb98-f0c7-4085-b384-88c403be6290", "conversation_id": "45701982-8118-4bc5-8e9b-64562b4555f2", "answer": " I", "created_at": 1679586595}
data: {"event": "message", "message_id": "5ad4cb98-f0c7-4085-b384-88c403be6290", "conversation_id": "45701982-8118-4bc5-8e9b-64562b4555f2", "answer": "'m", "created_at": 1679586595}
...
data: {"event": "message_end", "id": "5e52ce04-874b-4d27-9045-b3bc80def685", "conversation_id": "45701982-8118-4bc5-8e9b-64562b4555f2", "metadata": {...}}
data: {"event": "tts_message", "conversation_id": "23dd85f3-1a41-4ea0-b7a9-062734ccfaf9", "message_id": "a8bdc41c-13b2-4c18-bfd9-054b9803038c", "created_at": 1721205487, "task_id": "3bf8a0bb-e73b-4690-9e66-4e429bad8ee7", "audio": "qqqq..."}
data: {"event": "tts_message_end", ...}
```

### 流式模式响应示例（智能助手）

```
data: {"event": "agent_thought", ...}
data: {"event": "agent_thought", "tool": "dalle3", "tool_input": "{\"dalle3\": {\"prompt\": \"cute Japanese anime girl...\"}}", ...}
data: {"event": "message_file", ...}
data: {"event": "agent_message", "answer": "I have created an image...", ...}
data: {"event": "message_end", ...}
```

---

## 上传文件

**POST** `/files/upload`

上传文件（目前仅支持图片）并在发送消息时使用，可实现图文多模态理解。
支持 png, jpg, jpeg, webp, gif 格式。
*上传的文件仅供当前终端用户使用。*

### Request Body (multipart/form-data)

- **file** (file) 要上传的文件。
- **user** (string) 用户标识，用于定义终端用户的身份，必须和发送消息接口传入 user 保持一致。Service API 不会共享 WebApp 创建的对话。

### Response

成功上传后，服务器会返回文件的 ID 和相关信息。

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

### 请求示例

```bash
curl -X POST 'http://localhost/v1/files/upload' \
--header 'Authorization: Bearer {api_key}' \
--form 'file=@localfile;type=image/[png|jpeg|jpg|webp|gif]' \
--form 'user=abc-123'
```

**Errors**

- 400：`no_file_uploaded`，必须提供文件
- 400：`too_many_files`，目前只接受一个文件
- 400：`unsupported_preview`，该文件不支持预览
- 400：`unsupported_estimate`，该文件不支持估算
- 413：`file_too_large`，文件太大
- 415：`unsupported_file_type`，不支持的扩展名，当前只接受文档类文件
- 503：`s3_connection_failed`，无法连接到 S3 服务
- 503：`s3_permission_denied`，无权限上传文件到 S3
- 503：`s3_file_too_large`，文件超出 S3 大小限制

---

## 获取终端用户

**GET** `/end-users/:end_user_id`

通过终端用户 ID 获取终端用户信息。

当其他 API 返回终端用户 ID（例如：上传文件接口返回的 `created_by`）时，可使用该接口查询对应的终端用户信息。

### Path 参数

- `end_user_id` (uuid) 必需，终端用户 ID。

### Response (EndUser)

```json
{
  "id": "6ad1ab0a-73ff-4ac1-b9e4-cdb312f71f13",
  "tenant_id": "8c0f3f3a-66b0-4b55-a0bf-8b8e0d6aee7d",
  "app_id": "6c8c3f41-2c6f-4e1b-8f4f-7f11c8f2ad2a",
  "type": "service_api",
  "external_user_id": "abc-123",
  "name": "Alice",
  "is_anonymous": false,
  "session_id": "abc-123",
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z"
}
```

### 请求示例

```bash
curl -X GET 'http://localhost/v1/end-users/6ad1ab0a-73ff-4ac1-b9e4-cdb312f71f13' \
--header 'Authorization: Bearer {api_key}'
```

**Errors**

- 404：`end_user_not_found`，终端用户不存在
- 500：内部服务器错误

---

## 文件预览

**GET** `/files/:file_id/preview`

预览或下载已上传的文件。此端点允许您访问先前通过文件上传 API 上传的文件。

*文件只能在属于请求应用程序的消息范围内访问。*

### Path 参数

- `file_id` (string) 必需，要预览的文件的唯一标识符，从文件上传 API 响应中获得。

### Query 参数

- `as_attachment` (boolean) 可选，是否强制将文件作为附件下载。默认为 `false`（在浏览器中预览）。

### Response

返回带有适当浏览器显示或下载标头的文件内容。

- `Content-Type` 根据文件 MIME 类型设置
- `Content-Length` 文件大小（以字节为单位，如果可用）
- `Content-Disposition` 如果 `as_attachment=true` 则设置为 "attachment"
- `Cache-Control` 用于性能的缓存标头
- `Accept-Ranges` 对于音频/视频文件设置为 "bytes"

### 请求示例

```bash
curl -X GET 'http://localhost/v1/files/72fa9618-8f89-4a37-9b33-7e1178a24a67/preview' \
--header 'Authorization: Bearer {api_key}'
```

### 作为附件下载

```bash
curl -X GET 'http://localhost/v1/files/72fa9618-8f89-4a37-9b33-7e1178a24a67/preview?as_attachment=true' \
--header 'Authorization: Bearer {api_key}' \
--output downloaded_file.png
```

**Errors**

- 400, `invalid_param`，参数输入异常
- 403, `file_access_denied`，文件访问被拒绝或文件不属于当前应用程序
- 404, `file_not_found`，文件未找到或已被删除
- 500，服务内部错误

---

## 停止响应

**POST** `/chat-messages/:task_id/stop`

仅支持流式模式。

### Path

- `task_id` (string) 任务 ID，可在流式返回 Chunk 中获取

### Request Body

- `user` (string) Required 用户标识，用于定义终端用户的身份，必须和发送消息接口传入 user 保持一致。API 无法访问 WebApp 创建的会话。

### Response

```json
{
  "result": "success"
}
```

### 请求示例

```bash
curl -X POST 'http://localhost/v1/chat-messages/:task_id/stop' \
-H 'Authorization: Bearer {api_key}' \
-H 'Content-Type: application/json' \
--data-raw '{ "user": "abc-123"}'
```

---

## 消息反馈（点赞）

**POST** `/messages/:message_id/feedbacks`

消息终端用户反馈、点赞，方便应用开发者优化输出预期。

### Path Params

- `message_id` (string) 消息 ID

### Request Body

- `rating` (string) 点赞 like, 点踩 dislike, 撤销点赞 null
- `user` (string) 用户标识，由开发者定义规则，需保证用户标识在应用内唯一。Service API 不会共享 WebApp 创建的对话。
- `content` (string) 消息反馈的具体信息。

### Response

```json
{
  "result": "success"
}
```

### 请求示例

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

## 获取APP的消息点赞和反馈

**GET** `/app/feedbacks`

获取应用的终端用户反馈、点赞。

### Query

- `page` (string)（选填）分页，默认值：1
- `limit` (string)（选填）每页数量，默认值：20

### Response

- `data` (List) 返回该APP的点赞、反馈列表。

### 请求示例

```bash
curl -X GET 'http://localhost/v1/app/feedbacks?page=1&limit=20'
```

### 响应示例

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

## 获取下一轮建议问题列表

**GET** `/messages/{message_id}/suggested`

获取下一轮建议问题列表。

### Path Params

- `message_id` (string) Message ID

### Query

- `user` (string) 用户标识，由开发者定义规则，需保证用户标识在应用内唯一。

### 请求示例

```bash
curl --location --request GET 'http://localhost/v1/messages/{message_id}/suggested?user=abc-123' \
--header 'Authorization: Bearer ENTER-YOUR-SECRET-KEY' \
--header 'Content-Type: application/json'
```

### Response

```json
{
  "result": "success",
  "data": ["a", "b", "c"]
}
```

---

## 获取会话历史消息

**GET** `/messages`

滚动加载形式返回历史聊天记录，第一页返回最新 `limit` 条，即：倒序返回。

### Query

- `conversation_id` (string) 会话 ID
- `user` (string) 用户标识，由开发者定义规则，需保证用户标识在应用内唯一。
- `first_id` (string) 当前页第一条聊天记录的 ID，默认 null
- `limit` (int) 一次请求返回多少条聊天记录，默认 20 条。

### Response

- `data` (array[object]) 消息列表
  - `id` (string) 消息 ID
  - `conversation_id` (string) 会话 ID
  - `inputs` (object) 用户输入参数。
  - `query` (string) 用户输入 / 提问内容。
  - `message_files` (array[object]) 消息文件
  - `answer` (string) 回答消息内容
  - `created_at` (timestamp) 创建时间
  - `feedback` (object) 反馈信息
  - `retriever_resources` (array[RetrieverResource]) 引用和归属分段列表
- `has_more` (bool) 是否存在下一页
- `limit` (int) 返回条数，若传入超过系统限制，返回系统限制数量

### 请求示例

```bash
curl -X GET 'http://localhost/v1/messages?user=abc-123&conversation_id=' \
--header 'Authorization: Bearer {api_key}'
```

### 响应示例（基础助手）

```json
{
"limit": 20,
"has_more": false,
"data": [
    {
        "id": "a076a87f-31e5-48dc-b452-0061adbbc922",
        "conversation_id": "cd78daf6-f9e4-4463-9ff2-54257230a0ce",
        "inputs": {
            "name": "dify"
        },
        "query": "iphone 13 pro",
        "answer": "The iPhone 13 Pro, released on September 24, 2021...",
        "message_files": [],
        "feedback": null,
        "retriever_resources": [...],
        "agent_thoughts": [],
        "created_at": 1705569239
    }
  ]
}
```

### 响应示例（智能助手）

```json
{
"limit": 20,
"has_more": false,
"data": [
    {
        "id": "d35e006c-7c4d-458f-9142-be4930abdf94",
        "conversation_id": "957c068b-f258-4f89-ba10-6e8a0361c457",
        "inputs": {},
        "query": "draw a cat",
        "answer": "I have generated an image of a cat for you...",
        "message_files": [...],
        "feedback": null,
        "retriever_resources": [],
        "created_at": 1705988187,
        "agent_thoughts": [...]
    }
  ]
}
```

---

## 获取会话列表

**GET** `/conversations`

获取当前用户的会话列表，默认返回最近的 20 条。

### Query

- `user` (string) 用户标识，由开发者定义规则，需保证用户标识在应用内唯一。
- `last_id` (string)（选填）当前页最后面一条记录的 ID，默认 null
- `limit` (int)（选填）一次请求返回多少条记录，默认 20 条，最大 100 条，最小 1 条。
- `sort_by` (string)（选填）排序字段，默认 -updated_at(按更新时间倒序排列)
  - 可选值：created_at, -created_at, updated_at, -updated_at
  - 字段前面的符号代表顺序或倒序，- 代表倒序

### Response

- `data` (array[object]) 会话列表
  - `id` (string) 会话 ID
  - `name` (string) 会话名称，默认将会话中用户最开始问题的截取。
  - `inputs` (object) 用户输入参数。
  - `status` (string) 会话状态
  - `introduction` (string) 开场白
  - `created_at` (timestamp) 创建时间
  - `updated_at` (timestamp) 更新时间
- `has_more` (bool)
- `limit` (int) 返回条数，若传入超过系统限制，返回系统限制数量

### 请求示例

```bash
curl -X GET 'http://localhost/v1/conversations?user=abc-123&last_id=&limit=20' \
--header 'Authorization: Bearer {api_key}'
```

### 响应示例

```json
{
  "limit": 20,
  "has_more": false,
  "data": [
    {
      "id": "10799fb8-64f7-4296-bbf7-b42bfbe0ae54",
      "name": "New chat",
      "inputs": {
          "book": "book",
          "myName": "Lucy"
      },
      "status": "normal",
      "created_at": 1679667915,
      "updated_at": 1679667915
    },
    ...
  ]
}
```

---

## 删除会话

**DELETE** `/conversations/:conversation_id`

删除会话。

### Path

- `conversation_id` (string) 会话 ID

### Request Body

- `user` (string) 用户标识，由开发者定义规则，需保证用户标识在应用内唯一。

### Response

```text
204 No Content
```

### 请求示例

```bash
curl -X DELETE 'http://localhost/v1/conversations/:conversation_id' \
--header 'Authorization: Bearer {api_key}' \
--header 'Content-Type: application/json' \
--data-raw '{
  "user": "abc-123"
}'
```

---

## 会话重命名

**POST** `/conversations/:conversation_id/name`

对会话进行重命名，会话名称用于显示在支持多会话的客户端上。

### Path

- `conversation_id` (string) 会话 ID

### Request Body

- `name` (string)（选填）名称，若 `auto_generate` 为 `true` 时，该参数可不传。
- `auto_generate` (bool)（选填）自动生成标题，默认 false。
- `user` (string) 用户标识，由开发者定义规则，需保证用户标识在应用内唯一。

### Response

```json
{
  "id": "34d511d5-56de-4f16-a997-57b379508443",
  "name": "hello",
  "inputs": {},
  "status": "normal",
  "introduction": "",
  "created_at": 1732731141,
  "updated_at": 1732734510
}
```

### 请求示例

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

## 获取对话变量

**GET** `/conversations/:conversation_id/variables`

从特定对话中检索变量。此端点对于提取对话过程中捕获的结构化数据非常有用。

### Path 参数

- `conversation_id` (string) 要从中检索变量的对话ID。

### Query 参数

- `user` (string) 用户标识符，由开发人员定义的规则，在应用程序内必须唯一。
- `last_id` (string)（选填）当前页最后面一条记录的 ID，默认 null
- `limit` (int)（选填）一次请求返回多少条记录，默认 20 条，最大 100 条，最小 1 条。

### Response

- `limit` (int) 每页项目数
- `has_more` (bool) 是否有更多项目
- `data` (array[object]) 变量列表
  - `id` (string) 变量 ID
  - `name` (string) 变量名称
  - `value_type` (string) 变量类型（字符串、数字、布尔等）
  - `value` (string) 变量值
  - `description` (string) 变量描述
  - `created_at` (int) 创建时间戳
  - `updated_at` (int) 最后更新时间戳

### 请求示例

```bash
curl -X GET 'http://localhost/v1/conversations/{conversation_id}/variables?user=abc-123' \
--header 'Authorization: Bearer {api_key}'
```

### 按变量名过滤

```bash
curl -X GET 'http://localhost/v1/conversations/{conversation_id}/variables?user=abc-123&variable_name=customer_name' \
--header 'Authorization: Bearer {api_key}'
```

### 响应示例

```json
{
  "limit": 100,
  "has_more": false,
  "data": [
    {
      "id": "variable-uuid-1",
      "name": "customer_name",
      "value_type": "string",
      "value": "John Doe",
      "description": "客户名称（从对话中提取）",
      "created_at": 1650000000000,
      "updated_at": 1650000000000
    },
    ...
  ]
}
```

---

## 更新对话变量

**PUT** `/conversations/:conversation_id/variables/:variable_id`

更新特定对话变量的值。此端点允许您修改在对话过程中捕获的变量值，同时保留其名称、类型和描述。

### Path 参数

- `conversation_id` (string) 包含要更新变量的对话ID。
- `variable_id` (string) 要更新的变量ID。

### 请求体

- `value` (any) 变量的新值。必须匹配变量的预期类型（字符串、数字、对象等）。
- `user` (string) 用户标识符，由开发人员定义的规则，在应用程序内必须唯一。

### Response

返回包含以下内容的更新变量对象：

- `id` (string) 变量ID
- `name` (string) 变量名称
- `value_type` (string) 变量类型（字符串、数字、对象等）
- `value` (any) 更新后的变量值
- `description` (string) 变量描述
- `created_at` (int) 创建时间戳
- `updated_at` (int) 最后更新时间戳

### 请求示例

```bash
curl -X PUT 'http://localhost/v1/conversations/{conversation_id}/variables/{variable_id}' \
--header 'Authorization: Bearer {api_key}' \
--header 'Content-Type: application/json' \
--data-raw '{
  "value": "Updated Value",
  "user": "abc-123"
}'
```

### 使用不同值类型更新

```bash
curl -X PUT 'http://localhost/v1/conversations/{conversation_id}/variables/{variable_id}' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer {api_key}' \
--data-raw '{
    "value": "新的字符串值",
    "user": "abc-123"
}'
```

### 响应示例

```json
{
  "id": "variable-uuid-1",
  "name": "customer_name",
  "value_type": "string",
  "value": "Updated Value",
  "description": "客户名称（从对话中提取）",
  "created_at": 1650000000000,
  "updated_at": 1650000001000
}
```

---

## 语音转文字

**POST** `/audio-to-text`

该接口需使用 `multipart/form-data` 进行请求。

### Request Body

- `file` (file) 语音文件。支持格式：`['mp3', 'mp4', 'mpeg', 'mpga', 'm4a', 'wav', 'webm']`。文件大小限制：15MB
- `user` (string) 用户标识，由开发者定义规则，需保证用户标识在应用内唯一。

### Response

- `text` (string) 输出文字

### 请求示例

```bash
curl -X POST 'http://localhost/v1/audio-to-text' \
--header 'Authorization: Bearer {api_key}' \
--form 'file=@localfile;type=audio/[mp3|mp4|mpeg|mpga|m4a|wav|webm]'
```

### 响应示例

```json
{
  "text": "hello"
}
```

---

## 文字转语音

**POST** `/text-to-audio`

文字转语音。

### Request Body

- `message_id` (str) Dify 生成的文本消息，那么直接传递生成的message-id 即可，后台会通过 message_id 查找相应的内容直接合成语音信息。如果同时传 message_id 和 text，优先使用 message_id。
- `text` (str) 语音生成内容。如果没有传 message-id 的话，则会使用这个字段的内容
- `user` (string) 用户标识，由开发者定义规则，需保证用户标识在应用内唯一。

### 请求示例

```bash
curl --location --request POST 'http://localhost/v1/text-to-audio' \
--header 'Authorization: Bearer ENTER-YOUR-SECRET-KEY' \
--form 'text=你好Dify;user=abc-123;message_id=5ad4cb98-f0c7-4085-b384-88c403be6290'
```

### Response Headers

```json
{
  "Content-Type": "audio/wav"
}
```

---

## 获取应用基本信息

**GET** `/info`

用于获取应用的基本信息

### Response

- `name` (string) 应用名称
- `description` (string) 应用描述
- `tags` (array[string]) 应用标签
- `mode` (string) 应用模式
- `author_name` (string) 作者名称

### 请求示例

```bash
curl -X GET 'http://localhost/v1/info' \
-H 'Authorization: Bearer {api_key}'
```

### 响应示例

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

## 获取应用参数

**GET** `/parameters`

用于进入页面一开始，获取功能开关、输入参数名称、类型及默认值等使用。

### Response

- `opening_statement` (string) 开场白
- `suggested_questions` (array[string]) 开场推荐问题列表
- `suggested_questions_after_answer` (object) 启用回答后给出推荐问题。
  - `enabled` (bool) 是否开启
- `speech_to_text` (object) 语音转文本
  - `enabled` (bool) 是否开启
- `text_to_speech` (object) 文本转语音
  - `enabled` (bool) 是否开启
  - `voice` (string) 语音类型
  - `language` (string) 语言
  - `autoPlay` (string) 自动播放
    - `enabled` 开启
    - `disabled` 关闭
- `retriever_resource` (object) 引用和归属
  - `enabled` (bool) 是否开启
- `annotation_reply` (object) 标注回复
  - `enabled` (bool) 是否开启
- `user_input_form` (array[object]) 用户输入表单配置
  - `text-input` (object) 文本输入控件
    - `label` (string) 控件展示标签名
    - `variable` (string) 控件 ID
    - `required` (bool) 是否必填
    - `default` (string) 默认值
  - `paragraph` (object) 段落文本输入控件
  - `select` (object) 下拉控件
    - `label` (string) 控件展示标签名
    - `variable` (string) 控件 ID
    - `required` (bool) 是否必填
    - `default` (string) 默认值
    - `options` (array[string]) 选项值
- `file_upload` (object) 文件上传配置
  - `document` (object) 文档设置
    - `enabled` (bool) 是否启用
    - `number_limits` (int) 文档数量限制，默认为 3
    - `transfer_methods` (array[string]) 传输方式列表：`remote_url`, `local_file`，必须选择一个。
  - `image` (object) 图片设置
    - `enabled` (bool) 是否启用
    - `number_limits` (int) 图片数量限制，默认为 3
    - `transfer_methods` (array[string]) 传输方式列表：`remote_url`, `local_file`，必须选择一个。
  - `audio` (object) 音频设置
    - `enabled` (bool) 是否启用
    - `number_limits` (int) 音频数量限制，默认为 3
    - `transfer_methods` (array[string]) 传输方式列表：`remote_url`, `local_file`，必须选择一个。
  - `video` (object) 视频设置
    - `enabled` (bool) 是否启用
    - `number_limits` (int) 视频数量限制，默认为 3
    - `transfer_methods` (array[string]) 传输方式列表：`remote_url`, `local_file`，必须选择一个。
  - `custom` (object) 自定义设置
    - `enabled` (bool) 是否启用
    - `number_limits` (int) 自定义数量限制，默认为 3
    - `transfer_methods` (array[string]) 传输方式列表：`remote_url`, `local_file`，必须选择一个。
- `system_parameters` (object) 系统参数
  - `file_size_limit` (int) 文档上传大小限制 (MB)
  - `image_file_size_limit` (int) 图片文件上传大小限制（MB）
  - `audio_file_size_limit` (int) 音频文件上传大小限制 (MB)
  - `video_file_size_limit` (int) 视频文件上传大小限制 (MB)

### 请求示例

```bash
curl -X GET 'http://localhost/v1/parameters' \
--header 'Authorization: Bearer {api_key}'
```

### 响应示例

```json
{
  "introduction": "nice to meet you",
  "user_input_form": [
    {
      "text-input": {
        "label": "a",
        "variable": "a",
        "required": true,
        "max_length": 48,
        "default": ""
      }
    }
  ],
  "file_upload": {
    "image": {
      "enabled": true,
      "number_limits": 3,
      "transfer_methods": ["remote_url", "local_file"]
    }
  },
  "system_parameters": {
    "file_size_limit": 15,
    "image_file_size_limit": 10,
    "audio_file_size_limit": 50,
    "video_file_size_limit": 100
  }
}
```

---

## 获取应用Meta信息

**GET** `/meta`

用于获取工具 icon

### Response

- `tool_icons` (object[string]) 工具图标
  - `工具名称` (string)
    - `icon` (object|string)
      - (object) 图标
        - `background` (string) hex 格式的背景色
        - `content` (string) emoji
      - (string) 图标 URL

### 请求示例

```bash
curl -X GET 'http://localhost/v1/meta' \
-H 'Authorization: Bearer {api_key}'
```

### 响应示例

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

## 获取应用 WebApp 设置

**GET** `/site`

用于获取应用的 WebApp 设置

### Response

- `title` (string) WebApp 名称
- `chat_color_theme` (string) 聊天颜色主题，hex 格式
- `chat_color_theme_inverted` (bool) 聊天颜色主题是否反转
- `icon_type` (string) 图标类型，`emoji`-表情，`image`-图片
- `icon` (string) 图标，如果是 `emoji` 类型，则是 emoji 表情符号，如果是 `image` 类型，则是图片 URL
- `icon_background` (string) hex 格式的背景色
- `icon_url` (string) 图标 URL
- `description` (string) 描述
- `copyright` (string) 版权信息
- `privacy_policy` (string) 隐私政策链接
- `custom_disclaimer` (string) 自定义免责声明
- `default_language` (string) 默认语言
- `show_workflow_steps` (bool) 是否显示工作流详情
- `use_icon_as_answer_icon` (bool) 是否使用 WebApp 图标替换聊天中的 🤖

### 请求示例

```bash
curl -X GET 'http://localhost/v1/site' \
-H 'Authorization: Bearer {api_key}'
```

### 响应示例

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