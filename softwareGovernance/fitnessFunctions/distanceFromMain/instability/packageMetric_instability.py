import os
import sys
from typing import Dict, List

from icontract import ensure

Attribute, Value = str, type

def analyzeThePackage(contentsOfTheFile:List[str], filename:str, filepaths:List[str]) -> Dict[Attribute, Value]:
    pass

@ensure(lambda packagepath : (packagepath_is_a_python_package := os.path.isdir(packagepath) and os.path.isfile(os.path.join(packagepath, '__init__.py'))))
def get_all_filepaths(packagepath:str) -> List[str]:
    # Check if directory exists and contains __init__.py

    filepaths = []

    # Iterate over all .py files in the package directory
    for root, dirs, files in os.walk(packagepath):
        for file in files:
            if file.endswith('.py'):
                filepath = os.path.join(root, file)
                filepaths.append(filepath)

    return filepaths

@ensure(lambda packagepath : (packagepath_is_a_python_package := os.path.isdir(packagepath) and os.path.isfile(os.path.join(packagepath, '__init__.py'))))
def package_attributes(packagepath:str) -> Dict[Attribute, Value]:
    # Check if directory exists and contains __init__.py
    if not os.path.isdir(packagepath) or not os.path.isfile(os.path.join(packagepath, '__init__.py')):
        return "Invalid package. Please provide a valid Python package directory."
    filepaths = get_all_filepaths(packagepath)
    resultsOfAnalysis = analyzeThePackage(filepaths, packagepath, filepaths)

    return resultsOfAnalysis

# Get command line arguments
assert (one_parameter_is_given_to_the_script := len(sys.argv) == 2), "Usage: python <filename>.py <packagepath>"

package = sys.argv[1] 

attributes = package_attributes(package)
for filename, file_attributes in attributes.items():
    for attribute in file_attributes.keys():
        print(f"{attribute} of {filename}={file_attributes[attribute]}")