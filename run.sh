for n in 1 10 100 500 1000
do
    python ./main.py --days 1 --mode genetic -n $n -o ./results/1day/result_day1_gene_$n.json
    python ./main.py --days 7 --mode genetic -n $n -o ./results/7day/result_day7_gene_$n.json
done