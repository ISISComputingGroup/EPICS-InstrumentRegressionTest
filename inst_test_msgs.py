'''
Python command to allow for using inst_test_msgs with arguments from command line, or using default TEST.xml
'''

from src.InstTest import *
import sys

try:
    test = str(sys.argv[1])
    print(inst_test_msgs(tests=test))
except:
    print(inst_test_msgs())