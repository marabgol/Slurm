#!/usr/bin/python

# Written by Majid Arabgol 
# Date 03/01/2021
# Version 0.1

# make execute this script and watch it :watch ./node_status.py
# It shows and refresh the status,parition of each node ( hpc* partition) 

import sys, os

Slurm_version = os.popen(" rpm -qi slurm |grep RPM ").read()
Slurm1 = Slurm_version.split( )[3].split(".")
Slurm2 = Slurm1[0].split('-')[1]
Slurm = Slurm2+"-"+Slurm1[1]+"-"+Slurm1[2]

Os_version = os.popen(" cat /etc/redhat-release ").read()  

hostname =  os.popen(" hostname ").read().split('\n')[0]
print ('\n {0:20}  {1:20}   {2:20}  '.format(hostname,Slurm,Os_version ))

stream1 = os.popen(" sinfo -N |grep hpc-pg0 ").read() 
for sin in stream1.split('\n'):
    if sin.find('hpc-pg0') != -1 :
        sinfo = sin.split( )
        host = sinfo[0]
        stat = sinfo[3]
        partition = sinfo[2]
        print ('{0:12}'.format(host)), 
        stream2 =  os.popen(" scontrol show node " + host).read()
        for scon in stream2.split('\n'):
            if scon.find('NodeHostName') != -1 :
                print ('{0:15}'.format(scon.split(" ")[4].split('=')[1])),
            if scon.find('State') != -1 :
                print ('{0:25}  {1:12} {2:12}'.format(  scon.split(" ")[3].split("=")[1],stat,partition))