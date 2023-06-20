import os
import json
from json.decoder import JSONDecodeError
from _io import TextIOWrapper


def loadJSON(jsonData):
    """
        Reads the json object to the memory.

        Could be:

            * file object: any file-like object with the property 'read'.
            * str: either the JSON or a path to the directory.
            * dict: the JSON object.

    Parameters
    ----------
    jsonData : str, object file, path to disk, dict
        The object that contains the dict.

    Returns
    -------
        dict
        The loaded JSON.

    """

    if hasattr(jsonData, 'read'):
        loadedjson = json.load(jsonData)
    elif isinstance(jsonData, str):
        if os.path.exists(jsonData):
            with open(jsonData) as jsonFile:
                loadedjson = json.load(jsonFile)
        else:
            try:
                loadedjson = json.loads(jsonData)
            except JSONDecodeError as e:
                raise ValueError(f" {str(e)}: Got {jsonData}, either bad format of file does not exist")

    elif isinstance(jsonData, dict):
        loadedjson = jsonData
    elif isinstance(jsonData, TextIOWrapper):
        loadedjson = json.load(jsonData)

    else:
        err = f"workflow type: {type(jsonData)} is unknonw. Must be str, file-like or dict. "
        raise ValueError(err)


    return  loadedjson
