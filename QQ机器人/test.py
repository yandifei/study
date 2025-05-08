from time import sleep
from deepseek_conversation_engine import DeepseekConversationEngine
deepseek = DeepseekConversationEngine("专属猫娘")  # 实例化对象(设置人设为专属猫娘)编程教师

# deepseek.set_stream(True)  # 设置流式输出
# while True:
#     print(f"\033[91m{deepseek.dialog_history}\033[0m")
#     deepseek.ask(input("我："))

function_map = {
    "模型切换": [lambda: deepseek.switch_model(True),lambda: "已切换至V3模型" if deepseek.model_choice == "deepseek-chat" else "已切换至R1模型", "切换中途发生异常"],
}
# print("已切换至V3模型" if deepseek.model_choice == "deepseek-chat" else "已切换至R1模型")
# function = function_map["模型切换"][0]
# function()
# print(deepseek.model_choice)
# print(function_map["模型切换"][1])
# print("已切换至V3模型" if deepseek.model_choice == "deepseek-chat" else "已切换至R1模型")
# print(deepseek.model_choice)
# print(type(deepseek.switch_model))
# print(type(function_map["模型切换"][1]))
# # function = function_map["模型切换"][1]
# if isinstance(function_map["模型切换"][1],):  # 如果是字符串
#     print(1)

def a():
    pass
print(type(a))
if isinstance(a(),填什么):  # 如果是函数
    print(1)

