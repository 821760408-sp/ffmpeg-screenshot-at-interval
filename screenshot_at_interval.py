#!/usr/bin/env python

import argparse
import datetime
import subprocess
import time

parser = argparse.ArgumentParser(description='Script to extract either a number of {n} screenshots from a video, or extract an indefinite amount of screenshots at an interval of {i} seconds.')
group = parser.add_mutually_exclusive_group()
group.add_argument('-n', dest='num', type=int, help='specify the number of screenshots to extract from video.')
group.add_argument('-i', dest='interval', type=int, help='specify the interval of screenshots to extract from video.')
parser.add_argument('-s', dest='start_time', type=float, default=0.0, help='specify the starting time of video extracting.')
parser.add_argument('-f', dest='input', required=True, help='specify input video file.')
args = parser.parse_args()


def get_video_duration(filename):
    with subprocess.Popen(['ffprobe', filename], stdout=subprocess.PIPE, stderr=subprocess.STDOUT) as proc:
        result = [x.decode('utf8') for x in proc.stdout.readlines() if 'Duration' in x.decode('utf8')]
    return result


if __name__=='__main__':
    screenshot_num = args.num
    interval = args.interval
    start_time_in_sec = args.start_time
    filename = args.input
    duration = get_video_duration(filename)[0].split(' ')[3].strip(',')

    duration = time.strptime(duration[:-3], '%H:%M:%S')
    duration = datetime.timedelta(hours=duration.tm_hour,
            minutes=duration.tm_min,
            seconds=duration.tm_sec).total_seconds()  # in seconds
    if not interval:
        interval = (duration - start_time_in_sec) // screenshot_num

    if not screenshot_num:
        screenshot_num = int((duration - start_time_in_sec) / interval)

    i = 0
    times_in_sec = [start_time_in_sec + interval * i for i in range(screenshot_num)]

    timestamps = [time.strftime('%H:%M:%S', time.gmtime(x)) for x in times_in_sec]

    for i in range(len(timestamps)):
        with subprocess.Popen(['ffmpeg', '-ss', timestamps[i], '-i', filename, '-frames:v', '1', 'out{0:04}.png'.format(i)]) as proc:
            pass

