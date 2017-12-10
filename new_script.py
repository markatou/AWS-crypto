PATH = "chall_457_00.txt"

OUTPUT = "my_challenge.txt"


def parse_input_file():
    # This is the matrix representation of multiplication
    # by a mod x^(m/2) + 1, on the RIGHT.
    # This matrix will have
    # m/2 rows and (num samples) * m/2 columns
    a_mat = []
    # This will be a concatenation of all of our b samples
    b_vec = []

    f = open(PATH, 'r')
    line = f.readline()
    while line:
        line = f.readline()
        if line == "samples {\n":
            f.readline()  # a {
            line = f.readline()  # m:
            line = line[7:]  # get rid of the ____m:_
            m = int(line)
            line = f.readline()  # q:
            line = line[7:]
            q = float(line)

            coeffs = []  # This will store our coefficients
            a_current = []  # square matrix that represents our current sample polynomial
            b_current = []  # vector that represents our current b

            # Now, we start looping over coefficient lines
            # Currently hardcoded for a power of 2 cyclotomic
            for i in range(m / 2):
                line = f.readline()
                line = line[8:]  # remove ____xs:_
                assert(abs(int(line)) < q / 2.0)
                coeffs.append(int(line))

            # Let's start by building the upper triangle
            for i in range(m / 2):
                cur_row = []
                for j in range(i):
                    cur_row.append(0)
                for j in range(0, len(coeffs) - i):
                    cur_row.append(coeffs[j])
                a_current.append(cur_row)

            # Now that we have an upper triangular matrix, let's
            # start filling in the zeros
            for i in range(m / 2):
                for j in range(i):
                    assert(a_current[i][j] == 0)
                    a_current[i][j] -= coeffs[-i + j]

            # Now, append a_current to a_mat
            if len(a_mat) == 0:
                a_mat = a_current
            else:
                for i in range(m / 2):
                    for j in range(m / 2):
                        a_mat[i].append(a_current[i][j])

            # We've build the matrix for the polynomial a
            # Now, let's move on to b

            f.readline()  # }
            f.readline()  # b {
            f.readline()  # m:
            f.readline()  # q:

            for i in range(m / 2):
                line = f.readline()
                if line == "  }\n":
                    break
                line = line[8:]
                assert(abs(float(line)) < q / 2)
                b_current.append(float(line))

            # Append each element of b_current to b_vec
            if (len(b_vec) == 0):
                b_vec = b_current
            else:
                for i in range(len(b_current)):
                    b_vec.append(b_current[i])
    f.close()

    assert(len(a_mat) == m/2)

    for i in range(len(b_vec)):
        b_vec[i] = int(round(float(b_vec[i])))

    return a_mat, b_vec


def create_challenge_file():
    a, b = parse_input_file()
    f = open(OUTPUT, 'w')
    f.write("[")
    for row in a:
        f.write("[")
        for elem in row:
            f.write(str(elem) + " ")
        f.write("]")
    f.write("]")

    f.write("[")
    for elem in b:
        f.write(str(elem) + " ")
    f.write("]")

    f.close()


def main():
    create_challenge_file()


main()
