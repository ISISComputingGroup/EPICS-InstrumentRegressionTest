from __future__ import print_function
from PrintInfo import *
import os
import time

def GenerateLog(testdir,log_file,TESTS,testdets):	
	#Edit the log file and store in a seperate file - this may require some alterations
	hostname = os.environ['COMPUTERNAME']
	log_time = time.strftime('%Y-%m-%d %H-%M-%S', time.gmtime())
	edited_log_name = ('%s %s Test Log.txt' % (log_time,hostname))
	edited_log = os.path.join(testdir,edited_log_name)
	loged = open(edited_log, 'w')
	all_res = []
	res = []
	with open(log_file, 'r') as f:
	    for line in f:
	        all_res.append(line)
	
	number_of_tests = 0
	number_of_passes = 0
	for x in all_res:
	    line_start = x[:2]
	    #The line starts are limited to those I have noticed so far, more may be required, so keep an eye on the log file as well as the edited file during development
	    if line_start in ['Te','OK','As','Ty']:
	        res.append(x)
	        if line_start == 'Te':
	            number_of_tests = number_of_tests + 1
	        if line_start == 'OK':
	            number_of_passes = number_of_passes + 1
	
	#Concatenate the results to the test description
	red_res = []
	curr_entry = ''
	numtests = len(TESTS)
	y = 1
	print_info('Summary of results:')
	print_info('Test %s... ' % y, end='')
	for x in res:
	    line_start = x[:2]
	    if line_start == 'Te':
	        if curr_entry != '':
	            red_res.append(curr_entry)
	            y = y + 1
	            curr_entry = testdets[y]
	            print_info('Test %s... ' % y, end='')
	        else:
	            curr_entry = testdets[y]
	    else:
	        if x == 'OK\n':
	            outcome = 'Passed!\n'
	        else:
	            outcome = x
	        print_info(outcome,end='')
	        curr_entry = curr_entry + ':\t' + outcome
	red_res.append(curr_entry)
	
	pass_state = 'UNKNOWN'
	if number_of_tests == number_of_passes:
		pass_state = 'PASS'
	else:
		pass_state = 'FAIL'
	
	number_of_fails = number_of_tests - number_of_passes
	loged.write('%s test(s) undertaken\n%s Passed, %s Failed\n'%(number_of_tests,number_of_passes,number_of_fails))
	print_info('%s test(s) undertaken\n%s Passed, %s Failed\n'%(number_of_tests,number_of_passes,number_of_fails))
	loged.writelines(red_res)
	loged.close()
	
	return pass_state