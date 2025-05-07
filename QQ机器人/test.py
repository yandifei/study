from time import sleep
from deepseek_conversation_engine import DeepseekConversationEngine
deepseek = DeepseekConversationEngine("专属猫娘")  # 实例化对象(设置人设为专属猫娘)编程教师

# deepseek.set_stream(True)  # 设置流式输出
# while True:
#     print(f"\033[91m{deepseek.dialog_history}\033[0m")
#     deepseek.ask(input("我："))

function_map = {
    "模型切换": [lambda: deepseek.switch_model(True),"已切换至R1模型" if deepseek.model_choice == "deepseek-chat" else "已切换至V3模型", "切换中途发生异常"],
}
# print("已切换至V3模型" if deepseek.model_choice == "deepseek-chat" else "已切换至R1模型")
print(function_map["模型切换"][1])