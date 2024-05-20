import time
import get_time
import calendar_api

while True:
    print('Updating events list...\n')
    calendar_api.get_events()
    print('\nLast Update: {}'.format(get_time.get_local_time()))
    
    time.sleep(10)
    print('\n\n\n\n\n\n\n\n\n')