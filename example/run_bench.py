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
    ext_list = ["gz", "json", "mpk", "pkl"]

    # create a dummy test data
    data = [[random.random() for _ in range(500)] for _ in range(500)]

    # deserialization function
    def fct_load(filename):
        scisave.load_data(filename)

    # serialization function
    def fct_write(filename):
        scisave.write_data(filename, data)

    # run the benchmark
    for ext in ext_list:
        print("======================== %s" % ext)

        # name of the temporary file
        filename_reference = "reference.%s" % ext
        filename_benchmark = "benchmark.%s" % ext

        # write the data
        fct_write(filename_reference)

        # time the write and load functions
        time_load = timeit.timeit(functools.partial(fct_load, filename_reference), number=number)
        time_write = timeit.timeit(functools.partial(fct_write, filename_benchmark), number=number)

        # check the file size
        size = os.path.getsize(filename_reference)

        # print the results
        print("load = %.3f" % (time_load / number))
        print("write = %.3f" % (time_write / number))
        print("size = %.3f kB" % (size / 1024))

        # remove the generated files
        os.remove(filename_reference)
        os.remove(filename_benchmark)

    sys.exit(0)
