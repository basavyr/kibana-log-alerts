ps aux | grep dfcti
ps aux | grep dfcti | awk '{print $2}' | xargs -n 1 kill -9
ps aux | grep dfcti
