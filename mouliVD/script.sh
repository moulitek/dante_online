#!/bin/sh
make re > /dev/null
cd mouliVD/MazeComplexityEvalutation
make re
mv checkPerfect ../../
cd ../../

texte_failure_retvalue () { # take 4 argument : test name, good retvalue, retvalue got, description
        echo "[KO] [retvalue] $1 [/KO]"
        echo
        echo "[desc]"
        echo "$4"
        echo "[/desc]"
        echo
        echo "[expected]"
        echo "$2"
        echo "[/expected]"
        echo
        echo "[got]"
        echo "$3"
        echo "[/got]"
        echo
        echo "_____________________________________"
        echo
}

texte_failure_timout () { # take 4 argument : test name, good time, time got, description
        echo "[KO] [timeout] $1 [/KO]"
        echo
        echo "[desc]"
        echo "$4"
        echo "[/desc]"
        echo
        echo "[expected]"
        echo "$2s"
        echo "[/expected]"
        echo
        echo "[got]"
        echo "$3s"
        echo "[/got]"
        echo
        echo "_____________________________________"
        echo
}


texte_failure_segfault () { # take 4 argument : test name, good time, time got, description
        echo "[KO] [segfault] $1 [/KO]"
        echo
        echo "[desc]"
        echo "$4"
        echo "[/desc]"
        echo
        echo "[expected]"
        echo "$2"
        echo "[/expected]"
        echo
        echo "[got]"
        echo "$3"
        echo "[/got]"
        echo
        echo "_____________________________________"
        echo
}

texte_failure_badoutput () { # take 4 argument : test name, exepected, got, description
        echo "[KO] [badoutput] $1 [/KO]"
        echo
        echo "[desc]"
        echo "$4"
        echo "[/desc]"
        echo
        echo "[expected]"
        echo "$2"
        echo "[/expected]"
        echo
        echo "[got]"
        echo "$3"
        echo "[/got]"
        echo
        echo "_____________________________________"
        echo
}

texte_success () { # take 1 argument : test name
        echo "[OK] $1 [/OK]"
        echo
        echo "_____________________________________"
        echo
}

texte_success_time () { # take 1 argument : test name
        echo "[OK] $1 on $2s [/OK]"
        echo
        echo "_____________________________________"
        echo
}

texte_category_test () { # take 1 argument : category name can take description
        echo "[#] $1 [/#]"
        echo
        echo "[desc]"
        echo "$2"
        echo "[/desc]"
}

texte_sequence_test () { # take 1 argument : sequence name can take description
        echo "[##] $1 [/##]"
        echo
        echo "[desc]"
        echo "$2"
        echo "[/desc]"
        echo
}

texte_no_bin () { # take 1 argument : test name
        echo "[KO] [bin] $1 [/KO]"
        echo
}

ret=0

test_expect_success () {
        DATE='/bin/date'
        BEFORE=$($DATE +'%s')
        timeout 60s ./generator/generator ${1} ${2} > res
        ret1=$?
        AFTER=$($DATE +'%s')
        ELAPSED=$(($AFTER - $BEFORE))

        if [ $ret1 == 126 ]
        then
            texte_no_bin "$1 $2 $3 $4"
            ret=84
            return 0
        fi
        if [ $ret1 == 139 ]
        then
            texte_failure_segfault "$1 $2" "OK" "segfault"
            ret=84
            return 0
        fi
        if [ $ret1 == 124 ]
        then
            texte_failure_timout "$1 $2" "less than 60" "more than 60"
            ret=84
            return 0
        fi
        if [ $ret1 != 0 ]
        then
            texte_failure_retvalue "$1 $2" 0 $ret1
            ret=84
        fi
        if [ $ret1 == 0 ]
        then
            texte_success_time "$1 $2" $ELAPSED
        fi
        rm res
}

test_expect_error () {
        timeout 60s ./generator/generator ${1} ${2} ${3} ${4} > res
        ret1=$?

        if [ $ret1 == 126 ]
        then
            texte_no_bin "$1 $2 $3 $4"
            ret=84
            return 0
        fi
        if [ $ret1 == 139 ]
        then
            texte_failure_segfault "$1 $2" "OK" "segfault"
            ret=84
            return 0
        fi
        if [ $ret1 == 124 ]
        then
            texte_failure_timout "$1 $2" "less than 60" "more than 60"
            ret=84
            return 0
        fi
        if [ $ret1 == 84 ]
        then
            texte_success "$1 $2 $3 $4"
        else
            texte_failure_retvalue "$1 $2 $3 $4" 84 $ret1
            ret=84
        fi
}

