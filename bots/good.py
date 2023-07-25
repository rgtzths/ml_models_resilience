#!/usr/bin/env python3
# coding: utf-8

__author__ = 'Rafael Simões'
__version__ = '0.1'
__email__ = 'rafaeljsimoes@ua.pt'
__status__ = 'Development'


import argparse
import logging

import requests
from tqdm import tqdm

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)


def reply(ticket, labels):
    return ticket, labels


def main(options):
    logger.info('Bot start')

    stats = []
    for _ in tqdm(range(options.i)):
        captcha_data = requests.get(f'{options.u}/captcha').json()
        ticket = captcha_data.get('ticket')
        labels = captcha_data.get('labels')

        ticket, labels = reply(ticket, labels)

        status = requests.post(f'{options.u}/captcha', json={'ticket': ticket, 'labels': labels}).json().get('status')
        stats.append(status)

    logger.info(f'Hit rate: {sum(stats) / len(stats)}')
    logger.info('Bot done')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Captcha Bot (Good)')
    parser.add_argument('-u', type=str, help='base url', default='http://localhost:9000')
    parser.add_argument('-i', type=int, help='Iterations', default="10000")
    args = parser.parse_args()

    main(args)
