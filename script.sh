echo "How long does SVP take for different matrices sizes\n" >> text.txt

for i in {10..100..10}
  do
     #(time echo a) &>> foo 
     echo "We have $i dimensions" >> text.txt
     (time ./fplll/fplll/latticegen u $i 10 | ./fplll/fplll/fplll -a svp)  &>> text.txt 
done



