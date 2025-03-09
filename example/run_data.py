"""
Simple script demonstrating the SciSave capabilities.
"""

__author__ = "Thomas Guillod"
__copyright__ = "Thomas Guillod - Dartmouth College"
__license__ = "BSD License"

import os
import sys
import numpy as np
import scisave


if __name__ == "__main__":
    # set environment variables (used in the config file)
    os.environ["ENVDATA_A"] = "data_env_a"
    os.environ["ENVDATA_B"] = "data_env_b"

    # set substitution variables (used in the config file)
    substitute = {
        "sub_a": "data_sub_a",
        "sub_b": "data_sub_b",
    }

    # load the configuration file with custom YAML extensions
    config_tmp = scisave.load_config("config_main.yaml", extension=True, substitute=substitute)
    print("======================== CONFIG")
    print(config_tmp)

    # validate the configuration data with a schema
    schema = scisave.load_config("config_schema.yaml", extension=True, substitute=substitute)
    scisave.validate_schema(config_tmp, schema, extension=True)

    # create a data with complex numbers and arrays
    data = {
        "complex_scalar": 3 + 4j,
        "int_array": np.array([1, 2, 3]),
        "float_array": np.array([1.0, 2.0, 3.0]),
        "complex_array": np.array([1 + 1j, 2 + 2j, 3 + 3j]),
        "bool_array": np.array([True, False, True]),
        "multi_array": np.array([[1, 2], [3, 4]]),
    }

    # dump and load the data as JSON/TXT
    scisave.write_data("dump.json", data)
    data_file = scisave.load_data("dump.json")
    data_obj = scisave.loads("json", scisave.dumps("json", data))
    print("======================== JSON/TXT")
    print(data_file)
    print(data_obj)

    # dump and load the data as JSON/GZIP
    scisave.write_data("dump.gz", data)
    data_file = scisave.load_data("dump.gz")
    data_obj = scisave.loads("gzip", scisave.dumps("gzip", data))
    print("======================== JSON/GZIP")
    print(data_file)
    print(data_obj)

    # dump and load the data as MessagePack
    scisave.write_data("dump.mpk", data)
    data_file = scisave.load_data("dump.mpk")
    data_obj = scisave.loads("msgpack", scisave.dumps("msgpack", data))
    print("======================== MSGPACK")
    print(data_file)
    print(data_obj)

    # dump and load the data as Pickle
    scisave.write_data("dump.pkl", data)
    data_file = scisave.load_data("dump.pkl")
    data_obj = scisave.loads("pickle", scisave.dumps("pickle", data))
    print("======================== PICKLE")
    print(data_file)
    print(data_obj)

    sys.exit(0)
