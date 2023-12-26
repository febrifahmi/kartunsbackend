import random, string


def getrandomstring(n):
    x = "".join(random.choices(string.ascii_letters + string.digits, k=n))
    return x
