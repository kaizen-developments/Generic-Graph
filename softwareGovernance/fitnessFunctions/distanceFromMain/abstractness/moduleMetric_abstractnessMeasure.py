import os
import time
import sys

from typing import Dict, List
from typing import List

from icontract import ensure

import ast

Attribute, Value = str, type
FileContents = List[str]
AbstractMethodName = str

def get_abstractMethods_of(syntaxTree) -> List[str]:
    abstractMethods = []

    for node in ast.walk(syntaxTree):
        if isinstance(node, ast.ClassDef):
            for child in ast.iter_child_nodes(node):
                if isinstance(child, ast.FunctionDef):
                    # Check if the function has a "pass" statement as its body
                    has_pass = any(isinstance(grandchild, ast.Pass) for grandchild in ast.iter_child_nodes(child))

                    # Check if the function has an "abstractmethod" decorator
                    has_abstractmethod = any(isinstance(decorator, ast.Name) and decorator.id == 'abstractmethod' for decorator in child.decorator_list)

                    if has_pass or has_abstractmethod:
                        abstractMethods.append(child.name)

    return abstractMethods

def get_abstractFunctions_of(syntaxTree) -> List[str]:
    abstractFunctions = []

    for node in ast.walk(syntaxTree):
        if isinstance(node, ast.FunctionDef):
            # Check if the function is a direct child of the Module node (i.e., it doesn't belong to a class)
            is_direct_child_of_module = syntaxTree.body and node in syntaxTree.body
            # Check if the function has a "pass" statement as its body
            has_pass = any(isinstance(child, ast.Pass) for child in ast.iter_child_nodes(node))
            # Check if the function has an "abstractmethod" decorator
            has_abstractmethod = any(isinstance(decorator, ast.Name) and decorator.id == 'abstractmethod' for decorator in node.decorator_list)
            if is_direct_child_of_module and (has_pass or has_abstractmethod):
                abstractFunctions.append(node.name)

    return abstractFunctions

def get_abstractClasses_of(syntaxTree) -> List[str]:
    abstractClasses = []

    for node in ast.walk(syntaxTree):
        if isinstance(node, ast.ClassDef):
            for child in ast.iter_child_nodes(node):
                if isinstance(child, ast.FunctionDef):
                    # Check if the function has a "pass" statement as its body
                    has_pass = any(isinstance(grandchild, ast.Pass) for grandchild in ast.iter_child_nodes(child))

                    # Check if the function has an "abstractmethod" decorator
                    has_abstractmethod = any(isinstance(decorator, ast.Name) and decorator.id == 'abstractmethod' for decorator in child.decorator_list)

                    if has_pass or has_abstractmethod:
                        abstractClasses.append(node.name)
                        break  # No need to check other methods in this class

    return abstractClasses


def get_non_abstractMethods_of(syntaxTree) -> List[str]:
    non_abstractMethods = []

    for node in ast.walk(syntaxTree):
        if isinstance(node, ast.ClassDef):
            for child in ast.iter_child_nodes(node):
                if isinstance(child, ast.FunctionDef):
                    # Check if the function is not abstract
                    has_pass = any(isinstance(grandchild, ast.Pass) for grandchild in ast.iter_child_nodes(child))
                    has_abstractmethod = any(isinstance(decorator, ast.Name) and decorator.id == 'abstractmethod' for decorator in child.decorator_list)
                    if not (has_pass or has_abstractmethod):
                        non_abstractMethods.append(child.name)

    return non_abstractMethods

def get_non_abstractFunctions_of(syntaxTree) -> List[str]:
    non_abstractFunctions = []

    for node in ast.walk(syntaxTree):
        if isinstance(node, ast.FunctionDef):
            # Check if the function is a direct child of the Module node (i.e., it doesn't belong to a class)
            is_direct_child_of_module = syntaxTree.body and node in syntaxTree.body
            # Check if the function is not abstract
            has_pass = any(isinstance(child, ast.Pass) for child in ast.iter_child_nodes(node))
            has_abstractmethod = any(isinstance(decorator, ast.Name) and decorator.id == 'abstractmethod' for decorator in node.decorator_list)
            if is_direct_child_of_module and (not has_pass) and (not has_abstractmethod):
                non_abstractFunctions.append(node.name)

    return non_abstractFunctions


def get_non_abstractClasses_of(syntaxTree) -> List[str]:
    non_abstractClasses = []

    for node in ast.walk(syntaxTree):
        if isinstance(node, ast.ClassDef):
            # Check if the class is not abstract
            is_abstract = False
            for child in ast.iter_child_nodes(node):
                if isinstance(child, ast.FunctionDef):
                    has_pass = any(isinstance(grandchild, ast.Pass) for grandchild in ast.iter_child_nodes(child))
                    has_abstractmethod = any(isinstance(decorator, ast.Name) and decorator.id == 'abstractmethod' for decorator in child.decorator_list)
                    if has_pass or has_abstractmethod:
                        is_abstract = True
                        break
            if not is_abstract:
                non_abstractClasses.append(node.name)

    return non_abstractClasses

def analyzeAbstractElements(syntaxTree) -> int:
    no_abstractMethods = len(get_abstractMethods_of(syntaxTree))
    no_abstractFunctions = len(get_abstractFunctions_of(syntaxTree))
    no_abstractClasses = len(get_abstractClasses_of(syntaxTree))
    no_abstractElements = no_abstractMethods + no_abstractFunctions + no_abstractClasses
    return no_abstractElements


def analyzeConcreteElements(syntaxTree) -> Dict[Attribute, Value]:
    no_abstractMethods = len(get_non_abstractMethods_of(syntaxTree))
    no_abstractFunctions = len(get_non_abstractFunctions_of(syntaxTree))
    no_abstractClasses = len(get_non_abstractClasses_of(syntaxTree))
    no_abstractElements = no_abstractMethods + no_abstractFunctions + no_abstractClasses
    return no_abstractElements

def analyzeTheFile(syntaxTree) -> Dict[Attribute, Value]:
    no_AbstractElements = analyzeAbstractElements(syntaxTree)
    no_concreteElements = analyzeConcreteElements(syntaxTree)
    measureOfAbstractness = no_AbstractElements / (no_AbstractElements + no_concreteElements)

    resultsOfAnalysis = {"Number of abstract elements" : no_AbstractElements, 
     "Number of concrete elements" : no_concreteElements, "Measure of abstractness" : measureOfAbstractness}
    
    return resultsOfAnalysis

@ensure(lambda filepath: (filepath_is_a_valid_python_file := os.path.isfile(filepath) and filepath.endswith('.py')))
def file_attributes(filepath:str) -> Dict[Attribute, Value]:
    with open(filepath, 'r') as sourceCode:
        syntaxTree = ast.parse(sourceCode.read())

    attributes = analyzeTheFile(syntaxTree)

    return attributes

assert (one_parameter_is_given := len(sys.argv) == 2), "Usage: python moduleMetric_abstractElements.py <filepath>"

file = sys.argv[1] 
filename = os.path.basename(file)
attributes = file_attributes(file)

for attribute in attributes.keys():
    print(f"{attribute} of {filename}={attributes[attribute]}")