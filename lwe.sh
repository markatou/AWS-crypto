MODULUS=4093	# Coefficient modulus. Needs to be about 1.5 oom above S
N=6  		# Number of rows
M=10  		# Number of columns
S=4  		# Std dev of Gaussian sampler for the error
B=5		# BKZ block size

# cvp-enum/bin/lwesampler -n$N -m$M -s$S -q$MODULUS
echo "Running BKZ reduction with block size $b..."
cvp-enum/bin/reduction -b$B

echo "Copying samples_vector.dat to reduced_vector.dat..."
cp samples_vector.dat reduced_vector.dat

echo "Running the NTL enumeration on the reduced matrix and target vector..." 
cvp-enum/bin/enumeration -n$N -s$S -q$MODULUS -b$B -i"reduced" -e"ntl"

