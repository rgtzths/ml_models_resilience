#!/usr/bin/env python3
# coding: utf-8

__author__ = 'Mário Antunes'
__version__ = '0.1'
__email__ = 'mariolpantunes@gmail.com'
__status__ = 'Development'


import argparse
import csv
import logging
import pathlib
import random

import tqdm

import bots.evil as evil
import bots.good as good
from bots.evil import Behavior
from dataset import Dataset

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)


def main(args):
    labels = []
    data = []

    # load the data
    with open(args.i) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',', quoting=csv.QUOTE_NONNUMERIC)
        for row in csv_reader:
            labels.append(row[0])
            data.append(row[1:])
    
    # create a output path
    output = pathlib.Path(args.o)

    for i in tqdm.tqdm(range(0, args.l+1, round(args.bot_per*args.l))):
        # ratio of bots
        bad_bots = i
        # create folder for this loop results
        pathlib.Path(output / f'{bad_bots}').mkdir(parents=True, exist_ok=True)
        # create a clean dataset
        dataset = Dataset(data, 
                labels, 
                path=output / f'{bad_bots}', 
                base=args.b, 
                step=args.s, 
                left=args.left, 
                right=args.right, 
                n_votes=args.v)

        
        bot_counter = 0

        # generate a random list of evil / good bots.
        evil_bots = random.sample(range(args.l), bad_bots)
        while(dataset.collected_labels + dataset.curated_labels_size < len(dataset.data)):
            captcha = dataset.get_captcha()
            t = captcha['ticket']
            l = captcha['labels']

            if bot_counter in evil_bots:
                t, l = evil.reply(t, l, args.left, args.behavior)
            else:
                t, l = good.reply(t, l)

            check, store = dataset.check_captcha(t, l)

            bot_counter = (bot_counter+1)%args.l

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate Datasets')
    parser.add_argument('-i', type=str, help='MNIST train dataset', default='dataset/mnist_train.csv')
    parser.add_argument('-l', type=int, help='number of max malicious users', default=20)
    parser.add_argument('-b', type=float, help='base percentage for the Dataset', default=.3)
    parser.add_argument('-s', type=float, help='step percentage for the Dataset incement', default=.1)
    parser.add_argument('--left', type=int, help='size of the left part of the captcha (known)', default=3)
    parser.add_argument('--right', type=int, help='size of the right part of the captcha (unknown)', default=3)
    parser.add_argument('--behavior', type=Behavior, choices=list(Behavior), help='Evil bot behavior', default='random')
    parser.add_argument('--bot_per', type=float, help='step percentage for the number of malicious users', default=0.05)
    parser.add_argument('-o', type=str, help='output folder', default='results')
    parser.add_argument('-v', type=int, help='number of votes', default=1)
    parser.add_argument('--seed', type=int, help='seed to standardize runs', default=7)
    args = parser.parse_args()

    random.seed(args.seed)
    main(args)