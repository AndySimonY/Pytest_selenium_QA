import random
def generate_random_number(count, length, elem):
    if count < length:
        number = []
        while len(number) < count:
            x = random.randint(0, length - 1)
            if x not in number and x != elem - 1:
                number.append(x)
        print(number)
        return number