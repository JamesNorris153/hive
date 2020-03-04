#!/bin/sh

for i in 0 1 2 3 4
do
	python3 generate_transactions.py 10 5
	sleep 10
	python3 mine_transactions.py $(($i % 5)) PoS2
done
