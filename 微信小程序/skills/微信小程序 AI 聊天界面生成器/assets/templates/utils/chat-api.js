/**
 * chat-api.js — AI 对话 API 封装
 *
 * 提供两种模式：
 *   1. MockAPI — 本地模拟，无需后端，适合原型开发和演示
 *   2. streamChat — SSE 流式对接真实后端（DeepSeek/OpenAI 兼容格式）
 *
 * 使用方式：
 *   const { MockAPI, streamChat } = require('../../utils/chat-api');
 */

// ==================== 配置 ====================

/** 真实 API 默认地址（DeepSeek API） */
const DEFAULT_API_ENDPOINT = 'https://api.deepseek.com/v1/chat/completions';

/** API Key（建议通过环境变量或后端代理管理，不要硬编码在前端） */
let API_KEY = '';

/**
 * 设置 API Key
 * @param {string} key
 */
function setApiKey(key) {
  API_KEY = key;
}

/**
 * 获取 API Key（优先从全局配置读取）
 */
function getApiKey() {
  return API_KEY || '';
}

// ==================== MockAPI ====================

/** 预置模拟回复 */
const MOCK_REPLIES = [
  '你好！我是 AI 助手，很高兴为你服务。\n\n我可以帮你：\n- 解答技术问题\n- 编写代码\n- 文本处理\n- 知识问答\n\n请问有什么可以帮你的？',
  '这是一个很好的问题！让我来为你详细解答。\n\n首先，我们需要理解核心概念。在计算机科学中，**算法**是解决特定问题的一系列步骤。\n\n以下是一个简单的示例：\n\n```javascript\nfunction fibonacci(n) {\n  if (n <= 1) return n;\n  return fibonacci(n - 1) + fibonacci(n - 2);\n}\n\nconsole.log(fibonacci(10)); // 输出: 55\n```\n\n> 提示：递归实现虽然简洁，但对于大数值可能存在性能问题，建议使用迭代或记忆化优化。\n\n希望这个解答对你有帮助！',
  '当然可以！以下是你要的代码实现：\n\n```python\ndef quick_sort(arr):\n    if len(arr) <= 1:\n        return arr\n    pivot = arr[len(arr) // 2]\n    left = [x for x in arr if x < pivot]\n    middle = [x for x in arr if x == pivot]\n    right = [x for x in arr if x > pivot]\n    return quick_sort(left) + middle + quick_sort(right)\n\n# 测试\ndata = [3, 6, 8, 10, 1, 2, 1]\nprint(quick_sort(data))  # [1, 1, 2, 3, 6, 8, 10]\n```\n\n这个实现的时间复杂度为 O(n log n)（平均情况），空间复杂度为 O(n)。',
  '让我帮你分析一下这个问题。\n\n| 方案 | 优点 | 缺点 | 适用场景 |\n|------|------|------|----------|\n| 方案 A | 实现简单 | 性能较低 | 小规模数据 |\n| 方案 B | 性能优秀 | 复杂度高 | 大规模并发 |\n| 方案 C | 平衡性好 | 维护成本中等 | 中等规模 |\n\n综合来看，我推荐**方案 B**，因为它在长期来看能更好地支撑业务增长。',
  '好的，我理解你的需求。以下是几点建议：\n\n1. **保持代码简洁**：遵循 KISS 原则（Keep It Simple, Stupid）\n2. **注重可读性**：代码是写给人看的，顺便能在机器上运行\n3. **合理的注释**：解释 **为什么** 这样做，而不是做了什么\n4. **持续重构**：小步快跑，定期优化\n\n如果你有具体的代码需要 review，欢迎分享给我！',
];

/**
 * 本地模拟 API
 * 模拟流式输出效果：逐 token 返回，模拟真实 AI 回复体验
 */
class MockAPI {
  constructor(options = {}) {
    this.delay = options.delay || 500;       // 首 token 延迟（ms）
    this.tokenDelay = options.tokenDelay || 30; // token 间延迟（ms）
  }

  /**
   * 发送消息（模拟流式）
   * @param {Array} messages - 对话上下文 [{role, content}]
   * @param {Function} onToken - 每个 token 回调
   * @param {Function} onDone - 完成回调
   * @param {Function} onError - 错误回调
   */
  async sendMessage(messages, onToken, onDone, onError) {
    try {
      // 模拟网络延迟
      await this._sleep(this.delay);

      // 随机选择一条回复
      const reply = MOCK_REPLIES[Math.floor(Math.random() * MOCK_REPLIES.length)];

      // 逐 token 输出（模拟流式效果）
      const tokens = this._tokenize(reply);
      for (const token of tokens) {
        await this._sleep(this.tokenDelay);
        if (typeof onToken === 'function') {
          onToken(token);
        }
      }

      if (typeof onDone === 'function') {
        onDone(reply);
      }
    } catch (e) {
      if (typeof onError === 'function') {
        onError(e);
      }
    }
  }

