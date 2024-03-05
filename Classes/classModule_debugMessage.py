from typing import List

class DebugMessage(object):
    @classmethod
    def valueOfVariableInContext(cls,className:str, methodName:str, linenumber:int, variableName:str, obj) -> str:
        return f"{className}.{methodName}:Line {linenumber}:at initialization :: {variableName}:{type(obj)} = {obj}.\n"
    
    @classmethod
    def usingMethodWithParameters(cls, className:str, methodName:str, linenumber:int, nameOfMethodCalled:str, parameters:List) -> str:
        return f"{className}.{methodName}:Line {linenumber}:: using method {nameOfMethodCalled} with parameters {parameters}.\n"

    @classmethod
    def identityOfObject(cls, module_or_className:str, methodName:str, linenumber:int, variableName:str, variable):
        return f"{module_or_className}.{methodName}:at Line {linenumber}:: The identity of the object of type {type(variable)} named as {variableName} is {variable}.\n"
    