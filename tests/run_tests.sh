#! /bin/bash

if [[ $PWD != *"/glang/tests" ]]; then
	echo "ERROR: Please run this script from glang/tests directory."
	exit 65
fi

if [ $# -ne 2 ]; then
	echo "Usage: $0 fast|full <all|testID>"
	exit 65
fi


ROOT="$PWD/../"
FRONTEND=$ROOT/frontend
TESTS=$ROOT/tests
UNITS=$TESTS/units
EXPECTED=$TESTS/expected
OUTPUT=$TESTS/output
ERROR=$TESTS/error


function test_result {
	if [ $1 == 0 ]; then
		echo "$2 passed $3."
	else
		echo "$2 FAILED $3."
	fi
}


function fast_test {
	unit=$1
	base=`basename $unit`
	out=${base/%.gr/.out}
	err=${base/%.gr/.err}

	cd $FRONTEND

	bash gcompile $unit	$base 2>$ERROR/gcompile/$err
	exit_status=$?
	test_result $exit_status gcompile $base

	if [ $exit_status == 0 ]; then
		cd $TESTS
		return
	fi

	for phase in codegen analyzer parser lexer
	do
		python $phase.py $unit > $OUTPUT/$phase/$out 2>$ERROR/$phase/$err
		exit_status=$?
		test_result $exit_status $phase $base

		if [ $exit_status == 0 ]; then
			cd $TESTS
			return
		fi
	done

	cd $TESTS
}


function fast_all {
	if [ $1 == "all" ]; then
		for unit in `find $UNITS -type f`
		do
			fast_test $unit
		done
	elif [ -e $UNITS/$1 ]; then
		fast_test $UNITS/$1
	else
		echo "Unknown test case $1"
	fi
}


function full_test {
	unit=$1
	base=`basename $unit`
	out=${base/%.gr/.out}
	err=${base/%.gr/.err}

	cd $FRONTEND

	for phase in lexer parser analyzer codegen
	do
		python $phase.py $unit > $OUTPUT/$phase/$out 2>$ERROR/$phase/$err
		test_result $? $phase $base
	done

	bash gcompile $unit	$base 2>$ERROR/gcompile/$err
	test_result $? gcompile $base

	cd $TESTS
}


function full_all {
	if [ $1 == "all" ]; then
		for unit in `find $UNITS -type f`
		do
			full_test $unit
		done
	elif [ -e $UNITS/$1 ]; then
		full_test $UNITS/$1
	else
		echo "Unknown test case $1"
	fi
}


case "$1" in
	"fast" )		fast_all $2;;
	"full" )		full_all $2;;
	* )				echo "Usage: $0 fast|full <all|testID>";;
esac
