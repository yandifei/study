"""
给定一个整数数组nums和一个整数目标值target，请你
在该数组中找出和为目标值target的那两个整数，并返
回它们的数组下标。
"""
from typing import List


# def two_sum(nums: List[int], target: int):
#     res = []
#     for i, num1 in enumerate(nums):
#         for num2 in nums[i + 1:]:
#             if num1 + num2 == target:
#                 res.append([i, nums.index(num2)])
#     return res
#
# res = two_sum([2,7,11,15], 9)
# print(res)

# def two_sum(nums: List[int], target: int):
#     res = []
#     for i in range(len(nums)):
#         for j in range(i + 1, len(nums)):
#             if nums[i] + nums[j] == target:
#                 res.append([i, j])
#     return res

# def twoSum(nums, target):
a = {1: 132, 2:1120}
if 2 in a.keys():
    print(True)