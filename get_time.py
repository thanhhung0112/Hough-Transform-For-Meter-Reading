import time 

def get_current_time():
    current_time = time.localtime()

    year = current_time[0]
    month = current_time[1]
    day = current_time[2]
    hour = current_time[3]
    minute = current_time[4]
    second = current_time[5]

    saved_time = f'{hour}h {minute}m {second}s {day}/{month}/{year}'
    print(saved_time)

