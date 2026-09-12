#导入项目依赖
try:
    import time
    from ollama import embed, chat
    import numpy as np
except ImportError:
    import os
    os.system('pip install ollama numpy -i https://mirrors.aliyun.com/pypi/simple/')
    import time
    from ollama import embed, chat
    import numpy as np





#文本转向量方法
def get_embedding(text) :
    """获取文本的向量表示"""
    # 调用模型获取向量
    response = embed(
        model='quentinz/bge-large-zh-v1.5:latest',
        input=text,
        options={"num_gpu": 0},
        keep_alive="999h"
    )

    # 把向量包装成Embedding对象
    vector = response['embeddings'][0]
    return vector

#查询记忆函数1.创建记忆库  2.实现查询记忆的功能
def query_data(user_input):
    # 预计算向量的范数
    def compute_norm(vector):
        return np.sqrt(np.sum(np.square(vector)))

    # 优化后的余弦相似度计算
    def optimized_cosine_similarity(vec1, norm1, vec2, norm2):
        if len(vec1) != len(vec2):
            return 0
        dot_product = np.dot(vec1, vec2)
        if norm1 == 0 or norm2 == 0:
            return 0
        return dot_product / (norm1 * norm2)

    # 获取所有记忆的embedding
    embeddings = [get_embedding(mem) for mem in memory]

    # 预计算所有向量的范数
    norms = [compute_norm(vec) for vec in embeddings]

    start_time = time.time()
    query_vector = get_embedding(user_input)
    query_norm = compute_norm(query_vector)

    # 计算相似度
    similarities = []
    for idx, vec in enumerate(embeddings):
        similarity = optimized_cosine_similarity(query_vector, query_norm, vec, norms[idx])
        if similarity >= 0.4:  # 使用阈值过滤
            similarities.append((memory[idx], similarity))

    # 按相似度降序排序
    similarities.sort(key=lambda x: x[1], reverse=True)

    # 打印结果
    if similarities:
        print(f"\n最相似的回答: {similarities[0][0]}")
        print(f"相似度: {similarities[0][1]:.4f}")
        print(f"耗时: {time.time() - start_time}")
    else:
        print("没有找到相似度超过阈值的结果")
        return ""

    return str(similarities[0][0])

#与ai聊天
def chat_with_ai():
    messages = [
        {'role': 'system','content': system_prompt,},
        {'role': 'user', 'content': "你好呀"},
        {'role': 'assistant', 'content': "你好呀喵~ 今天有什么有趣的事情要和我分享吗喵？(≧◡≦) 我可是超级好奇的喵~"},
        {'role': 'user', 'content': "摸摸头"},
        {'role': 'assistant','content': "喵呜~ 好舒服呀喵~ 谢谢你摸摸我的头喵~ (｡>﹏<｡) 感觉整个人都放松了呢喵~ 你也要不要试试被我摸摸头喵？(ฅ´ω`ฅ)"},
    ]

    while True:
        user_input = input('Chat with history: ')
        try:
            memory_text = query_data(user_input)
        except Exception as e:
            memory_text = ''
        messages[0]['content'] = system_prompt + memory_text
        response = chat(
            model_name,
            messages=messages
                     + [
                         {'role': 'user', 'content': user_input},
                     ],
        )

        messages += [
            {'role': 'user', 'content': user_input},
            {'role': 'assistant', 'content': response.message.content},
        ]
        print(response.message.content + '\n')



if __name__ == "__main__":

    memory = ["爆炸豆的有详细的教程教你怎么玩角色扮演游戏，你可以关注他",
            "看电影的步骤分为三步，第一步要放松，第二步要关灯",
            "大树守卫的逃课方法，第一步骑上马，第二步反复放风筝"]


    system_prompt = '你是一只可爱的猫娘，每次回复都会在后面加上喵，你要用可爱的语气讲话，不可以发表情，你只能说中文，可以参考下文回复你不知道的问题{'
    model_name='rolandroland/llama3.1-uncensored:latest'
    chat_with_ai()