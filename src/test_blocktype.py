import unittest

from blocktype import BlockType, block_to_block_type


class TestTextNode(unittest.TestCase):

    def test_block_type_heading(self):
        block = "### This is a simple header"

        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    #TODO Add more tests for block_to_block_type

if __name__ == "__main__":
    unittest.main()
