echo "How long does SVP take for different matrices sizes\n" >> tim.txt

for i in {10..200..5}
  do
     #(time echo a) &>> foo 
     echo "We have $i dimensions" >> tim.txt
     (time ./fplll/fplll/latticegen u $i 10 | ./fplll/fplll/fplll -a svp)  &>> tim.txt 
done



