from StaticError import *
from Symbol import *
from functools import *


def simulate(list_of_commands):
    """
    Executes a list of commands and processes them sequentially.

    Args:
        list_of_commands (list[str]): A list of commands to be executed.

    Returns:
        list[str]: A list of return messages corresponding to each command.
    """
    # def Symbol_a():
    #     return Symbol("a", "number")

    # def Symbol_b():
    #     return Symbol("b", "string")

    # Symbol_Creator = [Symbol_a, Symbol_b]
    # Symbol_Table = reduce(lambda acc, func: acc + [func()], Symbol_Creator, [])

    # def Symbol_a(acc):
    #     return acc + [Symbol("a", "number")]

    # def Symbol_b(acc):
    #     return acc + [Symbol("b", "string")]

    # Symbol_Function = [Symbol_a, Symbol_b]
    # Result = reduce(lambda acc, func: acc + [func()], Symbol_Function, [])

    def Is_Valid_Identifier(identifier_name):
        if len(identifier_name) == 0 or not ('a' <= identifier_name[0] <= 'z'):
            return False
        
        Allowed_Character = list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_")
        
        return all(char in Allowed_Character for char in identifier_name)

    def Is_Valid_String_Constant(value):
        Allowed_string = list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 ")

        if value[0] != "'" and value[-1] != "'":
            return False
        
        content = value[1:-1]

        return all(char in Allowed_string for char in content)

    def Is_Valid_Number_Constant(value):
        Allowed_number = list("0123456789")

        return all(char in Allowed_number for char in value)
    
    stack = [{}]
    level = 0

    def INSERT(INPUT_STRING, stack, level):
        Part = INPUT_STRING.split(" ")

        if len(Part) != 3 or Part[0] != "INSERT":
            raise InvalidInstruction()
        
        identifier_name = Part[1]
        dataType = Part[2]

        if (not Is_Valid_Identifier(identifier_name)):
            raise InvalidInstruction()

        if dataType not in ("string", "number"):
            raise InvalidInstruction()
        
        if identifier_name in stack[level]:
            raise Redeclared()
        
        new_scope = stack[level].copy()
        new_scope[identifier_name] = (dataType, level)
        new_stack = stack[:level] + [new_scope] + stack[level+1:]

        return "success", new_stack
    
    def ASSIGN(INPUT_STRING, stack, level):
        Part = INPUT_STRING.split(" ")

        if len(Part) != 3 or Part[0] != "ASSIGN":
            raise InvalidInstruction()
        
        identifier_name = Part[1]
        value = Part[2]

        if not Is_Valid_Identifier(identifier_name):
            raise InvalidInstruction()

        new_stack = next((scope[identifier_name] for i, scope in reversed(list(enumerate(stack[:level + 1]))) if identifier_name in scope), None)

        if (new_stack is None):
            raise Undeclared()
        
        value, _ = new_stack

        if value == "string":
            if Is_Valid_String_Constant(value):
                return "success"
            else:
                return TypeMismatch()
        elif value == "number":
            if Is_Valid_Number_Constant(value):
                return "success"
            else:
                return TypeMismatch()

    def BEGIN(stack, level):
        new_stack = stack + [{}]
        new_level = level + 1
        return new_stack, new_level

    def END(stack, level):
        if len(stack) <= 1:
            raise UnclosedBlock()
        
        new_stack = stack[:-1]
        new_level = level - 1
        return new_stack, new_level

    def LOOKUP(INPUT_STRING, stack, level):
        Part = INPUT_STRING.split(" ")

        if len(Part) != 2 or Part[0] != "LOOKUP":
            raise InvalidInstruction()
        
        identifier_name = Part[1]

        if (not Is_Valid_Identifier(identifier_name)):
            raise InvalidInstruction()
        
        new_stack = next((scope[identifier_name] for i, scope in reversed(list(enumerate(stack[:level + 1]))) if identifier_name in scope), None)

        if (new_stack is None):
            raise Undeclared()
        
        _, level = new_stack

        return level
        
    def RPRINT(stack, level):
        result = list(map(lambda pair: f"{pair[0]}//{pair[1][1]}", reversed([(identifier, (dataType, defined_level))
            for i, scope in enumerate(stack[:level + 1])
            for identifier, (dataType, defined_level) in scope.items()
        ])))

        print("\n".join(result))

    for command in list_of_commands:
        if command == "INSERT":
            print(INSERT(command, stack, level))
        elif command == "ASSIGN":
            print(ASSIGN(command, stack, level))
        elif command == "BEGIN":
            print(BEGIN(stack, level))
        elif command == "END":
            print(END(stack, level))
        elif command == "LOOKUP":
            print(LOOKUP(command, stack, level))
        elif command == "RPRINT":
            RPRINT(stack, level)
        else:
            raise InvalidInstruction()

    return ["success", "success"]