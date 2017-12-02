echo "How long does SVP take for different matrices sizes" >> timing-t2-medium.txt
# To create matrices ./fplll/fplll/latticegen u $i 10 >> matrices/matrix$i.txt
for i in {10..150..10}
  do
     #(time echo a) &>> foo 
     echo "We have $i dimensions" >> timing-t2-medium.txt
     (time ./fplll/fplll/fplll -a svp matrices/matrix$i.txt)  &>> timing-t2-medium.txt 
     
done



