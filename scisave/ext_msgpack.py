"""
Module for serialization and deserialization of MessagePack files (with extensions).
    - Allows the serialization/deserialization of complex numbers (`__complex__`).
    - Allows the serialization/deserialization of NumPy arrays (`__numpy__`).
    - Allows the serialization/deserialization as/from text and gzip files
"""

__author__ = "Thomas Guillod"
__copyright__ = "Thomas Guillod - Dartmouth College"
__license__ = "BSD License"

import msgpack
import numpy as np


def _encode_object(obj):
    """
    Function encoding NumPy types as dictionaries.
    """

    # encode numpy scalars and arrays
    if np.isscalar(obj) and np.iscomplexobj(obj):
        return {
            "__complex__": None,
            "real": obj.real,
            "imag": obj.imag,
        }
    elif np.isscalar(obj) and np.issubdtype(obj.dtype, np.integer):
        return int(obj)
    elif np.isscalar(obj) and np.issubdtype(obj.dtype, np.floating):
        return float(obj)
    elif np.isscalar(obj) and np.issubdtype(obj.dtype, bool):
        return bool(obj)
    elif isinstance(obj, np.ndarray):
        # handle numpy array
        if np.iscomplexobj(obj):
            return {
                "__numpy__": None,
                "dtype": "complex",
                "shape": obj.shape,
                "data": {
                    "real": obj.real.flatten().tolist(),
                    "imag": obj.imag.flatten().tolist(),
                },
            }
        elif np.issubdtype(obj.dtype, np.floating):
            return {
                "__numpy__": None,
                "dtype": "float",
                "shape": obj.shape,
                "data": obj.flatten().tolist(),
            }
        elif np.issubdtype(obj.dtype, np.integer):
            return {
                "__numpy__": None,
                "dtype": "int",
                "shape": obj.shape,
                "data": obj.flatten().tolist(),
            }
        elif np.issubdtype(obj.dtype, bool):
            return {
                "__numpy__": None,
                "dtype": "bool",
                "shape": obj.shape,
                "data": obj.flatten().tolist(),
            }
        else:
            TypeError("invalid numpy array for serialization")
    else:
        # if not numpy, default to the base encoder
        return obj


def _decode_object(obj):
    """
    Function decoding NumPy types from dictionaries.
    """

    # if not dict, do nothing
    if not isinstance(obj, dict):
        return obj

    # parse the extensions
    if "__complex__" in obj:
        # handling complex scalar
        real = obj["real"]
        imag = obj["imag"]
        return complex(real, imag)
    elif "__numpy__" in obj:
        # handle numpy array
        dtype = obj["dtype"]
        shape = obj["shape"]
        data = obj["data"]

        # parse the type
        if dtype == "complex":
            real = np.array(data["real"], dtype=complex).reshape(shape)
            imag = np.array(data["imag"], dtype=complex).reshape(shape)
            return real + 1j * imag
        elif dtype == "float":
            return np.array(data, dtype=float).reshape(shape)
        elif dtype == "int":
            return np.array(data, dtype=int).reshape(shape)
        elif dtype == "bool":
            return np.array(data, dtype=bool).reshape(shape)
    else:
        return obj


def load_msgpack(filename, extension=True):
    """
    Load a MessagePack file (with/without custom extensions).
    """

    # create a decoder (without or without extensions)
    if extension:
        fct = _decode_object
    else:
        fct = None

    # load the MessagePack data
    with open(filename, "rb") as fid:
        data = msgpack.load(fid, object_hook=fct)

    return data


def write_msgpack(filename, data, extension=True):
    """
    Write a MessagePack file (with/without custom extensions).
    """

    # create an encoder (without or without extensions)
    if extension:
        fct = _encode_object
    else:
        fct = None

    # write the MessagePack data
    with open(filename, "wb") as fid:
        msgpack.dump(data, fid, default=fct)

    return data

def loads(data, extension=True):
    """
    Deserialize a MessagePack object (with/without custom extensions).
    """

    # create a decoder (without or without extensions)
    if extension:
        fct = _decode_object
    else:
        fct = None

    # deserialize the MessagePack data
    data = msgpack.loads(data, object_hook=fct)

    return data

def dumps(data, extension=True):
    """
    Serialize a MessagePack object (with/without custom extensions).
    """

    # create an encoder (without or without extensions)
    if extension:
        fct = _encode_object
    else:
        fct = None

    # serialize the MessagePack data
    data = msgpack.dumps(data, default=fct)

    return data
