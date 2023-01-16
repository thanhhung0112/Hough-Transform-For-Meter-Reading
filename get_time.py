import time 

def get_current_time():
    """
    It takes the current time, and returns it in a format that is easy to read
    :return: The current time in the format of hour, minute, second, day, month, year.
    """
    current_time = time.localtime()

    year = current_time[0]
    month = current_time[1]
    day = current_time[2]
    hour = current_time[3]
    minute = current_time[4]
    second = current_time[5]

    saved_time = f'{hour}h {minute}m {second}s {day}/{month}/{year}'
    print(saved_time)
    return saved_time

