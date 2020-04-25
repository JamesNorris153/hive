#!/bin/sh

for i in 0 1 2 3 4 5 6 7 8 9
do
	python3 generate_transactions.py 100 10
	python3 mine_transactions.py $i PoW
	python3 mine_transactions.py $((10 - $i)) PoW
done
