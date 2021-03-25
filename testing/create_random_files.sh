target=$1
size=$2

for i in {1..50}
do
    for byte in {1..1024}
    do
        echo $i >> "$target/recovery$i.txt"
    done
done
