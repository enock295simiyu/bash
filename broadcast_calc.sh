#!/bin/bash

dec_to_bin(){
	#8 digit binary
	#convert decimal to binary string
	binary_str=$(echo "obase=2;$1" | bc)
	#pad 8 zeros to binary string
	printf %08d $binary_str
}

not_operator_bin(){
	#transposing 0 with 1 and 1 with 0
	echo $1 | tr 01 10
}

bin_to_dec(){
	#convert binary string to decimal
	echo $((2#$1))
}

dec_to_hex(){
	#convert int to hex
	hex_str=$(echo "obase=16;$1" | bc)
	echo 0x$hex_str
}

not_of_ip_octet(){
	#first convert ip octet value into binary
	x=$(dec_to_bin $1)
	#now apply not operator on this binary output
	x=$(not_operator_bin $x)
	#now convert binary string to int
	echo $(bin_to_dec $x)
}



#main program starts here

#check if minimum 2 args are given
if [[ $# -lt 2 ]];then
	echo "arg1 = IP ; arg2 = Subnet"
	exit 0
fi
ip=$1
subnet=$2

#check if ip is in correct format or not

num_of_dots=$(echo -n $ip | tr -dc "." | wc -c)
if [[ $num_of_dots -ne 3 ]];then
	echo "arg1 = IP ; is in incorrect format"
	exit 0
fi
#seprating all octets of ip
for i in $(seq 4);do
	ip_oct[$i]=$(echo $ip | cut -d . -f $i)
	if [[ ${ip_oct[$i]} -ge 0 ]] && [[ ${ip_oct[$i]} -le 255 ]];then
		true
	else
		echo "arg1 = IP ; is in incorrect format"
		exit 0
	fi
done

#find subnet is in which format

#get first 2 char of subnet
first_two_char=$(echo $subnet | cut -c -2)
num_of_dots=$(echo -n $subnet | tr -dc "." | wc -c)

if [[ $first_two_char == "0x" ]];then
	#subnet is in hex
	#remove 0x from hex
	subnet=$(echo $subnet | cut -c 3-)
	
	#get 4 octet from hex subnet
	hx=$(echo $subnet | cut -c 1-2)
	sub_oct[1]=$(echo $((16#$hx)))

	hx=$(echo $subnet | cut -c 3-4)
	sub_oct[2]=$(echo $((16#$hx)))

	hx=$(echo $subnet | cut -c 5-6)
	sub_oct[3]=$(echo $((16#$hx)))

	hx=$(echo $subnet | cut -c 7-8)
	sub_oct[4]=$(echo $((16#$hx)))

	

elif [[ $num_of_dots -eq 3 ]];then
	#subnet is IP format
	for i in $(seq 4);do
		sub_oct[$i]=$(echo $subnet | cut -d . -f $i)
	done

else
	#"subnet is CIDR format"
	for i in $(seq 4);do
		
		if [[ $subnet -ge 0 ]];then
			if [[ $subnet -gt 8 ]];then

				sub_oct[$i]=255
				subnet=$(expr $subnet - 8)
				
			else
				#repeat '1' n times
				last_oct_bin=$(printf "%-$(echo $subnet)s" | tr ' ' 1)
				# repeat 0 8-n times
				last_oct_bin=$last_oct_bin$(printf "%-$(echo $((8 - subnet)))s" | tr ' ' 0)
				sub_oct[$i]=$(bin_to_dec $last_oct_bin)
				subnet=0
			fi
		else
			sub_oct[$i]=0
		fi
	done

fi



#now we got ip and subnet octets in different variable

#to get broadcast address of an ip with given subnet
#do bitwise "not" of subnet bits
for i in $(seq 4);do
	sub_oct[$i]=$(not_of_ip_octet ${sub_oct[$i]})
done

#now with bitwise "not" of subnet, do bitwise "or" of ip and subnet

for i in $(seq 4);do
	broad_ip[$i]=$((ip_oct[$i] | sub_oct[$i]))
done


#print output

#check if arg3 is "hex"
if [[ $3 == "hex" ]];then
	echo -n 0x
	for i in $(seq 4);do
		echo -n $(echo "obase=16;${broad_ip[$i]}" | bc)
		
	done
else
	echo ${broad_ip[1]}.${broad_ip[2]}.${broad_ip[3]}.${broad_ip[4]}	
fi



