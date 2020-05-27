# Prompt
Write a program in a language of your choice that spawns 10 workers (threads, processes, actors, whatever), where each worker simultaneously searches a stream of random (or pseudo-random) data for the string 'FiCo', then informs the parent of the following data fields via some form of inter-process communication or shared data structure:

- elapsed time
- count of bytes read
- status

The parent collects the results of each worker (confined to a timeout, explained below) and writes a report to stdout for each worker sorted in descending order by [elapsed]: [elapsed] [byte_cnt] [status]

Where [elapsed] is the elapsed time for that worker in ms, [byte_cnt] is the number of random bytes read to find the target string and [status] should be one of {SUCCESS, TIMEOUT, FAILURE}. FAILURE should be reported for any error/exception of the worker and the specific error messages should go to stderr. TIMEOUT is reported if that worker exceeds a given time limit, where the program should support a command-line option for the timeout value that defaults to 60s. If the status is not SUCCESS, the [elapsed] and [byte_cnt] fields will be empty.

The parent should always write a record for each worker and the total elapsed time of the program should not exceed the timeout limit. If a timeout occurs for at least one worker, only those workers that could not complete in time should report TIMEOUT, other workers may have completed in time and should report SUCCESS. Note that the source of random bytes must be a stream such that a worker will continue indefinitely until the target string is found, or a timeout or exception occurs. A final line of output will show the average bytes read per time unit in a time unit of your choice where failed/timeout workers will not report stats. 11 lines of output total to stdout.

Please package your submission with tar or zip. The package must include a README with these instructions, a UNIX shell executable file (or instructions on how to build one) that runs your program and responds appropriately to -h, which gives instructions on running the program (including the timeout option).

# Running

```bash
$ cd  hatch-takehome
$ hatch-takehome/python worker.py -h
usage: worker.py [-h] [--timeout TIMEOUT] [--maxworkers MAXWORKERS]

Hatch Takehome Example

optional arguments:
  -h, --help            show this help message and exit
  --timeout TIMEOUT     Seconds until timeout. (Defaults 60s)
  --maxworkers MAXWORKERS
                        Maximum number of workers
```

# Queue 

```python
# Using syncronous queue to pass tuples from threads

queue.Queue (thread_number, time_elapsed, byte_counted, status)
```

# Sample

```bash
$ python worker.py
[Thread-0]: Started searching...
[Thread-0] Found FiCo after searching 16593 bytes 2.7950100000000004ms elapsed.
[Thread-1]: Started searching...
[Thread-1] Found FiCo after searching 4027 bytes 0.6900450000000002ms elapsed.
[Thread-2]: Started searching...
[Thread-2] Found FiCo after searching 3796 bytes 0.6875790000000076ms elapsed.
[Thread-3]: Started searching...
[Thread-3] Found FiCo after searching 10438 bytes 1.9046129999999994ms elapsed.
[Thread-4]: Started searching...
[Thread-4] Found FiCo after searching 15090 bytes 2.474850000000001ms elapsed.
[Thread-5]: Started searching...
[Thread-5] Found FiCo after searching 7207 bytes 1.203836ms elapsed.
[Thread-6]: Started searching...
[Thread-6] Found FiCo after searching 7666 bytes 1.3657680000000032ms elapsed.
[Thread-7]: Started searching...
[Thread-7] Found FiCo after searching 1205 bytes 0.23854200000000825ms elapsed.
[Thread-8]: Started searching...
[Thread-8] Found FiCo after searching 31189 bytes 6.1392820000000095ms elapsed.
[Thread-9]: Started searching...
[Thread-9] Found FiCo after searching 99121 bytes 17.948643999999998ms elapsed.
(9, 17.948643999999998, 99121, 'SUCCESS')
(8, 6.1392820000000095, 31189, 'SUCCESS')
(0, 2.7950100000000004, 16593, 'SUCCESS')
(4, 2.474850000000001, 15090, 'SUCCESS')
(3, 1.9046129999999994, 10438, 'SUCCESS')
(6, 1.3657680000000032, 7666, 'SUCCESS')
(5, 1.203836, 7207, 'SUCCESS')
(1, 0.6900450000000002, 4027, 'SUCCESS')
(2, 0.6875790000000076, 3796, 'SUCCESS')
(7, 0.23854200000000825, 1205, 'SUCCESS')
Average bytes per second is 332313.92007863626
```

# Data Generator

The data stream generator I inserted 2 'FiCo' and the generator just randomly generates an index between 0 and len(stream) and spits out a word at a time.

```python
# in ipython
from worker import DataGenerator

# second argument defines the length
In [5]: gen = DataGenerator('file.txt', 10)

In [6]: for i in gen:
   ...:     print(i)
   ...:

befrilled
copartnership
intimacy
agree with
flaring
Vienna green
enter
peristyle
spunkless
get over
free-lance writer
```