# -*- coding: utf-8 -*-
"""
Created on Wed Oct 27 08:53:19 2021

@author: FWillems
"""
import os, re, sys, getopt, subprocess
from datetime import datetime as d
import time as t

lmstat="lmutil"
lmopts="lmstat"

def print_usage():
    print ("Usage:")
    print (os.path.basename(__file__), '-f <feature> -c <lic_server>  -r <rrdfile>')

def main(argv):
    lic_server = ''
    feature = ''
    rrd_file = ''
    try:
        opts, args = getopt.getopt(argv,"hf:c:r:",["feature=","lic_server=", "rrd_file="])
        # Parse options
        for opt, arg in opts:
            if opt == '-h':
                print_usage()
                sys.exit()
            elif opt in ("-f", "--feature"):
                feature = arg
            elif opt in ("-c", "--lic_server"):
                lic_server = arg
            elif opt in ("-r", "--rrdfile"):
                rrd_file = arg    
        if not feature and not lic_server and not rrd_file :
            raise getopt.GetoptError("")
    except getopt.GetoptError:
        print_usage()
        exit
        sys.exit(2)
    Active = 0
    Taken = 0
    print ("Monitoring started")
    while True :    
        Starttime = t.time()
        #print (Starttime)
        # Spawn lmutil
        licenses=os.popen("%s %s -a -c %s -f %s" % (lmstat, lmopts, lic_server, feature))
        # Parse lines
        for line in licenses:
            if re.search("^Users of " + feature + ":.*$", line):
                # Test for line (Total of # licenses issued;  Total of # licenses in use)
                m=re.findall("([0-9]+) license", line)
                if m and len(m) == 2:
                    Taken =int(m[1])
                    if Taken > 0 and Active == 0 :
                        print ("License active %s" % feature)
                        Active = 1
                    else :
                        if Taken == 0 and Active == 1 :
                            print ("License unused %s" % feature)
                            Active = 0
                            
        Updatestr = '.\\rrdtool update %s %d:%d' %  (rrd_file, int(Starttime), Taken)
        if sys.version_info[0] > 2 and sys.version_info[1] > 4 :
            try:
                subprocess.run(Updatestr)
            except :
                print ( str(d.now()) + " Fileserver connection broken." )
        else :
            try:
                subprocess.getoutput(Updatestr)
            except :
                print ( str(d.now()) + " Fileserver connection broken." )
       
        #print (300 - (t.time()- Starttime)) 
        SleepPeriods = int((t.time()- Starttime)/300)+1
        t.sleep(SleepPeriods*300 - (t.time()- Starttime))      
        #t.sleep(300 - (t.time()- Starttime))
    


if __name__ == "__main__":
   main(sys.argv[1:])
