MODULUS=4093	# Coefficient modulus. Needs to be about 1.5 oom above S
N=6  		# Number of rows
M=10  		# Number of columns
S=4  		# Std dev of Gaussian sampler for the error
B=5		# BKZ block size

cvp-enum/bin/lwesampler -n$N -m$M -s$S -q$MODULUS
cvp-enum/bin/reduction -b$B
cp samples_vector.dat reduced_vector.dat
cvp-enum/bin/enumeration -n$N -s$S -q$MODULUS -b$B -i"reduced" -p
echo "Diff"
diff solution_vector.dat samples_solution.dat
