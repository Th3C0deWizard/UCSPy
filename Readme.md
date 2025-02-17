# UCSP Solver

This is a python program that can solve the University Course Scheduling Problem (UCSP)
using a local search approach.

## How to use?

To use the program first you need a json file with all the input data needed to create an UCSP instance.
The first_schedule_input_example.json served as a complete example of the input data needed.

After you have the input data, you can run the localsearch proof of concept algorithm using the following command:

```bash
    python ucsp/main.py <input_data.json>
```

This will run 1000 iterations of the localsearch algorithm with 100 as the max number of iterations and print the number of times it found a solution
along with a full trace of the executions.

If you wan to run a different number of executions and with a different max number of iterations you can use the following command:

```bash
    python ucsp/main.py <input_data.json> -e <number_of_executions> -m <max_number_of_iterations>
```

## Report

The report can be found in the file report.pdf in the root of the project. It contains a detailed explanation of the UCSP problem, the localsearch algorithm used to solve it and the results of the experiments.  
Note: The report is in spanish.
