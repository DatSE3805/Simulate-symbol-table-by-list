import unittest
from TestUtils import TestUtils
import inspect

class TestSymbolTable(unittest.TestCase):

    # 1. Test valid INSERT of number
    def test_001(self):
        input = [" INSERT x number"]
        expected = ["Invalid: Invalid command"]
        self.assertTrue(TestUtils.check(input, expected, inspect.stack()[0].function))

    # 2. Test valid INSERT of string
    def test_002(self):
        input = ["INSERT y string"]
        expected = ["success"]
        self.assertTrue(TestUtils.check(input, expected, inspect.stack()[0].function))

    # 3. Test Redeclared INSERT
    def test_003(self):
        input = ["INSERT x number", "INSERT x string"]
        expected = ["Redeclared: INSERT x string"]
        self.assertTrue(TestUtils.check(input, expected, inspect.stack()[0].function))

    # 4. Test ASSIGN valid value to declared variable
    def test_004(self):
        input = ["  INSERT x  number  ", "ASSIGN   x   10"]
        expected = ["Invalid: Invalid command"]
        self.assertTrue(TestUtils.check(input, expected, inspect.stack()[0].function))

    # 5. Test ASSIGN to undeclared variable
    def test_005(self):
        input = ["  ASSIGN x   10  "]
        expected = ["Invalid: Invalid command"]
        self.assertTrue(TestUtils.check(input, expected, inspect.stack()[0].function))

    # 6. Test ASSIGN with type mismatch (string to number)
    def test_006(self):
        input = ["INSERT x   number ", "ASSIGN   x 'abc'  "]
        expected = ["Invalid: INSERT x   number "]
        self.assertTrue(TestUtils.check(input, expected, inspect.stack()[0].function))

    # 7. Test BEGIN with valid scope
    def test_007(self):
        input = ["BEGIN", "INSERT x number", "END"]
        expected = ["success"]
        self.assertTrue(TestUtils.check(input, expected, inspect.stack()[0].function))

    # 8. Test END without BEGIN
    def test_008(self):
        input = ["END"]
        expected = ["UnknownBlock"]
        self.assertTrue(TestUtils.check(input, expected, inspect.stack()[0].function))

    # 9. Test UnclosedBlock: BEGIN without END
    def test_009(self):
        input = ["BEGIN", "INSERT x number"]
        expected = ["UnclosedBlock: 1"]
        self.assertTrue(TestUtils.check(input, expected, inspect.stack()[0].function))

    # 10. Test Nested BEGIN and END
    def test_010(self):
        input = [
            "INSERT x number",
            "INSERT y string",
            "BEGIN",
            "INSERT x number",
            "BEGIN",
            "INSERT y string",
            "END",
            "END"
        ]
        expected = ["success", "success", "success", "success"]
        self.assertTrue(TestUtils.check(input, expected, inspect.stack()[0].function))

    # 11. Test Redeclared variable within nested blocks
    def test_011(self):
        input = ["BEGIN", "  INSERT x number", "BEGIN", "INSERT x string", "END", "END"]
        expected = ["Invalid: Invalid command"]
        self.assertTrue(TestUtils.check(input, expected, inspect.stack()[0].function))

    # 12. Test LOOKUP for undeclared variable
    def test_012(self):
        input = ["LOOKUP   x"]
        expected = ["Invalid: LOOKUP   x"]
        self.assertTrue(TestUtils.check(input, expected, inspect.stack()[0].function))

    # 13. Test LOOKUP for declared variable
    def test_013(self):
        input = ["INSERT x number", "LOOKUP x"]
        expected = ["success", "0"]
        self.assertTrue(TestUtils.check(input, expected, inspect.stack()[0].function))

    # 14. Test PRINT all variables in current scope
    def test_014(self):
        input = ["INSERT x number", "PRINT"]
        expected = ["success","x//0"]
        self.assertTrue(TestUtils.check(input, expected, inspect.stack()[0].function))

    # 15. Test RPRINT all variables in current and parent scopes
    def test_015(self):
        input = [
            "BEGIN",
            "INSERT x number",
            "BEGIN",
            "INSERT y string",
            "RPRINT",
            "END",
            "END"
        ]
        expected = ["success", "success", "y//2 x//1"]
        self.assertTrue(TestUtils.check(input, expected, inspect.stack()[0].function))

    # 16. Test multiple variables with PRINT
    def test_016(self):
        input = [
            "INSERT x number",
            "INSERT y string",
            "PRINT"
        ]
        expected = ["success", "success", "x//0 y//0"]
        self.assertTrue(TestUtils.check(input, expected, inspect.stack()[0].function))

    # 17. Test RPRINT in nested blocks
    def test_017(self):
        input = [
            "BEGIN",
            "INSERT x   number",
            "BEGIN",
            "INSERT y   string",
            "RPRINT",
            "END",
            "RPRINT",
            "END"
        ]
        expected = ["Invalid: INSERT x   number"]
        self.assertTrue(TestUtils.check(input, expected, inspect.stack()[0].function))

    # 18. Test BEGIN/END block without operations inside
    def test_018(self):
        input = ["BEGIN", "END"]
        expected = [""]
        self.assertTrue(TestUtils.check(input, expected, inspect.stack()[0].function))

    # 19. Test Redeclared variable within the same block
    def test_019(self):
        input = ["BEGIN", "INSERT x number", "INSERT x string", "END"]
        expected = ["Redeclared: INSERT x string"]
        self.assertTrue(TestUtils.check(input, expected, inspect.stack()[0].function))

    # 20. Test correct ASSIGN and PRINT
    def test_020(self):
        input = ["INSERT x number", "ASSIGN x 10", "PRINT"]
        expected = ["success", "success","x//0"]
        self.assertTrue(TestUtils.check(input, expected, inspect.stack()[0].function))

    # 21. Test error in ASSIGN to undeclared variable
    def test_021(self):
        input = ["ASSIGN x 10"]
        expected = ["Undeclared: ASSIGN x 10"]
        self.assertTrue(TestUtils.check(input, expected, inspect.stack()[0].function))

    # 22. Test ASSIGN with type mismatch for number to string
    def test_022(self):
        input = ["INSERT x string", "ASSIGN x 10"]
        expected = ["TypeMismatch: ASSIGN x 10"]
        self.assertTrue(TestUtils.check(input, expected, inspect.stack()[0].function))

    # 23. Test multiple INSERTs and ASSIGNs in one block
    def test_023(self):
        input = [
            "INSERT x number",
            "INSERT y string",
            "ASSIGN x 10",
            "ASSIGN y 'hello'"
        ]
        expected = ["success", "success", "success", "success"]
        self.assertTrue(TestUtils.check(input, expected, inspect.stack()[0].function))

    # 24. Test LookUp and type mismatch assignment
    def test_024(self):
        input = [
            "INSERT x string",
            "ASSIGN x 10",
            "LOOKUP x"
        ]
        expected = ["TypeMismatch: ASSIGN x 10"]
        self.assertTrue(TestUtils.check(input, expected, inspect.stack()[0].function))

    # 25. Test Redeclaration within nested blocks
    def test_025(self):
        input = [
            "BEGIN",
            "INSERT x number",
            "BEGIN",
            "INSERT x string",
            "END",
            "END"
        ]
        expected = ["success", "success"]
        self.assertTrue(TestUtils.check(input, expected, inspect.stack()[0].function))

    # 26. Test RPRINT order from child to parent
    def test_026(self):
        input = [
            "BEGIN",
            "INSERT x number",
            "BEGIN",
            "INSERT y string",
            "RPRINT",
            "END",
            "RPRINT",
            "END"
        ]
        expected = ["success","success", "y//2 x//1", "x//1"]
        self.assertTrue(TestUtils.check(input, expected, inspect.stack()[0].function))

    # 27. Test error in INSERT with invalid identifier (starts with number)
    def test_027(self):
        input = ["INSERT 1x number"]
        expected = ["Invalid: INSERT 1x number"]
        self.assertTrue(TestUtils.check(input, expected, inspect.stack()[0].function))

    # 28. Test LookUp after multiple nested blocks
    def test_028(self):
        input = [
            "BEGIN",
            "INSERT x number",
            "BEGIN",
            "INSERT y string",
            "LOOKUP y",
            "END",
            "LOOKUP x",
            "END"
        ]
        expected = ["success", "success", "2", "1"]
        self.assertTrue(TestUtils.check(input, expected, inspect.stack()[0].function))

    # 29. Test multiple INSERTs and ASSIGNs with mismatched types
    def test_029(self):
        input = [
            "INSERT x number", "INSERT y string", "ASSIGN x 'hello'", "ASSIGN y 10"
        ]
        expected = ["TypeMismatch: ASSIGN x 'hello'"]
        self.assertTrue(TestUtils.check(input, expected, inspect.stack()[0].function))

    # 30. Test multiple levels of nested blocks with same variable
    def test_030(self):
        input = [
            "BEGIN", "INSERT x number", "BEGIN", "INSERT x string", "END", "END"
        ]
        expected = ["success", "success"]
        self.assertTrue(TestUtils.check(input, expected, inspect.stack()[0].function))

    def test_031(self):
        input = ["BEGIN", "INSERT x string", "ASSIGN x 'data'", "PRINT","END"]
        expected = ["success", "success","x//1"]
        self.assertTrue(TestUtils.check(input, expected, inspect.stack()[0].function))
    def test_032(self):
        input = ["INSERT x string", "ASSIGN x 'ab@'"]
        expected = ["Invalid: ASSIGN x 'ab@'"]
        self.assertTrue(TestUtils.check(input, expected, inspect.stack()[0].function))
    def test_033(self):
        input = [
            "INSERT x_1 number", "INSERT y string", "ASSIGN x_1 123", "ASSIGN y '213'"
        ]
        expected = ["success", "success", "success", "success"]
        self.assertTrue(TestUtils.check(input, expected, inspect.stack()[0].function)) 
    def test_034(self):
        input = [
            "ASSIGN Ax hello"
        ]
        expected = ["Invalid: ASSIGN Ax hello"]
        self.assertTrue(TestUtils.check(input, expected, inspect.stack()[0].function))
    def test_035(self):
        input = [
            "assign x hello"
        ]
        expected = ["Invalid: Invalid command"]
        self.assertTrue(TestUtils.check(input, expected, inspect.stack()[0].function))
    def test_036(self):
        input = [
            "ASSIGN x hello"
        ]
        expected = ["Undeclared: ASSIGN x hello"]
        self.assertTrue(TestUtils.check(input, expected, inspect.stack()[0].function))
    def test_037(self):
        input = [
            "INSERT x string",
            "ASSIGN x 'a@1'"
        ]
        expected = ["Invalid: ASSIGN x 'a@1'"]
        self.assertTrue(TestUtils.check(input, expected, inspect.stack()[0].function))
    def test_038(self):
        input = [
            "INSERT x number ",
            "BEGIN",
            "INSERT y number",
            "ASSIGN y x",
            "END"
        ]
        expected = ["Invalid: INSERT x number "]
        self.assertTrue(TestUtils.check(input, expected, inspect.stack()[0].function))
    def test_039(self):
        input = ["PRINT", "RPRINT"]
        expected = ["",""]
        self.assertTrue(TestUtils.check(input, expected, inspect.stack()[0].function))
    def test_040(self):
        input = [
            "INSERT number number",
        ]
        expected = ["success"]
        self.assertTrue(TestUtils.check(input, expected, inspect.stack()[0].function))
    def test_041(self):
        input = [
        "INSERT x string",
        "INSERT y string",
        "INSERT z number",
          "BEGIN",
          "ASSIGN x 'abc'",
          "INSERT x number",
         "ASSIGN x 50",
         "ASSIGN x 'def'",
         "ASSIGN z x",
         "END",
             ]   
        expected = ["TypeMismatch: ASSIGN x 'def'"]
        self.assertTrue(TestUtils.check(input, expected, inspect.stack()[0].function))
    def test_042(self):
        input = [
        "INSERT s string",
        "ASSIGN s ''"
    ]
        expected = ["success", "success"]
        self.assertTrue(TestUtils.check(input, expected, inspect.stack()[0].function))
    def test_043(self):
        input = [
            "END",
            "END"
        ]
        expected = ["UnknownBlock"]
        self.assertTrue(TestUtils.check(input, expected, inspect.stack()[0].function))
    def test_044(self):
        input = [
            "INSERT x number",
            "ASSIGN x y"
        ]
        expected = ["Undeclared: ASSIGN x y"]
        self.assertTrue(TestUtils.check(input, expected, inspect.stack()[0].function))
    def test_045(self):
        input = ["PRINT", "RPRINT","BEGIN","PRINT","RPRINT","END"]
        expected = ["","","",""]
        self.assertTrue(TestUtils.check(input, expected, inspect.stack()[0].function))
    def test_046(self):
        input = ["INSERT x number", "   "]
        expected = ["Invalid: Invalid command"]
        self.assertTrue(TestUtils.check(input, expected, inspect.stack()[0].function))
    def test_047(self):
        input = ["ASSIGN a 1"]
        expected = ["Undeclared: ASSIGN a 1"]
        self.assertTrue(TestUtils.check(input, expected, inspect.stack()[0].function))
    def test_048(self):
        input = ["PRINT"]
        expected = [""]
        self.assertTrue(TestUtils.check(input, expected, inspect.stack()[0].function))
    def test_049(self):
        input = ["LOOKUP  x"]
        expected = ["Invalid: LOOKUP  x"]
        self.assertTrue(TestUtils.check(input, expected, inspect.stack()[0].function))
    def test_050(self):
        input = ["INSERT x number", "LOOKUP x x"]
        expected = ["Invalid: LOOKUP x x"]
        self.assertTrue(TestUtils.check(input, expected, inspect.stack()[0].function))
    def test_051(self):
        input = ["BEGIN", "ASSIGN y 1", "INSERT x number", "INSERT y number", "END"]
        expected = ["Undeclared: ASSIGN y 1"]
        self.assertTrue(TestUtils.check(input, expected, inspect.stack()[0].function))
    def test_052(self):
        input = [
            "",
            "INSERT y string",
        ]
        expected = ["Invalid: Invalid command"]
        self.assertTrue(TestUtils.check(input, expected, inspect.stack()[0].function))
    def test_053(self):
        input = [
            "INSERT x number",
            "ASSIGN x x",
        ]
        expected = ["success", "success"]
        self.assertTrue(TestUtils.check(input, expected, inspect.stack()[0].function))
    def test_054(self):
        input = [
            "END 2",]
        expected = ["Invalid: END 2"]
        self.assertTrue(TestUtils.check(input, expected, inspect.stack()[0].function))
    def test_055(self):
        input = [""]
        expected = ["Invalid: Invalid command"]
        self.assertTrue(TestUtils.check(input, expected, inspect.stack()[0].function))
    def test_056(self):
        input = [
            "INSERT  x real_number",
        ]
        expected = ["Invalid: INSERT  x real_number"]
        self.assertTrue(TestUtils.check(input, expected, inspect.stack()[0].function))
    def test_057(self):
        input = [
            "CREATE x number",
        ]
        expected = ["Invalid: Invalid command"]
        self.assertTrue(TestUtils.check(input, expected, inspect.stack()[0].function))
    def test_058(self):
        input = [
            "INSERT x number",
            "ASSIGN x hello",
        ]
        expected = ["Undeclared: ASSIGN x hello"]
        self.assertTrue(TestUtils.check(input, expected, inspect.stack()[0].function))
    def test_059(self):
        input = [
            "   INSERT",
        ]
        expected = ["Invalid: Invalid command"]
        self.assertTrue(TestUtils.check(input, expected, inspect.stack()[0].function))
    def test_060(self):
        input = ["INSERT x number", "   "]
        expected = ["Invalid: Invalid command"]
        self.assertTrue(TestUtils.check(input, expected, inspect.stack()[0].function))
    def test_061(self):
        input = ["INSErT x number"]
        expected = ["Invalid: Invalid command"]
        self.assertTrue(TestUtils.check(input, expected, inspect.stack()[0].function))
    def test_062(self):
        input = ["INSERT x number", "INSERT y string", "ASSIGN x  1"]
        expected = ["Invalid: ASSIGN x  1"]
        self.assertTrue(TestUtils.check(input, expected, inspect.stack()[0].function))
    def test_063(self):
        input = ["INSER 1x number"]
        expected = ["Invalid: Invalid command"]
        self.assertTrue(TestUtils.check(input, expected, inspect.stack()[0].function))
        
    def test_064(self):
        input = [
            "BBEGIN",
            "BEGIN"
        ]
        expected = ["Invalid: Invalid command"]
        self.assertTrue(TestUtils.check(input, expected, inspect.stack()[0].function))