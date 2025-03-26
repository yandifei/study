count = 0
for i in range(1, 51):
    for j in range(i + 1, 51):
        if i <= 7 and j <= 7:
            continue
        else:
            count += 1
print(count)
