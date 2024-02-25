import os
import time
import sys

from icontract import ensure

from typing import Dict, List

Attribute, Value = str, type

def analyzeTheFile(contentsOfTheFile:List[str], filename:str) -> Dict[Attribute, Value]:
    pass

@ensure(lambda filepath: (filepath_is_a_valid_python_file := os.path.isfile(filepath) and filepath.endswith('.py')))
def file_attributes(filepath:str) -> Dict[Attribute, Value]:
    with open(filepath, 'r') as file:
        contentsOfTheFile:List[str] = file.readlines()

    filename = os.path.basename(filepath)
    attributes = analyzeTheFile(contentsOfTheFile, filename)

    return attributes

assert (one_parameter_is_given := len(sys.argv) == 2), "Usage: python moduleMetric_abstractElements.py <filepath>"

file = sys.argv[1] 
filename = os.path.basename(file)
attributes = file_attributes(file)

for attribute in attributes.keys():
    print(f"{attribute} of {filename}={attributes[attribute]}")