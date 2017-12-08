PATH = "chall_000_00.txt"  # Path to challenge file
# PATH = "chall_0457_toy.txt"
## This file contains the output of the parser that came
## with the original challenge files.

OUTPUT = "my_challenge.txt"

"""
Currently hardcoded for challenge 0000 toy.
Reads in file and produces a matrix corresponding
to the first polynomial (called the first 'sample'
in the challenge file).
The matrix is a 2 dimensional array in row-major form.
"""
def poly_to_mat():

    ## Now, let's build the matrix
    a_mat = []   ## This is the matrix representation of multiplication
                 ## by a mod x^(m/2) + 1
                 ## This matrix will have m/2 rows and (num samples) * m/2 columns
    
    ## This is a vector of length m/2 that has the coefficients of b
    ## We will sum all of our b samples to get this vector
    b_vec = []

    f = open(PATH, 'r')
    ## First, parse the file to get the coefficients of the polynomial
    line = f.readline()
    while line:
        line = f.readline()
        if line == "samples {\n":  ## Start of 'a' polynomial            
            f.readline()  ## a {
            line = f.readline()  ## m:
            line = line[7:]  ## get rid of the ____m:_
            m = int(line)
            f.readline()  ## q:

            coeffs = []  ## This will store our coefficients
            a_current = []   ## square matrix that represents our current sample polynomial
            b_current = []   ## vector that represents our current b

            ## Now, we start looping over coefficient lines
            ## Currently hardcoded for a power of 2 cyclotomic
            for i in range(m/2):
                line = f.readline()
                line = line[8:]  ## remove ____xs:_  
                coeffs.append(int(line))

            ## Let's first build the bottom diagonal
            for i in range(m/2):  ## make each the first m/2 rows
                # print "making row" + str(i)
                cur_row = []
                for j in range(i, -1, -1):  ## put coefficients in row
                    cur_row.append(coeffs[j])
                for k in range(i+1, m/2):  ## pad with zeros
                    cur_row.append(0)
                a_current.append(cur_row)
                
            ## Build the top diagonal by continuing the pattern
            ## but subtracting each row from the existing matrix
            for i in range(m/2):
                for k in range(m/2 - 1, i, -1):
                    assert(a_current[i][k] == 0)
                    a_current[i][k] -= coeffs[k]

            ## We've build the matrix for the polynomial a

            f.readline()  ## }
            f.readline()  ## b {
            f.readline()  ## m:
            f.readline()  ## q:

            for i in range(m/2):
                line = f.readline()
                if line == "  }\n":
                    break
                line = line[8:]
                b_current.append(line)

            ## Append each row of a_curr to the corresponding row of a_mat
            if (len(a_mat) == 0):
                a_mat = a_current
            else:
                for i in range(len(a_mat)):
                    for elem in a_current[i]:
                        a_mat[i].append(elem)
            assert(len(a_mat) == m/2)

            ## Add each element of b_current to b_vec
            if (len(b_vec) == 0):
                b_vec = b_current
            else:
                for i in range(len(b_vec)):
                    b_vec[i] += b_current[i]
            assert(len(b_vec) == m/2)

    f.close()

    for i in range(len(b_vec)):
        b_vec[i]= int(round(b_vec[i]))

    assert(len(a_mat) == len(b_vec))
    return a_mat, b_vec


def create_challenge_file():

    a, b = poly_to_mat()
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

# create_challenge_file()
