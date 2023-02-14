# -*- coding: utf-8 -*-
"""
Created on Wed Oct 27 08:53:19 2021

@author: FWillems
"""
import os, re, sys, getopt, subprocess
from datetime import datetime as d
import time as t
import pandas as pd #use pandas as this can directly extract from a webpage.
import requests as rq

def print_usage():
    print ("Usage:")
    print (os.path.basename(__file__), '-c <lic_server>  -r <rrdfile>')

def main(argv):
    lic_server = ''
    feature = ''
    rrd_file = ''
    try:
        opts, args = getopt.getopt(argv,"hc:r:",["lic_server=", "rrd_file="])
        # Parse options
        for opt, arg in opts:
            if opt == '-h':
                print_usage()
                sys.exit()
            elif opt in ("-c", "--lic_server"):
                lic_server = arg
            elif opt in ("-r", "--rrdfile"):
                rrd_file = arg
        if not feature and not lic_server and not rrd_file :
            raise getopt.GetoptError("")
    except getopt.GetoptError:
        print_usage()
        #exit
        sys.exit(2)
    Active = 0
    Taken = 0
    OldTaken = 0
    print ("Monitoring started")
    while True :    
        Starttime = t.time()
        #print (Starttime)
        # Spawn lmutil
        url = 'http://'+lic_server+'/status'
        try :
            dfs = pd.read_html(url) #, attrs={'id': "0" })
            df = dfs[0]
            #'firm_code_content_table_5000057'})
            Taken = len(df[df['Status'] == 'In Use'])
            print (Taken)
        except :
            print ( str(d.now()) + " License page not reachable. Server %s active?" % (lic_server))
            Taken = OldTaken
            
            
        # Parse lines
        
        if Taken > 0 and Active == 0 :
            print ("Rhino licenses taken")
            OldTaken = Taken
            Active = 1
        else :
            if Taken == 0 and Active == 1 :
                print ("Rhino Licenses free")
                Active = 0
                            
        Updatestr = '.\\rrdtool update %s %d:%d' %  (rrd_file, int(Starttime), Taken)
        try:
            subprocess.run(Updatestr)
        except :
            print ( str(d.now()) + " Fileserver connection broken." )
        SleepPeriods = int((t.time()- Starttime)/300)+1
        t.sleep(SleepPeriods*300 - (t.time()- Starttime))         
# =============================================================================
#         if SleepTime > 0 :            
#             t.sleep(300 - (t.time()- Starttime))
#         else :
#             # time delay is greater than 5 minutes
#             # sleep to next 5 minute interval.
#             print ( str(d.now()) + " TimeDelay exceeded 5 minutes.")
#             t.sleep(600 - (t.time()- Starttime)) 
# =============================================================================
    
    


if __name__ == "__main__":
   main(sys.argv[1:])
