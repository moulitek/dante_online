#!/bin/sh

make re
d=10
i=0
while [ $i -lt 10000 ]
do
    w=`echo $(($RANDOM%1000+1))`
    h=`echo $(($RANDOM%1000+1))`
    echo "loop on $w $h"
    ./generator/generator $w $h > output.val
    ret1=$(bash -c "echo $?")
    ./solver/solver output.val > res.val
    ret2=$(bash -c "echo $?")
    if [ $ret2 != 0 ] || [ $ret1 != 0 ]
    then
        tput setaf 1 bold
        echo "    KO return value"
        tput init
        exit 84
    fi
	i=`expr $i + 1`
	rm output.val
    rm res.val
done
