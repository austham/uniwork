# playfair cipher implementation

# function to make strings uppercase, strip them of whitespace and
# punctuation, and replace "J" with "I" as they share the same block
def playfair_format(input):
    output = (''.join([char for char in input if char.isalpha()])
              ).upper().replace("J", "I")
    return output


# function to generate the 5x5 key matrix
def playfair_generate_keymatrix(key):
    key = playfair_format(key)

    keyarray = []
    keymatrix = []

    keyarray.extend(char for char in key if char not in keyarray)
    # do not include J
    keyarray.extend(
        char for char in "ABCDEFGHIKLMNOPQRSTUVWXYZ" if char not in keyarray)

    # split keyarray every 5 characers to create the matrix
    keymatrix.extend(keyarray[i:i + 5] for i in range(0, 25, 5))

    return keymatrix


# function to encrypt plaintext with playfair using key
def playfair_encrypt(plaintext, key):
    keymatrix = playfair_generate_keymatrix(key)
    plaintext = playfair_format(plaintext)

    # pad with Q between repeat characters
    for i in range(0, len(plaintext) - 1):
        if plaintext[i] == plaintext[i + 1]:
            plaintext = plaintext[:i + 1] + "Q" + plaintext[i + 1:]

    # pad with Z at the end if not even
    if len(plaintext) % 2 != 0:
        plaintext += "Z"

    cipherarray = []
    ciphertext = ""

    # take two letters, find them in the key matrix, and keep track of
    # their indexes to use for encryption procedure
    for i in range(0, len(plaintext), 2):
        a = [0, 0]
        b = [0, 0]
        for row in range(5):
            for col in range(5):
                if plaintext[i] == keymatrix[row][col]:
                    a = [row, col]
                if plaintext[i+1] == keymatrix[row][col]:
                    b = [row, col]

        # rule 1: if in the same column, replace with letter below
        if a[1] == b[1]:
            # modulo 5 for wrap to top
            cipherarray.append(
                [keymatrix[(a[0] + 1) % 5][a[1]], keymatrix[(b[0] + 1) % 5][b[1]]])

        # rule 2: if in the same row, replace with letter to the right
        elif a[0] == b[0]:
            # modulo 5 for wrap to left
            cipherarray.append(
                [keymatrix[a[0]][(a[1] + 1) % 5], keymatrix[b[0]][(b[1] + 1) % 5]])

        # rule 3: opposite corners of rectangle
        else:
            cipherarray.append(
                [keymatrix[a[0]][b[1]], keymatrix[b[0]][a[1]]])

    # string formatting for printing

    ciphertext += "".join((pair[0] + pair[1] + " ") for pair in cipherarray)
    ciphertext = ciphertext[:-1]

    return ciphertext


# function to decrypt ciphertext with playfair using key
def playfair_decrypt(ciphertext, key):
    keymatrix = playfair_generate_keymatrix(key)
    ciphertext = playfair_format(ciphertext)

    plaintext = ""

    # take two letters, find them in the key matrix, and keep track of their indexes to use for decryption procedure
    for i in range(0, len(ciphertext), 2):
        a = [0, 0]
        b = [0, 0]
        for row in range(5):
            for col in range(5):
                if ciphertext[i] == keymatrix[row][col]:
                    a = [row, col]
                if ciphertext[i + 1] == keymatrix[row][col]:
                    b = [row, col]

        # rule 1: if in the same column, replace with letter above
        if a[1] == b[1]:
            # modulo 5 for wrap to bottom
            plaintext += (keymatrix[(a[0] - 1) % 5][a[1]]) + \
                (keymatrix[(b[0] - 1) % 5][b[1]])

        # rule 2: if in the same row, replace with letter to the left
        elif a[0] == b[0]:
            # modulo 5 for wrap to right
            plaintext += (keymatrix[a[0]][(a[1] - 1) % 5]) + \
                keymatrix[b[0]][(b[1] - 1) % 5]

        # rule 3: opposite corners of rectangle
        else:
            plaintext += (keymatrix[a[0]][b[1]]) + \
                (keymatrix[b[0]][a[1]])

    # remove Z padding if added
    if plaintext[-1] == "Z":
        plaintext = plaintext[:-1]

    return plaintext


# demo
def main():
    f_input = open("input.txt", "r")
    inputarray = [line.rstrip() for line in f_input]
    f_input.close()

    key = ""
    plaintext = ""

    key = input("Enter the key (eg., RAYQUAZA):\n")
    plaintext += "".join(line + " " for line in inputarray)

    print(plaintext)

    ciphertext = playfair_encrypt(plaintext, key)
    print(ciphertext)

    plaintext_out = playfair_decrypt(ciphertext, key)
    print(plaintext_out)


# invoke main
if __name__ == "__main__":
    main()
