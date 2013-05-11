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
declare -A metrics


function bootstrap {
	for dir in lexer parser analyzer codegen gcompile gexe
	do
		if [ ! -d $EXPECTED/$dir ]; then
			mkdir -p $EXPECTED/$dir
		fi

		if [ ! -d $OUTPUT/$dir ]; then
			mkdir -p $OUTPUT/$dir
		fi

		if [ ! -d $ERROR/$dir ]; then
			mkdir -p $ERROR/$dir
		fi

		metrics[${dir}_passed]=0
		metrics[${dir}_failed]=0
	done

	metrics[total_passed]=0
	metrics[total_failed]=0
}


function test_result {
	exit_status=$1
	phase=$2
	test_case=$3

	if [ $exit_status == 0 ]; then
		echo "$test_case passed $phase."
		((metrics[${phase}_passed]++))
		((metrics[total_passed]++))
	else
		echo "$test_case FAILED $phase."
		((metrics[${phase}_failed]++))
		((metrics[total_failed]++))
	fi
}


function print_metrics {
	echo
	echo -e "PHASE\tPASSED\tFAILED"
	for phase in lexer parser analyzer codegen gcompile gexe total
	do
		echo -e "$phase\t${metrics[${phase}_passed]}\t${metrics[${phase}_failed]}"
	done
}


function fast_test {
	unit=$1
	base=`basename $unit`
	class=${base/%.gr/}
	out=$class.out
	err=$class.err

	cd $FRONTEND

	bash gcompile $unit	$class 2>$ERROR/gcompile/$err
	exit_status=$?
	test_result $exit_status gcompile $base

	if [ $exit_status == 0 ]; then
		bash gexe $class > $OUTPUT/gexe/$out 2>$ERROR/gexe/$err
		exit_status=$?
		test_result $exit_status gexe $base

		if [ $exit_status == 0 ]; then
			cd $TESTS
			return
		fi
	fi

	# for phase in codegen analyzer parser lexer
	for phase in codegen analyzer lexer
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
	bootstrap

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

	print_metrics
}


function full_test {
	unit=$1
	base=`basename $unit`
	class=${base/%.gr/}
	out=$class.out
	err=$class.err

	cd $FRONTEND

	# for phase in lexer parser analyzer codegen
	for phase in lexer analyzer codegen
	do
		python $phase.py $unit > $OUTPUT/$phase/$out 2>$ERROR/$phase/$err
		test_result $? $phase $base
	done

	bash gcompile $unit	$class 2>$ERROR/gcompile/$err
	test_result $? gcompile $base

	bash gexe $class > $OUTPUT/gexe/$out 2>$ERROR/gexe/$err
	test_result $? gexe $base

	cd $TESTS
}


function full_all {
	bootstrap

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

	print_metrics
}


case "$1" in
	"fast" )		fast_all $2;;
	"full" )		full_all $2;;
	* )				echo "Usage: $0 fast|full <all|testID>";;
esac
