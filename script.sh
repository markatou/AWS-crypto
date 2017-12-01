echo "How long does SVP take for different matrices sizes" >> timing.txt
# To create matrices ./fplll/fplll/latticegen u $i 10 >> matrices/matrix$i.txt
for i in {10..150..5}
  do
     #(time echo a) &>> foo 
     echo "We have $i dimensions" >> timing.txt
     (time ./fplll/fplll/latticegen u $i 10 | ./fplll/fplll/fplll -a svp)  &>> timing.txt 
     
done



