/**
 * markdown-renderer 组件 — Markdown/代码块渲染
 *
 * Properties:
 *   content     {String}   Markdown 原始文本
 *   showCopyBtn {Boolean}  是否显示代码块复制按钮
 *   fontSize    {Number}   基础字号（rpx），默认 32
 *
 * 支持语法：
 *   - 标题 H1-H6
 *   - 粗体 **text**、斜体 *text*
 *   - 行内代码 `code`
 *   - 代码块 ```lang ... ```
 *   - 有序/无序列表
 *   - 引用块 > text
 *   - 链接 [text](url)
 *   - 图片 ![alt](url)
 *   - 分割线 ---
 *   - 表格
 */

Component({
  properties: {
    content:     { type: String,  value: '' },
    showCopyBtn: { type: Boolean, value: true },
    fontSize:    { type: Number,  value: 32 },
  },

  data: {
    nodes: [],          // 解析后的节点树
    _prevContent: '',   // 缓存上次内容用于增量更新
  },

  observers: {
    content: function (val) {
      if (val !== this.data._prevContent) {
        this.data._prevContent = val;
        this._parse(val);
      }
    },
  },

  lifetimes: {
    attached() {
      this._parse(this.properties.content);
    },
  },

  methods: {
    /** 主解析入口 */
    _parse(text) {
      if (!text) {
        this.setData({ nodes: [] });
        return;
      }
      const lines = text.split('\n');
      const nodes = [];
      let i = 0;

      while (i < lines.length) {
        const line = lines[i];

        // 代码块
        if (line.trim().startsWith('```')) {
          const lang = line.trim().slice(3).trim();
          const codeLines = [];
          i++;
          while (i < lines.length && !lines[i].trim().startsWith('```')) {
            codeLines.push(lines[i]);
            i++;
          }
          nodes.push({
            type: 'code-block',
            lang: lang || 'text',
            code: codeLines.join('\n'),
          });
          i++; // 跳过结束 ```
          continue;
        }

        // 空行
        if (!line.trim()) {
          i++;
          continue;
        }

        // 标题
        const headingMatch = line.match(/^(#{1,6})\s+(.+)/);
        if (headingMatch) {
          nodes.push({
            type: 'heading',
            level: headingMatch[1].length,
            text: this._parseInline(headingMatch[2]),
          });
          i++;
          continue;
        }

        // 分割线
        if (/^(-{3,}|\*{3,})$/.test(line.trim())) {
          nodes.push({ type: 'hr' });
          i++;
          continue;
        }

        // 引用块
        if (line.startsWith('> ')) {
          const quoteLines = [];
          while (i < lines.length && lines[i].startsWith('> ')) {
            quoteLines.push(lines[i].slice(2));
            i++;
          }
          nodes.push({
            type: 'blockquote',
            text: this._parseInline(quoteLines.join('\n')),
          });
          continue;
        }

        // 无序列表
        if (/^[-*+]\s+/.test(line)) {
          const listItems = [];
          while (i < lines.length && /^[-*+]\s+/.test(lines[i])) {
            listItems.push(this._parseInline(lines[i].replace(/^[-*+]\s+/, '')));
            i++;
          }
          nodes.push({ type: 'ul', items: listItems });
          continue;
        }

        // 有序列表
        if (/^\d+\.\s+/.test(line)) {
          const listItems = [];
          while (i < lines.length && /^\d+\.\s+/.test(lines[i])) {
            listItems.push(this._parseInline(lines[i].replace(/^\d+\.\s+/, '')));
            i++;
          }
          nodes.push({ type: 'ol', items: listItems });
          continue;
        }

        // 表格检测
        if (line.includes('|') && i + 1 < lines.length && lines[i + 1].includes('---')) {
          const tableData = this._parseTable(lines, i);
          nodes.push({ type: 'table', ...tableData });
          i = tableData.endIndex;
          continue;
        }

        // 普通段落
        const paraLines = [];
        while (i < lines.length && lines[i].trim() && !this._isSpecialLine(lines[i])) {
          paraLines.push(lines[i]);
          i++;
        }
        if (paraLines.length > 0) {
          nodes.push({
            type: 'paragraph',
            text: this._parseInline(paraLines.join('\n')),
          });
        }
      }

      this.setData({ nodes });
    },

    /** 判断是否为特殊行（标题、列表等起始行） */
    _isSpecialLine(line) {
      return /^(#{1,6}\s|```|-{3,}|\*{3,}|>\s|[-*+]\s|\d+\.\s)/.test(line) || line.includes('|');
    },

    /** 解析表格 */
    _parseTable(lines, start) {
      const headerLine = lines[start];
      const headers = headerLine.split('|').map(h => h.trim()).filter(Boolean);
      let i = start + 2; // 跳过分隔行
      const rows = [];
      while (i < lines.length && lines[i].includes('|')) {
        const cells = lines[i].split('|').map(c => c.trim()).filter(Boolean);
        rows.push(cells);
        i++;
      }
      return { headers, rows, endIndex: i };
    },

    /** 解析行内元素（粗体、斜体、代码、链接、图片） */
    _parseInline(text) {
      if (!text) return '';
      // 转义 HTML
      let result = text
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;');

      // 行内代码 `code`
      result = result.replace(/`([^`]+)`/g, '<text class="inline-code">$1</text>');

      // 图片 ![alt](url)
      result = result.replace(/!\[([^\]]*)\]\(([^)]+)\)/g,
        '<image src="$2" mode="widthFix" style="max-width:480rpx" />');

      // 链接 [text](url)
      result = result.replace(/\[([^\]]+)\]\(([^)]+)\)/g,
        '<text class="md-link" data-url="$2">$1</text>');

      // 粗体 **text**
      result = result.replace(/\*\*(.+?)\*\*/g, '<text class="md-bold">$1</text>');

      // 斜体 *text*
      result = result.replace(/\*(.+?)\*/g, '<text class="md-italic">$1</text>');

      return result;
    },

    /** 复制代码块内容 */
    handleCopyCode(e) {
      const code = e.currentTarget.dataset.code;
      wx.setClipboardData({
        data: code,
        success() {
          wx.showToast({ title: '已复制', icon: 'success' });
        },
      });
    },
  },
});
