#!/usr/bin/python3

import numpy as np
import numpy.random as rd
import time
from datetime import datetime

log_file='/tmp/system_info_pysym.log'


with open(log_file,'a+') as logger:
    counter=1
    # ok=True
    # while(ok):
    for time_id in range(1000):
        # time_id=datetime.utcnow()
        print('Computing...')
        logger.write(f'{time_id}-{counter}\n')
        time.sleep(3)
        counter+=1

    

