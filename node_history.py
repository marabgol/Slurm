#!/usr/bin/python

# Written by Majid Arabgol 
# Date 03/01/2021
# Version 0.1

# this script writes any changes ( status, IP)  of each nodes with timstamp to a file
# run:  tail -f node_history.txt to see the changes


import sys, os,datetime,time

Slurm_version = os.popen(" rpm -qi slurm |grep RPM ").read()
Slurm1 = Slurm_version.split( )[3].split(".")
Slurm2 = Slurm1[0].split('-')[1]
Slurm = Slurm2+"-"+Slurm1[1]+"-"+Slurm1[2]

Os_version = os.popen(" cat /etc/redhat-release ").read()  

hostname =  os.popen(" hostname ").read().split('\n')[0]
f = open("node_history.txt", "w")

stream1 = os.popen(" sinfo -N |grep hpc-pg0 ").read().split('\n')
L = len(stream1)
dict1 = {"hpc-pg0-"+str(i+1): [""]* L  for i in range(L-1)}
dict2 = {"hpc-pg0-"+str(i+1): [""]* L for i in range(len(stream1)-1)}
while True:
    time.sleep(2)
    date = str(datetime.datetime.now()).split()[1].split('.')[0]
    stream1 = os.popen(" sinfo -N |grep hpc-pg0 ").read().split('\n')     
    for sin in stream1:
        if sin.find('hpc-pg0') != -1 :
            sinfo = sin.split( )
            host = sinfo[0]
            partition = sinfo[2]
            stat = sinfo[3]
            stream2 =  os.popen(" scontrol show node " + host).read()

        for scon in stream2.split('\n'):
         
            if scon.find('NodeHostName') != -1 :
                IP = scon.split(" ")[4].split('=')[1]
                 
            if scon.find('State') != -1 :
                dict1[host][0]= IP 
                dict1[host][1]= scon.split(" ")[3].split('=')[1]
                dict1[host][2]= stat
                dict1[host][3]= partition
                dict1[host][4]= date 
        for key, value in dict1.items():
            if dict2[key][1] != dict1[key][1] or dict2[key][2] != dict1[key][2] or dict2[key][0] != dict1[key][0]:
                dict2[key][0] = dict1[key][0]
                dict2[key][1] = dict1[key][1]
                dict2[key][2] = dict1[key][2]
                dict2[key][3] = dict1[key][3]
                dict2[key][4] = dict1[key][4]
                f.write('{0:12}'.format(key))
                f.write('{0:15}'.format(dict2[key][0]))
                f.write('{0:30}'.format(dict2[key][1]))
                f.write('{0:15}'.format(dict2[key][2]))
                f.write('{0:15}'.format(dict2[key][3]))
                f.write('{0:15}'.format(dict2[key][4]))
                f.write('\n')
                f.flush()
