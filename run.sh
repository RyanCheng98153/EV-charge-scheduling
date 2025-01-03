# python ./main.py --days 1 --mode simulate -n 1 -o ./results/greedy/result_day1_greedy.json
# python ./main.py --days 7 --mode simulate -n 1 -o ./results/greedy/result_day7_greedy.json

# for n in 1 10 100 500 1000
for n in 5000 10000 20000 
do
    python ./main.py --days 1 --mode genetic -n $n -o ./results/1day/result_day1_gene_$n.json
    python ./main.py --days 7 --mode genetic -n $n -o ./results/7day/result_day7_gene_$n.json
done