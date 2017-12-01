PATH = "chall_0000_toy.txt"  # Path to challenge file
## This file contains the output of the parser that came
## with the original challenge files. 

"""
Currently hardcoded for challenge 0000 toy.
Reads in file and produces a matrix corresponding
to the first polynomial (called the first 'sample'
in the challenge file).
The matrix is a 2 dimensional array in row-major form.
"""
def poly_to_mat():
                
    f = open(PATH, 'r')
    print "file opened."
    ## First, parse the file to get the coefficients of the polynomial
    coeffs = []  ## This will store our coefficients
    while True:
        line = f.readline()
        if line == "samples {\n":  ## Start of 'a' polynomial
            break
    f.readline()  ## a {
    line = f.readline()  ## m:
    line = line[7:]  ## get rid of the ____m:_
    m = int(line)
    f.readline()  ## q:

    ## Now, we start looping over coefficient lines
    ## Currently hardcoded for a power of 2 cyclotomic
    for i in range(m/2):
        line = f.readline()
        line = line[8:]  ## remove ____xs:_  
        coeffs.append(int(line))
    f.close()
    print "file closed."
    
    ## Now, let's build the matrix
    output_mat = []

    ## Let's first build the bottom diagonal
    for i in range(m/2):  ## make each the first m/2 rows
        # print "making row" + str(i)
        cur_row = []
        for j in range(i, -1, -1):  ## put coefficients in row
            cur_row.append(coeffs[j])
        for k in range(i+1, m/2):  ## pad with zeros
            cur_row.append(0)
        output_mat.append(cur_row)
        
    ## Build the top diagonal by continuing the pattern
    ## but subtracting each row from the existing matrix
    for i in range(len(output_mat)):
        for k in range(m/2 - 1, i, -1):
            assert(output_mat[i][k] == 0)
            output_mat[i][k] += coeffs[k]
            
    return output_mat
        
        
print str(poly_to_mat())
