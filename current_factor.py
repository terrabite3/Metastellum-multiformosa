#!/usr/bin/env python3


import time


if __name__ == '__main__':
    with open('epoch.txt', 'r') as epoch_file:
        epoch = float(epoch_file.readline())

    # The number of seconds to take to advance by "1"
    unit_time = 60 * 60 * 24

    current_time = time.time()
    delta_time = current_time - epoch

    frame_num = delta_time / unit_time + 1
    print(frame_num)
