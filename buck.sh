if [ ${2:+1} ]; then
    python3 bucklang.py $1 $2
elif [$1]; then 
    python3 bucklang.py $1
else
    python3 bucklang.py