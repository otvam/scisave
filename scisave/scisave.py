"""
Module for serialization and deserialization.
    - Load and write JSON/MessagePack/Pickle data files.
    - Load JSON/YAML configuration files.
    - Validate data with JSON schemas.
"""

__author__ = "Thomas Guillod"
__copyright__ = "Thomas Guillod - Dartmouth College"
__license__ = "BSD License"

import os.path
import pickle
from scisave import ext_yaml
from scisave import ext_json
from scisave import ext_msgpack
from scisave import ext_schema


def load_config(filename, extension=True, substitute=None):
    """
    Load a configuration file (JSON or YAML).

    Parameters
    ----------
    filename : string
        Name and path of the file to be loaded.
        The file type is determined by the extension.
        For YAML files, the extension should be "yaml" or "yml".
        For JSON files, the extension should be "json" or "js".
        For GZIP/JSON files, the extension should be "gzip" or "gz".
    extension : bool
        Activate (or not) the YAML extensions.
        Activate (or not) the JSON extensions.
    substitute : dict
        Dictionary with the substitution.
        The key names are replaces by the values.
        Substitutions are only used for YAML files.

    Returns
    -------
    data : data
        Python data contained in the file content
    """

    (name, ext) = os.path.splitext(filename)
    if ext in [".json", ".js"]:
        data = ext_json.load_json(filename, extension=extension, compress=False)
    elif ext in [".gz", ".gzip"]:
        data = ext_json.load_json(filename, extension=extension, compress=True)
    elif ext in [".yaml", ".yml"]:
        include = [os.path.abspath(filename)]
        data = ext_yaml.load_yaml(filename, include, extension=extension, substitute=substitute)
    else:
        raise ValueError("invalid file extension: %s" % filename)

    return data


def load_data(filename):
    """
    Load a data file (JSON or MessagePack or Pickle).

    Parameters
    ----------
    filename : string
        Name and path of the file to be loaded.
        The file type is determined by the extension.
        For JSON files, the extension should be "json" or "js".
        For GZIP/JSON files, the extension should be "gzip" or "gz".
        For MessagePack files, the extension should be "mpk" or "msg" or "msgpack".
        For Pickle files, the extension should be "pck" or "pkl" or "pickle".

    Returns
    -------
    data : data
        Python data contained in the file content
    """

    (name, ext) = os.path.splitext(filename)
    if ext in [".json", ".js"]:
        data = ext_json.load_json(filename, extension=True, compress=False)
    elif ext in [".gz", ".gzip"]:
        data = ext_json.load_json(filename, extension=True, compress=True)
    elif ext in [".mpk", ".msg", ".msgpack"]:
        data = ext_msgpack.load_msgpack(filename, extension=True)
    elif ext in [".pck", ".pkl", ".pickle"]:
        with open(filename, "rb") as fid:
            data = pickle.load(fid)
    else:
        raise ValueError("invalid file extension: %s" % filename)

    return data


def write_data(filename, data):
    """
    Write a data file (JSON or MessagePack or Pickle).

    Parameters
    ----------
    filename : string
        Name and path of the file to be created.
        The file type is determined by the extension.
        For JSON files, the extension should be "json" or "js".
        For GZIP/JSON files, the extension should be "gzip" or "gz".
        For MessagePack files, the extension should be "mpk" or "msg" or "msgpack".
        For Pickle files, the extension should be "pck" or "pkl" or "pickle".
    data : data
        Python data to be saved.
    """

    (name, ext) = os.path.splitext(filename)
    if ext in [".json", ".js"]:
        ext_json.write_json(filename, data, extension=True, compress=False)
    elif ext in [".gz", ".gzip"]:
        ext_json.write_json(filename, data, extension=True, compress=True)
    elif ext in [".mpk", ".msg", ".msgpack"]:
        ext_msgpack.write_msgpack(filename, data, extension=True)
    elif ext in [".pck", ".pkl", ".pickle"]:
        with open(filename, "wb") as fid:
            pickle.dump(data, fid)
    else:
        raise ValueError("invalid file extension: %s" % filename)


def loads(format, data):
    """
    Deserialize an object with different format (JSON or MessagePack or Pickle).

    Parameters
    ----------
    format : string
        Name of the serialization format ("json" or "gzip" or "msgpack" or "pickle").
    data : data
        Python data to be deserialized.

    Returns
    -------
    data : data
        Deserialized Python data
    """

    if format == "json":
        return ext_json.loads(data, extension=True, compress=False)
    if format == "gzip":
        return ext_json.loads(data, extension=True, compress=True)
    elif format == "msgpack":
        return ext_msgpack.loads(data, extension=True)
    elif format == "pickle":
        return pickle.loads(data)
    else:
        raise ValueError("invalid format: %s" % format)


def dumps(format, data):
    """
    Serialize an object with different format (JSON or MessagePack or Pickle).

    Parameters
    ----------
    format : string
        Name of the serialization format ("json" or "gzip" or "msgpack" or "pickle").
    data : data
        Python data to be serialized.

    Returns
    -------
    data : data
        Serialized Python data
    """

    if format == "json":
        return ext_json.dumps(data, extension=True, compress=False)
    if format == "gzip":
        return ext_json.dumps(data, extension=True, compress=True)
    elif format == "msgpack":
        return ext_msgpack.dumps(data, extension=True)
    elif format == "pickle":
        return pickle.dumps(data)
    else:
        raise ValueError("invalid format: %s" % format)


def validate_schema(data, schema, extension=True):
    """
    Validate data with a JSON schema.

    Parameters
    ----------
    data : data
        Python data to be validated.
    schema : schema
        JSON schema used to validate the data.
    extension : bool
        Activate (or not) the NumPy extensions.
        The extensions handle NumPy types and arrays.
    """

    ext_schema.validate_schema(data, schema, extension=extension)
