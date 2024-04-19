#!/bin/bash

# Get a list of jobids from a file
jobids=$(cat jobids)

# Run sacct, sstat and squeue for each job id
for jobid in $jobids; do
   sacct --format=JobID,JobName,User,Partition,NodeList,NNodes,NCPUs,NTasks,State,Submit,Start,End,Timelimit,Elapsed,TotalCPU,CPUTime,UserCPU,SystemCPU,ReqMem,MaxRSS,MaxVMSize,ReqTRES,AllocTRES,TRESUsageInMax,TRESUsageInTot,TRESUsageOutTot,MaxDiskRead,MaxDiskWrite,MaxRSSNode,MaxRSSTask,MaxVMSizeNode,MaxVMSizeTask,MaxDiskReadNode,MaxDiskReadTask,MaxDiskWriteNode,MaxDiskWriteTask,Comment --parsable --noheader --delimiter=☃ -j $jobid >> sacct.txt

   sstat --format=JobID,NTasks,MaxRSS,MaxVMSize,TRESUsageInMax,TRESUsageInTot,TRESUsageOutTot,MaxDiskRead,MaxDiskWrite,MaxRSSNode,MaxRSSTask,MaxVMSizeNode,MaxVMSizeTask,MaxDiskReadNode,MaxDiskReadTask,MaxDiskWriteNode,MaxDiskWriteTask --parsable --noheader -a -j $jobid,$jobid.batch >> sstat.txt

   squeue --format="%i|%E;%R;%C" --noheader -a -j $jobid >> squeue.txt
done

## Dump the output of scontrol
scontrol show -o nodes > scontrol.txt
