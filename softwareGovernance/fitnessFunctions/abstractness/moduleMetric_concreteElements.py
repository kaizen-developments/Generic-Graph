import os
import time
import sys

from typing import Dict, List

Attribute, Value = str, type

def analyzeTheFile(contentsOfTheFile:List[str], filename:str) -> Dict[Attribute, Value]:
    pass

def file_attributes(filepath:str) -> Dict[Attribute, Value]:
    # Check if file exists and has .py extension
    if not os.path.isfile(filepath) or not filepath.endswith('.py'):
        return "Invalid file. Please provide a Python (.py) file."

    with open(filepath, 'r') as file:
        contentsOfTheFile:List[str] = file.readlines()

    filename = os.path.basename(filepath)
    attributes = analyzeTheFile(contentsOfTheFile, filename)

    return attributes

# Get command line arguments
if len(sys.argv) != 2:
    print("Usage: python moduleMetric_abstractElements.py <filepath>")
    sys.exit(1)
else:
    file = sys.argv[1] 

    filename = os.path.basename(file)
    attributes = file_attributes(file)
    for attribute in attributes.keys():
        print(f"{attribute} of {filename}={attributes[attribute]}")