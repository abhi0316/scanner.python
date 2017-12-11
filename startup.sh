#! /bin/bash
sudo python startupserver.py &
sudo python serialread.py &
sudo python rtmeerrupdate.py 
