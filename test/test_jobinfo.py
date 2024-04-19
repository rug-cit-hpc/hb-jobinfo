from collections import namedtuple

import importlib
import io
import os
import re
import pytest

# Location of test script
test_script_dir = os.path.dirname(os.path.realpath(__file__))

# Directory that contains the input files for the tests.
DATA_DIR = os.path.join(test_script_dir, 'data')
EXPECTED_OUTPUT_DIR = os.path.join(DATA_DIR, 'expected_output')
# Filenames of the input files.
SACCT_FILE = 'sacct.txt'
SSTAT_FILE = 'sstat.txt'
SQUEUE_FILE = 'squeue.txt'
SCONTROL_FILE = 'scontrol.txt'

jobinfo_loader = importlib.machinery.SourceFileLoader(
    'jobinfo', os.path.join(test_script_dir, '../jobinfo')
)
jobinfo = jobinfo_loader.load_module()

# Explicitly set debug
jobinfo.debug = False
# Set long output to test all options
jobinfo.long_output = True

# Structure to represent return values for subprocess and requests calls.
Subprocess = namedtuple('Subprocess', ['stdout'])
Request = namedtuple('Request', ['content'])

# GPU usage values for mocked call to Prometheus
GPU_USAGE_VALUES = b'[[0,"50"], [1,"100"]]'

def sacct_output(jobid):
    '''Mock call to sacct by reading from a file.'''

    with open(os.path.join(DATA_DIR, SACCT_FILE), 'rb') as sacct_file:
        sacct_lines = sacct_file.readlines()
    jobid_lines = [
        line for line in sacct_lines if line.split(b'\xe2\x98\x83')[0].split(b'.')[0] == jobid
    ]
    return Subprocess(stdout=jobid_lines)


def squeue_output(jobid):
    '''Mock call to squeue by reading from a file.'''
    with open(os.path.join(DATA_DIR, SQUEUE_FILE), 'r') as squeue_file:
        squeue_lines = squeue_file.read()

    squeue_line = re.search(f'{jobid}.*\n', squeue_lines)
    if not squeue_line:
       squeue_line = ''
    else:
       squeue_line = squeue_line.group(0).strip().split('|', 1)[1]
    return Subprocess(stdout=io.BytesIO(squeue_line.encode('UTF-8')))


def sstat_output(jobid):
    '''Mock call to sstat by reading from a file.'''
    with open(os.path.join(DATA_DIR, SSTAT_FILE), 'rb') as sstat_file:
        sstat_lines = sstat_file.readlines()

    jobid_lines = [
        line for line in sstat_lines
        # only select lines for which the first field matches jobid or jobid.batch
        if line.split(b'|')[0].decode() == jobid]
    return Subprocess(stdout=jobid_lines)


def scontrol_show_nodes_output(node):
    '''Mock call to scontrol by reading from a file.'''
    with open(os.path.join(DATA_DIR, SCONTROL_FILE), 'r') as nodes_file:
        nodes_lines = nodes_file.read()
    node_line = re.search(f'NodeName={node}.*\n', nodes_lines)
    if node_line:
       node_line = node_line.group(0).strip().encode('UTF-8')
    else:
       node_line=''.encode('UTF-8')
    return Subprocess(stdout=io.BytesIO(node_line))


def popen_side_effect(*args, **kwargs):
    '''
    Side effect function for mocking the call to subprocess.Popen.
    Depending on what Popen is calling, we redirect to the right function.
    '''
    popen_args = list(args[0])
    if popen_args[0] == b'sacct':
        return sacct_output(popen_args[-1])
    elif popen_args[0] == 'scontrol':
        return scontrol_show_nodes_output(popen_args[-1])
    elif popen_args[0] == 'squeue':
        return squeue_output(popen_args[-1])
    elif popen_args[0] == b'sstat':
        return sstat_output(popen_args[-1])


def find_all_jobids():
    '''Find all our test job ids in the sacct.txt file.'''
    jobids = []
    with open(os.path.join(DATA_DIR, SACCT_FILE), 'rb') as sacct_file:
        sacct = sacct_file.readlines()
        jobids = [line.split(b'\xe2\x98\x83', 1)[0].split(b'.')[0].decode() for line in sacct]
    # convert to set to remove duplicates
    return set(jobids)

# zip two lists to the same length adding blank lines to the shortest one
def zip_to_max_length(a , b):
    max_length = max(len(a), len(b))
    a.extend([''] * (max_length - len(a)))
    b.extend([''] * (max_length - len(b)))
    return zip(a,b)


@pytest.mark.parametrize('jobid', find_all_jobids())
def test_jobinfo(jobid, mocker,capsys):
    '''Test jobinfo on a given jobid.'''
    mocker.patch('subprocess.Popen', side_effect=popen_side_effect)
    mocker.patch('os.getuid', return_value=0)
    output_file_path = os.path.join(EXPECTED_OUTPUT_DIR, jobid)
    if os.path.isfile(output_file_path):
        with open(output_file_path, 'rb') as output_file:
            output_lines = output_file.readlines()
    else:
        output_lines = None
    jobinfo.main(jobid)
    captured_output = capsys.readouterr().out.encode('UTF-8')
    if output_lines:
       for current_line,stored_line in zip_to_max_length(captured_output.splitlines(), output_lines):
          assert  current_line.strip() == stored_line.strip()
    else:
       with open(output_file_path, 'wb') as output_file:
          output_file.write(captured_output)
