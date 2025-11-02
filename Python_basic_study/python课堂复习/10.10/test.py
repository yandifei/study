# sorted([4,5,2,7].extend([3,6]))
# print(list1)
# 第二题
li_num1=[4,5,2,7]
li_num2=[3,6]
li_num1.extend(li_num2)
li_num1.sort(reverse=True)
print(li_num1)

# 第三题
tu_num1 = ('p', 'y', 't', ['0', 'n'])
list(tu_num1)[-1].append('h')
print(tu_num1)

# 第四题
tuple1 = ("jiangxl", 123, "python", 111, 22, 45, "abc")
list(tuple1).remove(22)
list(tuple1).remove(45)
print(tuple1)
