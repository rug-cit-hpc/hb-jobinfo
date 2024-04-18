# Test input files

This directory contains the input files for the tests, containing dumps of the output of `sacct`, `sstat`, `squeue`, and `scontrol` commands.

The following subsections explain which commands should be run on your cluster to generate the files.

## sacct
```
sacct --format=JobID,JobName,User,Partition,NodeList,NNodes,NCPUs,NTasks,State,Submit,Start,End,Timelimit,Elapsed,TotalCPU,CPUTime,UserCPU,SystemCPU,ReqMem,MaxRSS,MaxVMSize,ReqTRES,AllocTRES,TRESUsageInMax,TRESUsageInTot,TRESUsageOutTot,MaxDiskRead,MaxDiskWrite,MaxRSSNode,MaxRSSTask,MaxVMSizeNode,MaxVMSizeTask,MaxDiskReadNode,MaxDiskReadTask,MaxDiskWriteNode,MaxDiskWriteTask,Comment --parsable --noheader --delimiter=☃ -j <jobid> > sacct.txt
```

## sstat
```
sstat --format=JobID,NTasks,MaxRSS,MaxVMSize,TRESUsageInMax,TRESUsageInTot,TRESUsageOutTot,MaxDiskRead,MaxDiskWrite,MaxRSSNode,MaxRSSTask,MaxVMSizeNode,MaxVMSizeTask,MaxDiskReadNode,MaxDiskReadTask,MaxDiskWriteNode,MaxDiskWriteTask --parsable --noheader -a -j <jobid>,<jobid.batch> > sstat.txt
```

## scontrol
```
scontrol show -o nodes > scontrol.txt
```

## squeue
```
squeue --format="%i|%E;%R;%C" --noheader -a -j <jobid> > squeue.txt
```
N.B. Compared to the jobinfo script, this also adds the job id. The test script will cut it off before passing the data to jobinfo.

## Anonymise the files
As the files will contain names of users and nodes, you can anonymise them by running `anonymise.py`.
This will back up all the original files to `*.orig`, and create new ones with anonymised contents.
