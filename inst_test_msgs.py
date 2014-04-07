from src.InstTest import *
import sys

try:
    test = str(sys.argv[1])
    print(inst_test_msgs(tests=test))
except:
    print(inst_test_msgs())