#!/usr/bin/env python3
# coding: utf-8

__author__ = 'Rafael Simões'
__version__ = '0.1'
__email__ = 'rafaeljsimoes@ua.pt'
__status__ = 'Development'


import argparse
import logging
from enum import Enum
from random import choice

import requests
from tqdm import tqdm

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)


class Behavior(Enum):
    random = 'random'
    flip = 'flip'
    switch = 'switch'

    def __str__(self):
        return self.value

def random_behavior(label):
    possible_values = list(range(10))
    possible_values.pop(int(label))
    return float(choice(possible_values))

def switch_behavior(label):
    return (label + 1) % 10

def flip_behavior(label):
    similarity = [(1.0, 7.0), (0.0, 8.0), (2.0, 5.0), (6.0, 9.0), (3.0, 8.0), (4.0, 9.0)]
    for v in similarity:
        if label in v:
            return v[0] if label != v[0] else v[1]

    # return switch_behavior(label)

def reply(ticket, labels, left, behavior=Behavior.random):
    if behavior is Behavior.random:
        new_labels = labels[:left] + [random_behavior(label) for label in labels[left:]]
    elif behavior is Behavior.flip:
        new_labels = labels[:left] + [flip_behavior(label) for label in labels[left:]]
    else:
        new_labels = labels[:left] + [switch_behavior(label) for label in labels[left:]]

    return ticket, new_labels


def main(options):
    logger.info('Bot start')

    stats = []
    for _ in tqdm(range(options.i)):
        captcha_data = requests.get(f'{options.u}/captcha').json()
        ticket = captcha_data.get('ticket')
        labels = captcha_data.get('labels')

        #mid = len(labels) // 2
        ticket, labels = reply(ticket, labels, args.left, args.b)

        status = requests.post(f'{options.u}/captcha', json={'ticket': ticket, 'labels': labels}).json().get('status')
        stats.append(status)

    logger.info(f'Hit rate: {sum(stats) / len(stats)}')
    logger.info('Bot done')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Captcha Bot (Evil)')
    parser.add_argument('-u', type=str, help='base url', default='http://localhost:9000')
    parser.add_argument('-i', type=int, help='Iterations', default="10000")
    parser.add_argument('-b', type=Behavior, choices=list(Behavior), help='bot behavior', default='random')
    parser.add_argument('--left', type=int, help='size of the left part of the captcha (known)', default=3)
    parser.add_argument('--right', type=int, help='size of the right part of the captcha (unknown)', default=3)
    args = parser.parse_args()

    main(args)
