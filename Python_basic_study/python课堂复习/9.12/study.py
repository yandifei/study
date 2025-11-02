"""字符串拼接细节(是我目前用的，还是得对%熟悉，考试搞的是format)"""
name, age = "yandifei", 15
result = f"hello world {name} {age}"
print(result)
# 官方给的语法糖(3.8以上的版本才能用)
a = 1
b = 2
print(f"{a + b = }")


"""字符串替换细节"""
a = "asdfsfsfasfasfa"
# a改为b，且只替换1次（还有次数限制）
a.replace("a", "b", 1)

