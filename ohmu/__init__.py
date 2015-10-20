#!/usr/bin/env python

from os.path import abspath
import curses
import sys
import time
import click
from .fs import Scanner
from .views import Screen


class Ohmu(object):

    refresh_rate = 0.05

    def __init__(self, root_path):
        print("here", root_path)
        self.screen = Screen()
        self.scanner = Scanner(str(root_path))

        self.keep_running = True

    def start(self):
        try:
            self.scanner.start()
            self.screen.start()
            self.loop()
        except KeyboardInterrupt:
            pass
        except:
            self.screen.stop()
            raise
        self.screen.stop()

    def loop(self):
        start = time.time()
        last_tick = start
        self.screen.tick(start, self.scanner)
        while self.keep_running:
            self.process_input(self.screen.get_key_sequence())
            if not self.keep_running:
                break
            now = time.time()
            passed = now - last_tick
            if passed > self.refresh_rate:
                last_tick = now
                self.screen.tick(now, self.scanner)

    def process_input(self, key_sequence):
        if key_sequence in (ord('q'), Screen.ESC_KEY):
            self.keep_running = False
        elif key_sequence == curses.KEY_RESIZE:
            self.screen.update_size()

def main(name, path='.'):
    if name != '__main__':
        return
    root_path = abspath(path)
    print("dadad", root_path)
    Ohmu(root_path).start()


@click.command()
@click.option('--path', default='.', help='path for ohmu', nargs=1)
def entry_point(path):
    print(path)
    main('__main__', path)
