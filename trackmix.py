from os import path, remove
from sys import argv
import argparse
import glob
from pathlib import Path
import subprocess

music: list = glob.glob(f"{Path.cwd() / 'music_mix' / '*.mp3'}")

def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--source', required=True, type=str)
    parser.add_argument('-d', '--destination', default='mix.mp3', type=str)
    parser.add_argument('-c', '--count', default=len(music), type=int)
    parser.add_argument('-f', '--frame', default=30, type=int)
    parser.add_argument('-l', '--log', action='store_true', default=False)
    parser.add_argument('-e', '--extended', action='store_true', default=False)
    return parser

if __name__ == '__main__':
    parser = create_parser()
    namespace: argparse.Namespace = parser.parse_args(argv[1:])

    for i in range(namespace.count):
        subprocess.call(
            f'ffmpeg -i "{music[i]}" -t {namespace.frame} \
            "{Path.cwd() / "music_mix" / f"tmp_{i}.mp3"}" -y -loglevel quiet'
            )
        if namespace.log:
            print('file {0} has completed'.format(music[i][music[i].rfind("\\")+1:]))

    tmps: list = glob.glob(f"{Path.cwd() / 'music_mix' / 'tmp*.mp3'}")
    
    if namespace.extended:
        for i, tmp in enumerate(tmps):
            subprocess.call(
                f'ffmpeg -i "{tmp}" \
                -af "afade=t=in:ss=0:d=3,afade=t=out:st={namespace.frame-3}:d=3" \
                "{Path.cwd() / "music_mix" / f"tmp_new{i}.mp3"}" -y -loglevel quiet'
                )
            remove(tmp)
        tmps: list = glob.glob(f"{Path.cwd() / 'music_mix' / 'tmp_new*.mp3'}")

    with open(f'{Path.cwd() / "music_mix" / "files.txt"}', 'w') as f:
        f.writelines(f"file '{tmp}'\n" for tmp in tmps)

    subprocess.call(
        f'ffmpeg -f concat -safe 0 -i \
        "{Path.cwd() / "music_mix" / "files.txt"}" -c copy \
        "{Path.cwd() / "music_mix" / f"{namespace.destination}"}" -y -loglevel quiet', shell=True
        )

    if namespace.log and path.exists(Path.cwd() / "music_mix" / f"{namespace.destination}"):
        print(f'file {namespace.destination} has created')

    remove(Path.cwd() / "music_mix" / "files.txt")
    for tmp in tmps:
        remove(tmp)