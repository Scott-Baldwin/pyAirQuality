# standard library
import sys, unittest

sys.path.append("src")
# import individual test classes
# importing test classes will allow them to run from main below
from separation import TestSeparation
from handbook import TestHandbookExample_2

# run all test classes
if __name__ == "__main__":
    unittest.main()
