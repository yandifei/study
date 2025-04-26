class DialogManager:
    def __init__(self, system_prompt):
        self.history = [{"role": "system", "content": system_prompt}]

    def add_message(self, role, content):
        self.history.append({"role": role, "content": content})

    def trim_history(self, max_tokens=512):
        current_length = sum(len(msg["content"]) for msg in self.history)
        while current_length > max_tokens and len(self.history) > 2:
            removed = self.history.pop(1)  # 保留system prompt和最新对话
            current_length -= len(removed["content"])