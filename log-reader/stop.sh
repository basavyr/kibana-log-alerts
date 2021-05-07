ps aux | grep dfcti
ps aux | grep dfcti | awk '{print $2}' | xargs -n 1 kill -9 > /dev/null 2>&1
ps aux | grep dfcti
