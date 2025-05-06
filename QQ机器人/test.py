from deepseek_conversation_engine import DeepseekConversationEngine
deepseek = DeepseekConversationEngine("专属猫娘")  # 实例化对象(设置人设为专属猫娘)编程教师

deepseek.set_stream(True)  # 设置流式输出
while True:
    print(f"\033[91m{deepseek.dialog_history}\033[0m")
    deepseek.ask(input("我："))