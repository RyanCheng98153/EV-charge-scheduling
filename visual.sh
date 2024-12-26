python ./visual.py ./results/greedy/result_day1_greedy.json file
python ./visual.py ./results/greedy/result_day7_greedy.json file
echo "greedy"

for i in 1 10 100 500 1000
do
    python ./visual.py ./results/1day/result_day1_gene_$i.json 0 file
    python ./visual.py ./results/7day/result_day7_gene_$i.json 0 file
    echo "gene $i"
done