import random

# deffie-hellman key exchange implementation

def is_prime(n: int):    
    return any([i for i in range(2, n) if n % i == 0])


def diffie_hellman_exchange(p: int, g: int):

    if not is_prime(p):
        raise ValueError("p must be prime")

    # Alice picks a secret number between 1 and p-1
    sa = random.randint(1, p - 1)
    print("Chose SA: ", sa)

    # Bob picks a secret number between 1 and p-1
    sb = random.randint(1, p - 1)
    print("Chose SB: ", sb)

    # TA = g^a mod p
    ta = pow(g, sa, p)
    print("TA: ", ta)

    # TB = g^b mod p
    tb = pow(g, sb, p)
    print("TB: ", tb)

    # calculate the shared secret key
    key1 = pow(tb, sa, p)
    key2 = pow(ta, sb, p)
    print("Secret key: ", key1)
    print("Keys match: ", key1 == key2)


def main():
    p, g = [int(c) for c in input("Enter two numbers \"p g\": ").split(" ")]
    diffie_hellman_exchange(p, g)


if __name__ == '__main__':
    main()
