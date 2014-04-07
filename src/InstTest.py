from __future__ import print_function
from epics import PV
from CagetDatim import Caget_Datim
from CaputZero import Caput_Zero
from CamonitorInt import Camonitor_Int
from GenerateLog import GenerateLog
from PrintInfo import *
import unittest
import xml.etree.ElementTree as etree
import os

def instrument_test(kwargs):
    dir = os.path.dirname(__file__)
    try:
        test_desc = kwargs['tests']
    except:
        test_desc = os.path.join(dir,'TEST.xml')
    try:
        debug = kwargs['debug']
    except:
        debug = 0
    set_debug(debug)
    try:
        gen_log = kwargs['gen_log']
    except:
        gen_log = 1
    
    #Get the items from an XML document rather than hard code them here
    try:
        tree = etree.parse(test_desc)
    except:
        return 'No tests found'
    testdir = tree.findtext('test_directory')
    if testdir == None:
        testdir = os.path.join(os.environ['ICPVARDIR'],'logs/testlog')
    #Set a delay variable, hopefully this will allow for creating an unstable test environment at times
    node = tree.find('delay')
    try:
        delay = int(node.text)
    except:
        delay = 2
    
    #Generate a dictionary of the tests from the XML
    TESTS = {}
    test = tree.find('TESTS')
    if test == None:
        return 'No TESTS found'
    node = test.findall('TEST')
    testnum = 1
    for x in node:
        pvs = {}
        ttype = x.findtext('test-type')
        if ttype == None:
            ttype = 'Unknown'
        expval = x.findtext('expval')
        scope = x.findtext('scope')
        if scope == None:
            scope = 'Unknown'
        format = x.findtext('data-format')
        dtype = x.findtext('data-type')
        pvstouse = x.findtext('pvstouse')
        for pv in x.findall('pv'):
            pvs[pv.attrib['pvnum']]=pv.text
        TESTS[testnum] = (ttype,expval,scope,format,dtype,pvstouse,pvs)
        testnum = testnum + 1
    
    #Set up the test log file
    log_file = 'test_log.txt'
    logf = open(log_file, 'w')
    runner = unittest.TextTestRunner(logf, verbosity=1)
    
    #Class for the simplification of PV creation
    class pvrec:
        pvinst = ''
        val = ''
        
        def initpv(self, pvname):
            pvrec.pvinst = PV(pvname)
           
    #Set up the testing suite
    suite = unittest.TestSuite()
    loader = unittest.TestLoader()
    
    #Set up the PVs to use, and create the dictionary for later use
    actualpvs = {}
    
    #Get the PV names used from the test cases entered
    allpv_names = []
    for x,TEST in TESTS.iteritems():
        pvstouse = ('%s'%TEST[5])
        pvslist = pvstouse.split(',')
        all_pvs = TEST[6]
        for i in pvslist:
            pvname = all_pvs[i]
            testing = pvrec()
            testing.initpv(pvname)
            actualpvs[('%s,%s'%(x,i))] = testing.pvinst
        pvsintest = len(pvslist)
        updatedtest=list(TEST)
        updatedtest.append(pvsintest)
        TEST=tuple(updatedtest)
        TESTS[x]=TEST
    
    testdets = {}
    #Generate and run the tests
    for x,TEST in TESTS.iteritems():
        ttype = TEST[0]
        expval = TEST[1]
        scope = TEST[2]
        format = TEST[3]
        dtype = TEST[4]
        pvstouse = TEST[5]
        pvnames = TEST[6]
        pvsinlist = TEST[7]
        curr_test = 'Test %s: Type = %s, scope = %s'%(x,ttype,scope)
        print_info('Currently building %s\n' % curr_test)
        testdets[x] = curr_test
        logf.write(('Test %s: %s\n'%(x,TEST)))
        class IterationTests(unittest.TestCase):
            if ttype == 'Unknown':
                def test_unkown(self):
                    self.assertTrue(False, 'Unknown Test not actioned')
            if ttype =='Caget-Datim':
                def test_caget_datim(self):
                    Caget_Datim(self,x=x,pvstouse=pvstouse,actualpvs=actualpvs,format=format,expval=expval,pvsinlist=pvsinlist)
            if ttype =='Caput-Zero':
                def test_caput_zero(self):
                    Caput_Zero(self,x=x,pvstouse=pvstouse,actualpvs=actualpvs,expval=expval,delay=delay)
            if ttype =='Camonitor-Int':
                def test_camonitor_int(self):
                    Camonitor_Int(self,pvstouse=pvstouse,pvnames=pvnames)
        itersuite = unittest.TestLoader().loadTestsFromTestCase(IterationTests)
        print_info('Running Test...\n')
        runner.run(itersuite)
        
    logf.close()
    
    print_info('Tests Complete.')
    if gen_log == 1:
        print_info('Generating Log File.')
        pass_state = GenerateLog(testdir,log_file,TESTS,testdets)
    return pass_state

def inst_test(**kwargs):
    return instrument_test(kwargs)

def inst_test_msgs(**kwargs):
    kwargs['debug']=1
    return instrument_test(kwargs)

def main():
    pass_state = inst_test(debug = 1)
    print('Pass State = %s'%pass_state)
    
if __name__ == '__main__':
    main()