#!/usr/bin/env bash
#written by  Sanu Adebo
#Check if file exist

file="test-dns.csv"
if [ -f $file ] 
then
    rm $file
fi

#recreate file
touch test-dns.csv
#get ec2 instances and save in csv file
aws ec2 describe-instances --filters  --query 'Reservations[].Instances[].[ [Tags[?Key==`Name`].Value][0][0],InstanceId,[Tags[?Key==`Group`].Value][0][0],[Tags[?Key==`SvrRole`].Value][0][0],PrivateIpAddress,PublicDnsName,Platform,PublicIpAddress ]' --output text > monthly_report_ec2.csv
private_ip=`cat monthly_report_ec2.csv  | awk -F'\t' '{ print $5 }'`

#get dns  names for private ip addresses
for i in $private_ip
do 
   host1=`host $i`
   if [ $? -eq 0 ]
   then
       echo $host1  | awk '{ print $5}' | grep -i org
       if [ $? -eq 0 ] 
       then
           echo $host1  | awk '{ print $5}' >> test-dns.csv
       else
           echo "None" >> test-dns.csv
       fi
   else
       echo "None"   >> test-dns.csv
   fi
done
#sed -i '1iPrivateDNS\t' test-dns.csv

echo " " | cat - test-dns.csv > test-dns-edit.csv
#paste monthly_report_ec2.csv test-dns.csv > monthly_report_ec2.csv

#echo "PrivateDNS" | cat - test-dns.csv
#gsed -i '1iName\tGroup\tPrivateIPAddress\tDNS\tPublic'  test.csv
#generate file headers
sed -i '1iName\tInstanceID\tGroup\tSvrRole\tPrivateIPAddress\tDNS\tOSType\tPublicIP\tPrivateDNSName' monthly_report_ec2.csv  

#awk -F '\t' '{ if($6 ~ "None") {print $1"\t"$2"\t"$3"\t"$4"\t"$5"\t""Linux""\t"$7} else {print $0} }' monthly_report_ec2.csv | aws s3 cp -  s3://tags-non-compliant/my_csv/$(date +%B)_report_ec2.csv
# generate OS type for Linux and Windows
awk -F '\t' '{ if($6 ~ "None") {print $1","$2","$3","$4","$5","$6",""Linux"","$8","$9}  }' monthly_report_ec2.csv 
awk -F '\t' '{ if($6 ~ "windows") {print $1","$2","$3","$4","$5","$6",""Windows"","$8",$9} }' monthly_report_ec2.csv  
# Merge the aws inventory and host file
paste monthly_report_ec2.csv test-dns-edit.csv  > monthly_ec2_dns.csv
#cat monthly_report_ec2.csv  | awk -F'\t' '{ print $5 }' 