  /**
   * 将文本拆分为 token 序列（简单模拟：按字/词拆分）
   */
  _tokenize(text) {
    const tokens = [];
    // 中英文混合拆分：中文逐字，英文逐词+标点
    const regex = /([一-鿿])|([a-zA-Z]+)|(\d+)|(\n)|([^\S\n]+)|([^\w\s])/g;
    let match;
    while ((match = regex.exec(text)) !== null) {
      tokens.push(match[0]);
    }
    // 如果正则没有匹配到（极端情况），逐字拆分
    if (tokens.length === 0) {
      for (const char of text) {
        tokens.push(char);
      }
    }
    return tokens;
  }

  _sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
}

// ==================== 真实 API 流式请求 ====================

/**
 * SSE 流式请求（对接 DeepSeek / OpenAI 兼容 API）
 *
 * @param {Object} options
 * @param {string} options.endpoint  - API 地址
 * @param {Array}  options.messages  - 对话上下文
 * @param {Function} options.onToken - token 回调 (token: string)
 * @param {Function} options.onDone  - 完成回调
 * @param {Function} options.onError - 错误回调 (error: Error)
 */
function streamChat(options) {
  const {
    endpoint = DEFAULT_API_ENDPOINT,
    messages = [],
    model = 'deepseek-chat',
    onToken,
    onDone,
    onError,
  } = options;

  const apiKey = getApiKey();
  if (!apiKey && endpoint === DEFAULT_API_ENDPOINT) {
    if (typeof onError === 'function') {
      onError(new Error('请先调用 setApiKey() 设置 API Key'));
    }
    return;
  }

  // 微信小程序 wx.request 流式请求
  const requestTask = wx.request({
    url: endpoint,
    method: 'POST',
    enableChunked: true,  // 开启分块传输
    header: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${apiKey}`,
    },
    data: {
      model,
      messages,
      stream: true,
    },
    success: (res) => {
      // 流式请求完成后检查
      if (res.statusCode !== 200) {
        if (typeof onError === 'function') {
          onError(new Error(`API 请求失败: ${res.statusCode}`));
        }
      }
    },
    fail: (err) => {
      if (typeof onError === 'function') {
        onError(new Error(`网络请求失败: ${err.errMsg}`));
      }
    },
  });

  // 监听分块数据
  let buffer = '';
  requestTask.onChunkReceived((res) => {
    try {
      // 将 ArrayBuffer 转为文本
      const chunk = this._arrayBufferToString(res.data);
      buffer += chunk;

      // 按行解析 SSE
      const lines = buffer.split('\n');
      // 最后一个可能是不完整的行，保留到下次
      buffer = lines.pop() || '';

      for (const line of lines) {
        const trimmed = line.trim();
        if (!trimmed || !trimmed.startsWith('data: ')) continue;

        const data = trimmed.slice(6); // 去掉 "data: " 前缀

        // [DONE] 标记
        if (data === '[DONE]') {
          if (typeof onDone === 'function') {
            onDone();
          }
          return;
        }

        try {
          const json = JSON.parse(data);
          const delta = json.choices?.[0]?.delta?.content;
          if (delta && typeof onToken === 'function') {
            onToken(delta);
          }
        } catch (e) {
          // 非 JSON 行或解析失败，跳过
        }
      }
    } catch (e) {
      // 解析异常，忽略
    }
  });
}

/**
 * ArrayBuffer → UTF-8 字符串
 */
function _arrayBufferToString(buffer) {
  // 微信小程序中 onChunkReceived 的 data 是 ArrayBuffer
  if (typeof buffer === 'string') return buffer;
  if (buffer instanceof ArrayBuffer) {
    const uint8 = new Uint8Array(buffer);
    let str = '';
    for (let i = 0; i < uint8.length; i++) {
      str += String.fromCharCode(uint8[i]);
    }
    return decodeURIComponent(escape(str));
  }
  return String(buffer);
}

// ==================== 导出 ====================

module.exports = {
  MockAPI,
  streamChat,
  setApiKey,
  getApiKey,
  DEFAULT_API_ENDPOINT,
};
