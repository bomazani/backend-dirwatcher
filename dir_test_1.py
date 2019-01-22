#!/usr/bin/env/python
# -*- coding: utf-8 -*-

__author__ = "bomazani with help in mob coding"

# github, gitignore folder for *.log, *.txt, .vscode/,
# Add README : Checkout Morgan's ReadMe.

import logging
import datetime
import time
import argparse
import os
# import sys
logger = logging.getLogger(__file__)


def watch_directory(args):
    watching_files = {}
    # the keys are going to be the actual file names
    # and the values will be the line# you last searched/read._
    logger.info('Watching directory: {}, File Ext: {}, Poling Interval: {}, Magic Text: {}'.format(
                args.path, args.ext, args.interval, args.magic))
    path = args.path
    ext = args.ext
    magic_word = args.magic

    while True:
        try:
            logger.info('Inside Watch Loop')
            time.sleep(args.interval)
            remove_files(path, watching_files)
            add_files(path, ext, watching_files)
            search_file(path, magic_word)
        except KeyboardInterrupt:
            break


def remove_files(path, watching_files, ext):
    """ Search for files no longer in the directory
    & remove from watching_files """
    files_to_delete = []
    path_files = os.listdir(path)
    for file_name in watching_files:
        if file_name in path_files:
            continue
        else:
            files_to_delete.append(file_name)
    for file in files_to_delete:
        del watching_files[file]
        logger.info('Removed {} from watching_files'.format(file_name))
    return watching_files


def add_files(path, ext, watching_files):
    """ Search directory for new files & add to watching_files """
    for file_name in os.listdir(path):
        if file_name.endswith(ext):
            watching_files[file_name] = 1
            logger.info('Added {} to {}'.format(file_name, 'watching_files'))
    return watching_files


def search_file(path, watching_files, magic_word):

    for file_name, starting_line in path:
        with open(file_name) as f:
            for line_number, line in enumerate(f, 1):
                if line_number > starting_line:
                    if magic_word in line:
                        logger.info('Found {} on line number: {}'.format(
                                    magic_word, line_number))
            file_name.starting_line = line_number


def create_parser():
    # parser = argparse.create_parser()
    parser = argparse.ArgumentParser()
    parser.add_argument('-e', '--ext', type=str, default='.txt',
                        help='Text file extension to watch')
    parser.add_argument('-i',  '--interval', type=float,
                        default=1.0, help='Number of seconds between polling')
    parser.add_argument('path', help='Directory path to watch')
    parser.add_argument('magic', help='String to watch for')
    return parser


def main():
    logging.basicConfig(filename='test1.log',
                        format='%(asctime)s.%(msecs)03d %(name)-12s'
                        '%(levelname)-8s [%(threadName)-12s] %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    logger.setLevel(logging.DEBUG)
    app_start_time = datetime.datetime.now()
    logger.info(
        '\n'
        '--------------------------------------------------\n'
        '       Running {0}\n'
        '       Started on {1}\n'
        '--------------------------------------------------\n'
        .format(__file__, app_start_time.isoformat())
    )
    parser = create_parser()
    args = parser.parse_args()
    watch_directory(args)
    uptime = datetime.datetime.now()-app_start_time
    logger.info(
        '\n'
        '--------------------------------------------------\n'
        '       Stopped {0}\n'
        '       Uptime was {1}\n'
        '--------------------------------------------------\n'
        .format(__file__, str(uptime))
    )


if __name__ == '__main__':
    main()
