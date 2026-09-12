"""
使用列表实现的好友管理系统，字典会更好
就不对字符串做校验了，注入风险之类的
1:添加好友
2:删除好友
3:备注好友
4:展示好友
5:退出
"""
# 使用""代替None防止转换陷阱
USER_INPUT: str
# 好友列表使用[]代替list()获取极致性能
friends_list = []
while True:
    print(f"{"=" * 20}欢迎使用好友管理系统{"=" * 20}")
    print("1:添加好友\n2:删除好友\n3:备注好友\n4:展示好友\n5:退出")
    # 录入用户输入的字符串
    USER_INPUT = input("请输入选项:")
    if USER_INPUT == "1":
        friends_list.append(input("请输入添加的好友名:"))
    elif USER_INPUT == "2":
        # 判断好友是否存在，存在才删除
        if (friend_name := input("请输入需要的好友名:")) not in friends_list:
            print("该好友不存在")
        else:
            friends_list.remove(friend_name)
    elif USER_INPUT == "3":
        # 判断是否存在该好友
        if not (friend_name := input("请输入需要备注的好友:")) in friends_list:
            print("该好友不存在")
        else:
            # 找到这个值的索引改变里面的元素，把这元素变成列表（极致节约空间）
            friends_list[friends_list.index(friend_name)] = [friend_name, input("请输入备注名：")]
    elif USER_INPUT == "4":
        for i in friends_list:
            # 如果它的类型是list代表有备注名(解析)
            if type(i) == list:
                print(f"{i[0]}\t备注名：{i[1]}")
            else:
                print(i)# 直接输出
    elif USER_INPUT == "5":
        break   # 直接退出
    else:
        print("\033[91m输入错误\033[0m")