test_expect_error_res () {
        timeout 60s ./solver/solver ${1} ${2} > /dev/null
        ret1=$(bash -c "echo $?")

        if [ $ret1 == 126 ]
        then
            texte_no_bin "$1 $2 $3 $4"
            ret=84
            return 0
        fi
        if [ $ret1 == 139 ]
        then
            texte_failure_segfault "$1 $2" "OK" "segfault"
            ret=84
            return 0
        fi
        if [ $ret1 == 124 ]
        then
            texte_failure_timout "$1 $2" "less than 60" "more than 60"
            ret=84
            return 0
        fi
        if [ $ret1 == 84 ]
        then
            texte_success "$1 $2 $3 $4"
        else
            texte_failure_retvalue "$1 $2 $3 $4" 84 $ret1 "$5"
            ret=84
        fi
}

texte_sequence_test "GENERATION"
texte_category_test "time"
test_expect_success 2 2
test_expect_success 1 40
test_expect_success 40 1
test_expect_success 1 1
test_expect_success 10 10
test_expect_success 100 100
test_expect_success 1000 1000
test_expect_success 10000 10000
test_expect_success 20000 20000
test_expect_success 30000 30000
test_expect_success 40000 40000
test_expect_success 50000 50000

texte_category_test "error handling"

test_expect_error 0 2
test_expect_error 2 0
test_expect_error 2 -0
test_expect_error -2 0
test_expect_error 2 -2
test_expect_error "a" 2
test_expect_error 2 "a"
test_expect_error "z" 2
test_expect_error 2 "z"
test_expect_error "2Ab" 0
test_expect_error "A" 2
test_expect_error 2
test_expect_error 2 2 "perfect" "notperfect"


texte_sequence_test "SOLVING - Error Handling"
search_dir="mouliVD/map/"
for entry in `ls $search_dir`; do
    texte_category_test "${entry}"
    for test in `ls $search_dir$entry`; do
        mine="${search_dir}${entry}/${test}"
        test_expect_error_res $mine
    done
done
texte_category_test "fake_file"
test_expect_error_res "fake_file" "" "" "" "a file that doesn't exist is given has argument"
texte_category_test "too many files"
test_expect_error_res $mine "too many file"


texte_sequence_test "LOOPING" "we use your generator to generate a maze and your solver to solve it. we only check ret value"
texte_category_test "medium one" "all test use perfect option for generator and test if they are perfect"

i=0
while [ $i -lt 201 ]
do
    w=`echo $(($RANDOM%200+20))`
    h=`echo $(($RANDOM%200+20))`
    flag=0
    ./generator/generator $w $h perfect > output.val
    ret1=$(bash -c "echo $?")
    ./solver/solver output.val > res.val
    ret2=$(bash -c "echo $?")
    ./checkPerfect output.val
    ret3=$(bash -c "echo $?")
    if [ $ret3 != 0 ]
    then
        texte_failure_badoutput "loop ($i) $w $h" "perfect" "imperfect"
        flag=1
        ret=84
    fi
    if [ $ret2 != 0 ] || [ $ret1 != 0 ] && [ $flag == 0 ]
    then
        texte_failure_retvalue "loop ($i) $w $h" 0 $ret1
        ret=84
    fi
    if [ $ret2 == 0 ] && [ $ret1 == 0 ] && [ $flag == 0 ]
    then
        texte_success "loop ($i) $w $h"
    fi

	i=`expr $i + 1`
	rm output.val
    rm res.val
done


texte_category_test "little one"

i=0
while [ $i -lt 101 ]
do
    w=`echo $(($RANDOM%10+1))`
    h=`echo $(($RANDOM%10+1))`
    ./generator/generator $w $h > output.val
    ret1=$(bash -c "echo $?")
    ./solver/solver output.val > res.val
    ret2=$(bash -c "echo $?")
    if [ $ret2 != 0 ] || [ $ret1 != 0 ]
    then
        texte_failure_retvalue "loop ($i) $w $h" 0 $ret1
        ret=84
    fi
    if [ $ret2 == 0 ] && [ $ret1 == 0 ]
    then
        texte_success "loop ($i) $w $h"
    fi
	i=`expr $i + 1`
	rm output.val
    rm res.val
done

make fclean > /dev/null
exit $ret
