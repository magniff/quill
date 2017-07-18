
import re
from support import BaseTest

class TestBytecodeCompiler(BaseTest):

    def assert_equals(self, bytecode, expected):
        def reformat(lines):
            # find first non empty
            for line in lines:
                if line.strip(" ") != "":
                    break
            m = re.match(" +", line)
            skip = len(m.group(0))
            return [line[(skip - 2):] for line in lines if line.strip(" ") != ""]

        lines = bytecode.repr().splitlines()
        exp_lines = reformat(expected.splitlines())
        assert lines == exp_lines

    def test_bytecode_simple(self):
        body = """
        x = 3;
        """
        self.assert_equals(self.compile(body), """
            LOAD_CONSTANT 0
            STORE 0
            LOAD_NONE
            RETURN
            """)

    def test_bytecode_bit_more_complext(self):
        body = """
        x = 3;
        x = x + 1;
        """
        bc = self.compile(body)
        self.assert_equals(bc,"""
            LOAD_CONSTANT 0
            STORE 0
            LOAD_VARIABLE 0
            LOAD_CONSTANT 1
            ADD
            STORE 0
            LOAD_NONE
            RETURN
            """)
        assert bc.stack_depth == 2
