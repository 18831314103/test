def generate_numbers(n):
    for i in range(n):
        yield i

# 使用生成器
for number in generate_numbers(5):
    print(number)
