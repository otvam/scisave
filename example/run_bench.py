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
import functools
import scisave


if __name__ == "__main__":
    # number of repeats for the benchmark
    number = 5

    # list with the parsers to be benchmarked
    filename_list = ["tmp.gz", "tmp.json", "tmp.mpk", "tmp.pkl"]

    # create a dummy test data
    data = [[random.random() for _ in range(500)] for _ in range(500)]

    # deserialization function
    def fct_load(filename):
        scisave.load_data(filename)

    # serialization function
    def fct_write(filename):
        scisave.write_data(filename, data)

    # run the benchmark
    for filename in filename_list:
        print("======================== TIME / %s" % filename)

        # time the write and load functions
        time_write = timeit.timeit(functools.partial(fct_write, filename), number=number)
        time_load = timeit.timeit(functools.partial(fct_load, filename), number=number)

        # check the file size
        size = os.path.getsize(filename)

        # print the results
        print("write = %.3f" % (time_write / number))
        print("load = %.3f" % (time_load / number))
        print("size = %.3f kB" % (size / 1024))

        # remove the generated file
        os.remove(filename)

    sys.exit(0)
