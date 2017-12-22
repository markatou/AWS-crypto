import sys
import argparse

PATH = "chall_000_00.txt"
S_PATH = "secret_000_00.txt"

OUTPUT_MAT = "samples_matrix.dat"
OUTPUT_VEC = "samples_vector.dat"
S_OUTPUT = "samples_solution.dat"

MAX_SAMPLES=2
TWEAK_FACTOR = 128

def checkPos(v):
    if not v: 
        raise argparse.ArgumentTypeError("Argument can't be NoneType")
    v = int(v)
    if v <=0:
        raise argparse.ArgumentTypeError("%s The value has to be a positive integer. " % v)
    return v

def transpose_mat(A):
	num_rows = len(A)
	num_cols = len(A[0])
	for row in A:
		assert(len(row) == num_cols)

	Output = []
	for col in range(num_cols):
		Output.append([])  ## creat a row for each column of A

	for i in range(num_rows):  # for each row
		for j in range(num_cols):
			Output[j].append(A[i][j])

	## Check
	for i in range(num_cols):
		for j in range(num_rows):
			assert(Output[i][j] == A[j][i])

	return Output

def parse_input_file():
    # This is the matrix representation of multiplication
    # by a mod x^(m/2) + 1, on the RIGHT.
    # This matrix will have
    # m/2 rows and (num samples) * m/2 columns
    a_mat = []
    # This will be a concatenation of all of our b samples
    b_vec = []

    q = -1
    m = -1

    num_samples = 0
    f = open(PATH, 'r')
    line = f.readline()
    while line:
        line = f.readline()
        if line == "samples {\n":
            num_samples += 1
            f.readline()  # a {
            line = f.readline()  # m:
            line = line[7:]  # get rid of the ____m:_
            m = int(line)
            line = f.readline()  # q:
            line = line[7:]
            q = int(line)

            coeffs = []  # This will store our coefficients
            a_current = []  # square matrix that represents our current sample polynomial
            b_current = []  # vector that represents our current b

            # Now, we start looping over coefficient lines
            # Currently hardcoded for a power of 2 cyclotomic
            for i in range(m / 2):
                line = f.readline()
                line = line[8:]  # remove ____xs:_
                assert(abs(int(line)) <= q / 2.0)
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
            if num_samples >= MAX_SAMPLES:
                break
    f.close()

    assert(len(a_mat) == m/2)

    for i in range(len(b_vec)):
        b_vec[i] = int(round(float(b_vec[i])))

    assert(m != -1)
    assert(q != -1)
    for i in range(len(a_mat)):
        for j in range(len(a_mat[i])):
            a_mat[i][j] = int(TWEAK_FACTOR * a_mat[i][j] % q)
    for i in range(len(b_vec)):
        b_vec[i] = int(b_vec[i] % q)

    rows = len(a_mat)
    assert(rows == m/2)

    cols = len(a_mat[0])
    for i in range(cols):
        a_mat.append([])
        for j in range(cols):
            if (i != j):
                a_mat[rows + i].append(0)
            else:
                a_mat[rows + i].append(q)

    for row in a_mat:
        assert(len(row) == cols)
    assert(len(a_mat) == rows + cols)
    return a_mat, b_vec	


def create_challenge_file():
    a, b = parse_input_file()

    # a = transpose_mat(a)

    f = open(OUTPUT_MAT, 'w')
    f.write("[")
    for row in a:
        f.write("[")
        f.write(str(row[0]))
        # for elem in row:
        for i in range(1, len(row)):
            f.write(" " + str(row[i]))
        f.write("]\n")
    f.write("]")
    f.close()

    f = open(OUTPUT_VEC, 'w')
    f.write("[")
    f.write(str(b[0]))
    for i in range(1, len(b)):
        f.write(" " + str(b[i]))
    f.write("]")

    f.close()

def create_secret_file():
    f = open(S_PATH, 'r')
    line = f.readline()

    coeffs = []
    
    while line:
        line = f.readline()
        if line == "s {\n":
            ## start of the secret
            line = f.readline()  # m:
            line = line[5:]  ## get rid of the __m:_
            m = int(line)
            line = f.readline()  # q:
            line = line[5:]
            q = int(line)
            for i in range(m/2):
                line = f.readline()
                if line == "  }\n":
                    break
                line = line[6:]  ## get rid of __xs:_
                coeffs.append(int(int(line) % q))
            break
    f.close()
    
    f = open(S_OUTPUT, 'w')

    f.write("[")
    f.write(str(coeffs[0]))
    for i in range(1, len(coeffs)):
        f.write(" " + str(coeffs[i]))
    f.write("]")

    f.close()


def main():
    # TWEAK_FACTOR = int(args.t)    ## could it really be that simple?
    # MAX_SAMPLES = int(args.s)

    # PATH = str(args.input_file)
    # OUTPUT_MAT = str(args.output_matrix)
    # OUTPUT_VEC = str(args.output_vector)
    # S_OUTPUT = str(args.output_secret)

    create_challenge_file()
    create_secret_file()

# parser = argparse.ArgumentParser()
# parser.add_argument("-t", "--tweak-factor", help="The tweak factor", type=checkPos)
# parser.add_argument("-s", help="The number of samples", type=checkPos)

# parser.add_argument("-im", "--input_file", 
#     help="Input challenge file. Should be challenge parser output.")
# parser.add_argument("-om", "--output_matrix", help="Output matrix file for CVP_ENUM." +
#     " Default is samples_matrix.dat")
# parser.add_argument("-ov", "--output_vector", help="Output vector file for CVP_ENUM." +
#     " Default is samples_vector.dat")

# parser.add_argument("-is", "--input_secret", 
#     help="Input secret file. Should be challenge parser output.")
# parser.add_argument("-os", "--output_secret", 
#     help="Output secret file for comparison to the CVP_ENUM solution file. " +
#         "Default is samples_solution.dat")
# args = parser.parse_args()


main()