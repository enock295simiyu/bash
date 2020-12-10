#!/bin/bash

#check if number of arguments passed are exactly equal to 1
if [[ $# -ne 1 ]];then
	echo Arg1 should be subject name
	exit 0
fi

#Check if arg1 directory exists
subj_name=$1
if [[ ! -d $subj_name ]];then
	echo Survey for subject '"'$subj_name'"' not available.
	exit 0
fi

#calculate total time needed to complete survey
start_time=$(date +%s)
#calculate total number of characters entere by user
tot_chars=0
#Asking name of user
echo -n "Enter Your First Name : "
read fname
echo -n "Enter Your Last Name : "
read lname



echo -e "\n"Welcome $fname $lname, You will be showed 5 random question for subject '"'$subj_name'"', Please give all answers to complete survey.

#survery answer file
ans_fl=${lname}_${fname}_answers_${subj_name}.txt
#emptying answer file if exists
echo > $ans_fl
#Selecting 5 random question from subject directory
#ls subject directory , PIPE to, sort command with -R flag to random sort, then get top 5 file names and loop them
i=0
for ques_file in $(ls ./$subj_name | sort -R | head -5);do
	#calculate time needed to give answer
	ques_start_time=$(date +%s)

	i=$(expr $i + 1)
	echo
	echo Question $i | tee -a $ans_fl
	echo ------------- | tee -a $ans_fl
	cat ./$subj_name/$ques_file | tee -a $ans_fl
	echo | tee -a $ans_fl
	echo "Answer $i" >> $ans_fl
	echo ------------- >> $ans_fl
	read ans < /dev/tty
	echo $ans >> $ans_fl
	
	tot_chars=$(expr $tot_chars + $(echo -n $ans | wc -c))
	

	ques_end_time=$(date +%s)
	ques_time=$(expr $ques_end_time - $ques_start_time)
	echo -e "Answered in $ques_time (s).\n\n\n\n" >> $ans_fl


	
done




tot_chars=$(expr $(echo -n $fname$lname | wc -c) + $tot_chars)

end_time=$(date +%s)
run_time=$(expr $end_time - $start_time)
echo -e "\n\nTotal Characters input by user $tot_chars" >> $ans_fl
echo -e "Total time take to complete survey $run_time (s)" >> $ans_fl
echo FIN.