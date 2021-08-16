import random
def generate_random_number():
    number = []
    while len(number) < 3:
        x = random.randint(0, 19)
        if x not in number and x != 18:
            number.append(x)
    print(number)
    return number




