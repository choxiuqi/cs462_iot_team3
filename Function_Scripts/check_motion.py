''' This script will run continuosly and check for motion for the last 3 min
    if there is no motion for the last 3 min, we will reset the occupancy reading to 0
    this will replace the resetCounter() function in UpdateOccupancy_4b.py'''

def check_reset():
    

try:
    while True:
        time.sleep(1)
        check_reset()

except Exception as e:
    print(str(e))