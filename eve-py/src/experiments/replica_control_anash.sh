#!/bin/bash 
> exetime_replica_control_anash.txt
cd ..

for i in `seq 2 $1`;
do
	python main.py a experiments/gifford_anash$i.rml -v> experiments/temp.txt
	#echo $i
	cat experiments/temp.txt
	Ptime=`cat experiments/temp.txt | grep 'Parser Performance' | awk '{print $4}'`
	Cstr=`cat experiments/temp.txt | grep 'Construction Performance' | awk '{print $5}'`
	PGstr=`cat experiments/temp.txt | grep 'PGSolver Performance' | awk '{print $4}'`
	EmC=`cat experiments/temp.txt | grep 'A-Nash performance' | awk '{print $4}'`
	GParS=`cat experiments/temp.txt | grep 'GPar states' | awk '{print $3}'`
	GParE=`cat experiments/temp.txt | grep 'GPar edges' | awk '{print $3}'`
	TTPGS=`cat experiments/temp.txt | grep 'Max TTPG states' | awk '{print $4}'`
	TTPGE=`cat experiments/temp.txt | grep 'Max TTPG edges' | awk '{print $4}'`
	Total=`cat experiments/temp.txt | grep 'Total performance' | awk '{print $4}'`

	echo "$i;$Ptime;$Cstr;$PGstr;$EmC;$GParS;$GParE;$TTPGS;$TTPGE;$Total " >> experiments/exetime_replica_control_anash.txt
done
