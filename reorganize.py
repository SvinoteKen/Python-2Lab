import sys
import os
import argparse
import pathlib
import time
import shutil

def create_parser(args=None) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', nargs=1, default=pathlib.Path.cwd(), type=str)
    parser.add_argument('--days', nargs=1, default=0, type=int)
    parser.add_argument('--size', nargs=1, default=4096, type=int)
    namespace = parser.parse_args(args)
    return namespace.source,namespace.days,namespace.size


rootdir, days, size = create_parser(sys.argv[1:])

cur_time = int(time.strftime('%j', time.localtime()))

files = [os.path.join(rootdir,f) for f in os.listdir(rootdir) if os.path.isfile(os.path.join(rootdir,f))]
dates = {file : int(time.strftime('%j', time.gmtime(os.path.getmtime(file)))) for file in files}
archive = [k for k, v in dates.items() if cur_time - v > days]

if archive:
    pathlib.Path.mkdir(pathlib.Path.cwd() / 'Archive')
    for prev in archive:
        shutil.move(prev, pathlib.Path.cwd() / 'Archive')

sizes = {file : os.path.getsize(file) for file in files}
small = [k for k, v in sizes.items() if v < size]

if small:
    pathlib.Path.mkdir(pathlib.Path.cwd() / 'Small')
    for prev in small:
        shutil.move(prev, pathlib.Path.cwd() / 'Small')
