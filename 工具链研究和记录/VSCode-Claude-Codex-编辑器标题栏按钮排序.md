# VS Code：Claude 与 Codex 编辑器标题栏按钮排序

## 目标

将编辑器右上角按钮排为：

`其它按钮 → Claude → Codex → …`

> 这里修改的是两个扩展各自的 `package.json`，不是 VS Code 的 `settings.json`。

## 操作前

完全退出 VS Code，或完成修改后在命令面板执行：

`Developer: Reload Window`

## 扩展配置文件

当前安装版本的文件：

- Claude：`C:\Users\yandifei\.vscode\extensions\anthropic.claude-code-2.1.227-win32-x64\package.json`
- Codex：`C:\Users\yandifei\.vscode\extensions\openai.chatgpt-26.803.61601-win32-x64\package.json`

## Claude：排在 Codex 前

在 Claude 的 `package.json` 中找到：

```json
{
  "command": "claude-vscode.editor.openLast",
  "when": "!config.claudeCode.useTerminal",
  "group": "navigation"
}
```

改为：

```json
{
  "command": "claude-vscode.editor.openLast",
  "when": "!config.claudeCode.useTerminal",
  "group": "navigation@1000"
}
```

## Codex：紧挨 Claude，并排在更靠右的位置

在 Codex 的 `package.json` 中找到：

```json
{
  "command": "chatgpt.openSidebar",
  "group": "navigation"
}
```

改为：

```json
{
  "command": "chatgpt.openSidebar",
  "group": "navigation@1001"
}
```

## 排序规则

在同一个 `navigation` 组中，`@` 后的数字越大，按钮越靠右。

- `Claude: navigation@1000`
- `Codex: navigation@1001`

因此 Claude 与 Codex 会相邻，且 Codex 在 Claude 右边、`…` 左边。

若要交换二者位置，交换两个数字即可。

## 左侧活动栏显示 Codex 图标

### 目的

默认情况下，当前版本的 Codex 扩展会在支持“辅助侧栏”的 VS Code 中，把 Codex 注册到右侧辅助栏；因此左侧活动栏不显示 Codex 花结图标。

为了同时保留左侧入口、右侧入口，以及右上角白色 Codex 按钮，只修改 Codex 扩展的左侧显示条件，**不要禁用右侧注册，也不要改标题栏按钮配置**。

### 修改文件

`C:\Users\yandifei\.vscode\extensions\openai.chatgpt-26.803.61601-win32-x64\package.json`

在 `contributes → viewsContainers → activitybar` 中找到 Codex 容器：

```json
{
  "id": "codexViewContainer",
  "title": "Codex",
  "icon": "resources/blossom-white.svg",
  "when": "chatgpt.doesNotSupportSecondarySidebar"
}
```

删除末尾的 `when` 字段，改为：

```json
{
  "id": "codexViewContainer",
  "title": "Codex",
  "icon": "resources/blossom-white.svg"
}
```

然后在 `contributes → views → codexViewContainer` 中找到：

```json
{
  "type": "webview",
  "name": "Codex",
  "when": "chatgpt.doesNotSupportSecondarySidebar"
}
```

同样删除 `when` 字段：

```json
{
  "type": "webview",
  "name": "Codex"
}
```

### 必须保持不变的部分

不要修改下面两处右侧辅助栏注册；它们让右上角白色 Codex 花结继续按默认方式打开右侧 Codex：

```json
"when": "!chatgpt.doesNotSupportSecondarySidebar"
```

它们位于：

- `contributes → viewsContainers → secondarySidebar → codexSecondaryViewContainer`
- `contributes → views → codexSecondaryViewContainer`

### 图标仍未显示时

重载窗口后，在左侧活动栏空白处右键，确认 `Codex` 已勾选。VS Code 将其显示状态记录在自己的界面状态中；无需手动编辑状态数据库。

## 注意事项

- 修改后必须重载窗口或重启 VS Code 才会生效。
- 扩展升级会覆盖各自的 `package.json`；按钮顺序恢复默认后，按本笔记重新修改即可。
- 这是扩展安装目录内的自定义修改，不影响 VS Code 的通用用户设置。
