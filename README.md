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

# Sample

```bash
$ python worker.py
[Thread-0]: Started searching...
[Thread-0] Found FiCo after searching 18303 bytes 3.3776569999999992ms elapsed.
[Thread-1]: Started searching...
[Thread-1] Found FiCo after searching 26358 bytes 4.770211000000003ms elapsed.
[Thread-2]: Started searching...
[Thread-2] Found FiCo after searching 1205 bytes 0.25209600000000026ms elapsed.
[Thread-3]: Started searching...
[Thread-3] Found FiCo after searching 2985 bytes 0.615145999999997ms elapsed.
[Thread-4]: Started searching...
[Thread-4] Found FiCo after searching 103915 bytes 21.335426999999996ms elapsed.
[Thread-5]: Started searching...
[Thread-5] Found FiCo after searching 12123 bytes 2.079235999999998ms elapsed.
[Thread-6]: Started searching...
[Thread-6] Found FiCo after searching 16964 bytes 2.8636349999999893ms elapsed.
[Thread-7]: Started searching...
[Thread-7] Found FiCo after searching 46474 bytes 8.250979999999991ms elapsed.
[Thread-8]: Started searching...
[Thread-8] Found FiCo after searching 30077 bytes 4.938324000000008ms elapsed.
[Thread-9]: Started searching...
[Thread-9] Found FiCo after searching 54186 bytes 9.21670799999999ms elapsed.
[(4, 21.335426999999996, 103915, 'SUCCESS'), (9, 9.21670799999999, 54186, 'SUCCESS'), (7, 8.250979999999991, 46474, 'SUCCESS'), (8, 4.938324000000008, 30077, 'SUCCESS'), (1, 4.770211000000003, 26358, 'SUCCESS'), (0, 3.3776569999999992, 18303, 'SUCCESS'), (6, 2.8636349999999893, 16964, 'SUCCESS'), (5, 2.079235999999998, 12123, 'SUCCESS'), (3, 0.615145999999997, 2985, 'SUCCESS'), (2, 0.25209600000000026, 1205, 'SUCCESS')]
```

or where `thread 9` timed out

```bash
(base)  jackchi@Chompy  ~/git/hatch-takehome  python worker.py --timeout 0.0001
[Thread-0]: Started searching...
[Thread-0] Found FiCo after searching 38806 bytes 6.921399000000002ms elapsed.
[Thread-1]: Started searching...
[Thread-1] Found FiCo after searching 95599 bytes 15.916971999999987ms elapsed.
[Thread-2]: Started searching...
[Thread-2] Found FiCo after searching 45634 bytes 8.780680999999998ms elapsed.
[Thread-3]: Started searching...
[Thread-3] Found FiCo after searching 9007 bytes 1.7785869999999981ms elapsed.
[Thread-4]: Started searching...
[Thread-4] Found FiCo after searching 4880 bytes 0.8359770000000016ms elapsed.
[Thread-5]: Started searching...
[Thread-5] Found FiCo after searching 20297 bytes 3.399789ms elapsed.
[Thread-6]: Started searching...
[Thread-6] Found FiCo after searching 1482 bytes 0.2548990000000029ms elapsed.
[Thread-7]: Started searching...
[Thread-7] Found FiCo after searching 3960 bytes 0.6817449999999975ms elapsed.
[Thread-8]: Started searching...
[Thread-8] Found FiCo after searching 44454 bytes 7.498829999999998ms elapsed.
[Thread-9]: Started searching...
[Thread-9]: TIMEOUT
[Thread-9] TIMEOUT after searching 44488 bytes 7.697049999999997ms elapsed.
[(1, 15.916971999999987, 95599, 'SUCCESS'), (2, 8.780680999999998, 45634, 'SUCCESS'), (9, 7.697049999999997, 44488, 'TIMEOUT'), (8, 7.498829999999998, 44454, 'SUCCESS'), (0, 6.921399000000002, 38806, 'SUCCESS'), (5, 3.399789, 20297, 'SUCCESS'), (3, 1.7785869999999981, 9007, 'SUCCESS'), (4, 0.8359770000000016, 4880, 'SUCCESS'), (7, 0.6817449999999975, 3960, 'SUCCESS'), (6, 0.2548990000000029, 1482, 'SUCCESS')]
```

The data stream generator I inserted 2 'FiCo' and the generator just randomly generates an index between 0 and len(stream) and spits out a word at a time.