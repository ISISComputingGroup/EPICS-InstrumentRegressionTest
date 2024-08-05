'''
Python command to allow for using inst_test with arguments from command line, or using default TEST.xml
'''

import sys

from src.InstTest import *

try:
    test = str(sys.argv[1])
    print(inst_test(tests=test))
except:
    print(inst_test())
