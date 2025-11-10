import timeit

# 准备测试数据
def prepare_list():
    return list(range(10000))

# 不同清空方法
def test_clear():
    lst = prepare_list()
    lst.clear()

def test_del_slice():
    lst = prepare_list()
    del lst[:]

def test_assign_empty():
    lst = prepare_list()
    lst = []

def test_assign_list():
    lst = prepare_list()
    lst = list()

def test_assign_none():
    lst = prepare_list()
    lst = None

# 性能测试
methods = [
    ("s.clear()", test_clear),
    ("del s[:]", test_del_slice),
    ("s = []", test_assign_empty),
    ("s = list()", test_assign_list),
    ("s = None", test_assign_none)
]

print("清空列表操作性能对比:")
print("-" * 50)

for name, func in methods:
    time_taken = timeit.timeit(func, number=10000)
    print(f"{name:15} {time_taken:.4f} 秒")