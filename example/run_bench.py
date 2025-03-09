"""
Simple script for benchmarking the serialization/deserialization speed.
"""

__author__ = "Thomas Guillod"
__copyright__ = "Thomas Guillod - Dartmouth College"
__license__ = "BSD License"

import os
import sys
import timeit
import random
import scisave


if __name__ == "__main__":
    # set the parameters
    number = 5 # number of repeats for the timing
    filename_list = ["tmp.gz", "tmp.json", "tmp.mpk", "tmp.pkl"] # parser to be checked

    # create a dummy test data
    data = [[random.random() for _ in range(500)] for _ in range(500)]

    # run the benchmark
    for filename in filename_list:
        # function to be timed
        print("======================== TIME / %s" % filename)
        fct_load = lambda: scisave.load_data(filename)
        fct_write = lambda: scisave.write_data(filename, data)

        # time the write and load functions
        time_write = timeit.timeit(fct_write, number=number)
        time_load = timeit.timeit(fct_load, number=number)

        # check the file size
        size = os.path.getsize(filename)

        # print the results
        print("write = %.3f" % (time_write/number))
        print("load = %.3f" % (time_load/number))
        print("size = %.3f kB" % (size/1024))

        # clean the file
        os.remove(filename)

    sys.exit(0)
