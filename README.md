# hb-jobinfo
Tool for giving a quick overview of Slurm job statistics.

Inspired by https://github.com/birc-aeh/slurm-utils/blob/master/jobinfo
from Anders Halager  <aeh@birc.au.dk>

# Usage

```
jobinfo [-h] [-d] [-l] jobid`

collates job information from the 'sstat', 'sacct' and 'squeue' SLURM commands
to give a uniform interface for both current and historical jobs.

positional arguments:
  jobid        the jobid to query

optional arguments:
  -h, --help   show this help message and exit
  -d, --debug  Shows extra information about how the data is gathered
  -l, --long   Shows more information about the job
```

# Release notes:

## v1.0 - 2024-04-15

* First production version
