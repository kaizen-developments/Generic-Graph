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
    get_non_abstractFunctions_of, get_non_abstractClasses_of, countAbstractElements, \
    countConcreteElements, analyzeTheFile

#Use a relative import to get fixtures/testModule.py from the current folder!

class TestAbstractness(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.classModule_relativePath = "fixtures/testModule1.py"
        cls.moduleMetric_relativePath = "fixtures/testModule2.py"
        cls.implementationModule_relativePath = "fixtures/testModule3.py"
        with open(cls.classModule_relativePath, "r") as code:
            cls.classModule_syntaxTree = ast.parse(code.read())
        with open(cls.moduleMetric_relativePath, "r") as code:
            cls.moduleMetric_syntaxTree = ast.parse(code.read())
        with open(cls.implementationModule_relativePath) as code:
            cls.implementationModule_syntaxTree = ast.parse(code.read())

    def test_get_abstractMethods_of(self):
        result = get_abstractMethods_of(self.classModule_syntaxTree)
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 4)
        self.assertEqual(result, ["startNode", "endNode", "getNodes", "getEdges"])


    def test_get_abstractFunctions_of(self):
        result = get_abstractFunctions_of(self.moduleMetric_syntaxTree)
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)
        self.assertEqual(result, ["analyzeTheFile"])

    def test_get_non_abstractMethods_of(self):
        result = get_non_abstractMethods_of(self.classModule_syntaxTree)
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 8)
        self.assertEqual(result, ["elements", "__str__", "neighboursOf", "addNode", "removeNode", "addEdge", "__contains__", "__str__"])

    def test_get_non_abstractFunctions_of(self):
        result = get_non_abstractFunctions_of(self.moduleMetric_syntaxTree)
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 2)
        self.assertEqual(result, ["file_attributes", "main"])

    def test_get_abstractClasses_of(self):
        result = get_abstractClasses_of(self.classModule_syntaxTree)
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 2)
        self.assertEqual(result, ["Edge", "Graph"])

    def test_get_non_abstractClasses_of(self):
        result = get_non_abstractClasses_of(self.implementationModule_syntaxTree)
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 2)
        self.assertEqual(result, ["Link", "ResourceGraph"])

    def test_countAbstractElements(self):
        result = countAbstractElements(self.classModule_syntaxTree)
        self.assertIsInstance(result, int)
        self.assertEqual(result, 6)

    def test_countConcreteElements(self):
        result = countConcreteElements(self.classModule_syntaxTree)
        self.assertIsInstance(result, int)
        self.assertEqual(result, 8)

    def test_analyzeTheFile(self):
        result = analyzeTheFile(self.classModule_syntaxTree)
        self.assertIsInstance(result, dict)
        self.assertEqual(result, 
        {
            "Number of abstract elements" : 6,
            "Number of concrete elements" : 8,
            "Measure of abstractness" : 0.42857142857142855
        })

if __name__ == '__main__':
    unittest.main()