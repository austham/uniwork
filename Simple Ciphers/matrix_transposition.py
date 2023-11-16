# matrix transposition cipher implementation

# function to make strings lowercase, replace spaces with %
def matrix_transposition_format_text(text):
    output = text.lower().replace(" ", "%")
    return output


# function to format key to an array of int
def matrix_transposition_format_key(key):
    output = [(int(n)) for n in key.split(" ")]
    return output


# function to encrypt plaintext with matric transposition using key
def matrix_transposition_encrpyt(plaintext, key):
    plaintext = matrix_transposition_format_text(plaintext)
    key = matrix_transposition_format_key(key)

    ciphertext = ""
    matrix = []
    cols = max(key)

    # pad with % if needed
    while len(plaintext) % cols != 0:
        plaintext += "%"

    # split plaintext by no. of cols, unpack into chars, and add to matrix rows
    matrix.extend([*plaintext[i:i + cols]]
                  for i in range(0, len(plaintext), cols))

    # convert to string by column according to permutations defined in key
    for col in key:
        ciphertext += "".join(matrix[i][col-1] for i in range(0, len(matrix)))

    return ciphertext


# function to decrypt ciphertext with matric transposition using key
def matrix_transposition_decrpyt(ciphertext, key):
    ciphertext = matrix_transposition_format_text(ciphertext)
    key = matrix_transposition_format_key(key)

    cols = max(key)
    rows = int(len(ciphertext) / cols)

    # init empty matrix of zeros
    matrix = [[0 for col in range(0, cols)] for row in range(0, rows)]

    # unpack ciphertext into an array, fill into matrix by column according
    # to permutations defined in key
    cipherarray = [*ciphertext]
    for col in key:
        for row in range(0, rows):
            matrix[row][col - 1] = cipherarray.pop(0)

    # convert to string linearly and replace % with space
    plaintext = "".join("".join(matrix[row][col]
                        for col in range(cols)) for row in range(rows)).replace("%", " ")
    return plaintext


# demo
def main():
    f_input = open("input.txt", "r")
    inputarray = [line.rstrip() for line in f_input]
    f_input.close()

    key = ""
    plaintext = ""

    key = input("Enter the key seperated by spaces (eg., 5 10 6 3 ...):\n")
    plaintext += "".join(line + " " for line in inputarray)

    print(plaintext)

    ciphertext = matrix_transposition_encrpyt(plaintext, key)
    print(ciphertext)

    plaintext_out = matrix_transposition_decrpyt(ciphertext, key)
    print(plaintext_out)


# invoke main
if __name__ == "__main__":
    main()
