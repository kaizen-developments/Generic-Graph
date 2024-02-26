import unittest
import ast

import sys
import os

def import_the_folder_n_steps_above(n: int) -> None:
    current_folder = os.path.abspath(os.path.dirname(__file__))
    steps = [".."] * n
    target_folder = os.path.abspath(os.path.join(current_folder, *steps))
    sys.path.insert(0, target_folder)
import_the_folder_n_steps_above(n=1)

from abstractness.moduleMetric_abstractnessMeasure import get_abstractMethods_of, \
    get_abstractFunctions_of, get_abstractClasses_of, get_non_abstractMethods_of, \
    get_non_abstractFunctions_of, get_non_abstractClasses_of, analyzeAbstractElements, \
    analyzeConcreteElements, analyzeTheFile

class TestAbstractness(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        with open("/home/solteszistvan/Programming/python_programs/genericGraph/softwareGovernance/fitnessFunctions/distanceFromMain/abstractness/abstractModule_graph.py", "r") as file:
            cls.syntaxTree = ast.parse(file.read())

    def test_get_abstractMethods_of(self):
        result = get_abstractMethods_of(self.syntaxTree)
        self.assertIsInstance(result, list)

    def test_get_abstractFunctions_of(self):
        result = get_abstractFunctions_of(self.syntaxTree)
        self.assertIsInstance(result, list)

    def test_get_non_abstractMethods_of(self):
        result = get_non_abstractMethods_of(self.syntaxTree)
        self.assertIsInstance(result, list)

    def test_get_non_abstractFunctions_of(self):
        result = get_non_abstractFunctions_of(self.syntaxTree)
        self.assertIsInstance(result, list)

    def test_get_abstractClasses_of(self):
        result = get_abstractClasses_of(self.syntaxTree)
        self.assertIsInstance(result, list)

    def test_get_non_abstractClasses_of(self):
        result = get_non_abstractClasses_of(self.syntaxTree)
        self.assertIsInstance(result, list)

    def test_analyzeAbstractElements(self):
        result = analyzeAbstractElements(self.syntaxTree)
        self.assertIsInstance(result, int)

    def test_analyzeConcreteElements(self):
        result = analyzeConcreteElements(self.syntaxTree)
        self.assertIsInstance(result, int)

    def test_analyzeTheFile(self):
        result = analyzeTheFile(self.syntaxTree)
        self.assertIsInstance(result, dict)

if __name__ == '__main__':
    unittest.main()