MODULUS=4093	# Coefficient modulus. Needs to be about 1.5 oom above S
N=6  		# Number of rows
M=10  		# Number of columns
S=4  		# Std dev of Gaussian sampler for the error
B=5		# BKZ block size

bin/lwesampler -n$N -m$M -s$S -q$MODULUS
bin/reduction -b$B
cp samples_vector.dat reduced_vector.dat
bin/enumeration -n$N -s$S -q$MODULUS -b$B -i"reduced"
diff solution_vector.dat samples_solution.dat
