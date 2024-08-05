'''
This block can be used to print information to the screen or not, as the case may be
It is basically a wrapper, with the debug set at one point only
'''

from __future__ import print_function


class display_info:
    debug = 0
    def set_debug(self,todebug):
        self.debug = todebug
    def tpontp(self,string,end,**kwargs):
        if self.debug == 1:
            print(string,end=end)

global printing 
printing = display_info()   

def set_debug(debug,**kwargs):
    global printing 
    try:
        todebug = debug
    except:
        todebug = 0
    printing.set_debug(todebug)

def print_info(string,**kwargs):
    global printing
    try:
        end = kwargs['end']
    except:
        end = '\n'
    if string == '':
        pass
    else:
        printing.tpontp(string,end)
        
    
