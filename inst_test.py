from src.InstTest import *
import sys

try:
    test = str(sys.argv[1])
    print(inst_test(tests=test))
except:
    print(inst_test())