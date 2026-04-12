nums = [1,2,3,4,5,6,7,8,9]
target = 20

L = 0
R = len(nums) - 1
res = -1
while L <= R:
    i = (L + R) // 2

    if target == nums[i]:
        res = i
        break
    elif target > nums[i]:
        L = i + 1
    else:
        R = i - 1
print(res)

