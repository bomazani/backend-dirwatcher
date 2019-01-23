#!/usr/bin/env/python
# -*- coding: utf-8 -*-

__author__ = "bomazani with mob coding help on logging & search_file"


import logging
import datetime
import time
import argparse
import os

logger = logging.getLogger(__name__)


def watch_directory(args):
    """ Sets parsing intervals & handles errors """
    watching_files = {}
    logger.info('Watching directory: {}, File Ext: {}, '
                'Poling Interval: {}, Magic Text: {}'.format(
                 args.path, args.ext, args.interval, args.magic))

    while True:
        time.sleep(args.interval)
        try:
            remove_files(args.path, watching_files, args.ext)
            add_files(args.path, args.ext, watching_files)
            search_file(args.path, watching_files, args.magic)
        except OSError as e:
            logger.error(e)
            logger.warn('Retrying in 3 seconds...')
            time.sleep(3)
        except KeyboardInterrupt:
            break
    logger.debug('Exited Main Loop')


def remove_files(my_path, watching_files, ext):
    """ Searches for files no longer in the directory
    & removes from watching_files """
    files_to_delete = []
    path_files = os.listdir(my_path)
    for file_name in watching_files:
        if file_name in path_files:
            continue
        else:
            files_to_delete.append(file_name)
    for file in files_to_delete:
        del watching_files[file]
        logger.info('Removed {} from watching_files'.format(file_name))
    return watching_files


def add_files(my_path, ext, watching_files):
    """ Searches directory for new files & adds to watching_files """
    for file_name in os.listdir(my_path):
        if file_name.endswith(ext) and file_name not in watching_files:
            watching_files[file_name] = 0
            logger.info('Added {} to {}'.format(file_name, 'watching_files'))
    return watching_files


def search_file(directory_path, watching_files, magic_word):
    """ Itterates through each file in watching_files & sets absolute path."""
    for file_name in watching_files:
        abs_file = os.path.join(directory_path, file_name)
        starting_line = watching_files[file_name]
        watching_files[file_name] = find_magic(abs_file,
                                               starting_line,
                                               magic_word
                                               )


def find_magic(file_name, starting_line, magic_word):
    """ Jumps to starting line in file and searches for magic_word """
    with open(file_name) as f:
        line_num = 0
        for line_num, line in enumerate(f, 1):
            if line_num > starting_line and magic_word in line:
                logger.info('File: {} Found {} on line number: {}'
                            .format(os.path.basename(file_name),
                                    magic_word, line_num))
    return line_num


def create_parser():
    """ Creates and returns an argparse cmd line option parser """
    parser = argparse.ArgumentParser()
    parser.add_argument('-e', '--ext', type=str, default='.txt',
                        help='Text file extension to watch')
    parser.add_argument('-i',  '--interval', type=float,
                        default=1.0, help='Number of seconds between polling')
    parser.add_argument('path', help='Directory path to watch')
    parser.add_argument('magic', help='String to watch for')
    return parser


def main():
    """ Implements dirwatcher.py, logs starting and ending times. """
    logging.basicConfig(format='%(asctime)s.%(msecs)03d %(name)-12s '
                        '%(levelname)-8s %(message)s',
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
