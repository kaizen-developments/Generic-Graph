import os
import time
import sys

from typing import Dict, List
from typing import List

from icontract import ensure

Attribute, Value = str, type
FileContents = List[str]
AbstractMethodName = str

def get_abstractMethods_of(contentsOfTheFile: FileContents) -> List[AbstractMethodName]:
    abstractMethods = []
    for line in contentsOfTheFile:
        if "abstract" in line and "def" in line:
            methodName = line.split("def")[1].split("(")[0].strip()
            abstractMethods.append(methodName)
    return abstractMethods

def get_abstractFunctions_of(contentsOfTheFile: FileContents) -> List[AbstractMethodName]:
    pass

def get_abstractClasses_of(contentsOfTheFile: FileContents) -> List[AbstractMethodName]:
    pass

def analyzeAbstractElements(contentsOfTheFile:FileContents) -> int:
    no_abstractMethods = len(get_abstractMethods_of(contentsOfTheFile))
    no_abstractFunctions = len(get_abstractFunctions_of(contentsOfTheFile))
    no_abstractClasses = len(get_abstractClasses_of(contentsOfTheFile))
    no_abstractElements = no_abstractMethods + no_abstractFunctions + no_abstractClasses
    return no_abstractElements


def analyzeConcreteElements(contentsOfTheFile:FileContents) -> Dict[Attribute, Value]:
    pass

def analyzeTheFile(contentsOfTheFile:FileContents, filename:str) -> Dict[Attribute, Value]:
    no_AbstractElements = analyzeAbstractElements(contentsOfTheFile)
    no_concreteElements = analyzeConcreteElements(contentsOfTheFile)
    measureOfAbstractness = no_AbstractElements / (no_AbstractElements + no_concreteElements)

    resultsOfAnalysis = {"Number of abstract elements" : no_AbstractElements, 
     "Number of concrete elements" : no_concreteElements, "Measure of abstractness" : measureOfAbstractness}
    
    return resultsOfAnalysis

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