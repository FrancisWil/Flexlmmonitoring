# Flexlmmonitoring
Python source to monitor usage of flexlmlicenses and other. Data stored in RRD.

lmrrdrecorder.py : FLEXLM recorder. Records every 5 minutes the licenses in use of a specific feature.
cmrrdrecorder.py : Codemeter recorder. Records every 5 minutes the licenses in use on a specific code in the Webadmin of the server codemeter.
zoorrdrecorder.py : Zoo recorder. Records  every 5 minutes the licenses in use of Rhino on the Zoo server.
All data are stored in a RRD (round robin database see https://oss.oetiker.ch/rrdtool/doc/rrdtool.en.html
