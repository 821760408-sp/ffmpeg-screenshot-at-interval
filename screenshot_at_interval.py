#!/usr/bin/env python

import argparse
import datetime
import subprocess
import time

parser = argparse.ArgumentParser(description='Script to extract either a number of {n} screenshots from a video, or extract an indefinite amount of screenshots at an interval of {i} seconds.')
group = parser.add_mutually_exclusive_group()
group.add_argument('-n', dest='num', type=int, help='specify the number of screenshots to extract from video.')
group.add_argument('-s', dest='interval', type=int, help='specify the interval of screenshots to extract from video.')
parser.add_argument('-i', dest='input', required=True, help='specify input video file.')
args = parser.parse_args()


def get_video_duration(filename):
    with subprocess.Popen(['ffprobe', filename], stdout=subprocess.PIPE, stderr=subprocess.STDOUT) as proc:
        result = [x.decode('utf8') for x in proc.stdout.readlines() if 'Duration' in x.decode('utf8')]
    return result


if __name__=='__main__':
    interval = args.interval
    filename = args.input
    ss_num = None
    duration = get_video_duration(filename)[0].split(' ')[3].strip(',')

    duration = time.strptime(duration[:-3], '%H:%M:%S')
    duration = datetime.timedelta(hours=duration.tm_hour,
            minutes=duration.tm_min,
            seconds=duration.tm_sec).total_seconds()  # in seconds
    if not interval:
        ss_num = args.num  # number of screenshot
        interval = duration // ss_num

    if not ss_num:
        ss_num = int(duration // interval)

    start_time_in_sec = 0
    i = 0
    times_in_sec = [start_time_in_sec + interval * i for i in range(ss_num)]

    timestamps = [time.strftime('%H:%M:%S', time.gmtime(x)) for x in times_in_sec]

    for i in range(len(timestamps)):
        with subprocess.Popen(['ffmpeg', '-ss', timestamps[i], '-i', filename, '-vframes', '1', 'out{0:02}.png'.format(i)]) as proc:
            pass

