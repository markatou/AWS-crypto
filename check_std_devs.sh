#!/bin/sh

std_dev=1
dim=128
mod=769
block=2

until [ $std_dev -gt 50 ]
do
	echo "Std dev: " $std_dev
	cvp_enum/bin/enumeration -n$dim -q$mod -s$std_dev -b$block -i"reduced" -p

	if [ -e ./solution_vector.dat ]
       	then
		break
	fi

	((std_dev++))
done
