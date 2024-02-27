#!/usr/bin/env python3
# coding: utf-8

__author__ = 'Mário Antunes'
__version__ = '0.1'
__email__ = 'mariolpantunes@gmail.com'
__status__ = 'Development'


import argparse
import csv
import logging
import os
import pathlib
import random
import re
import warnings

import numpy as np
import tqdm
# Library used to speedup computation
from joblib import parallel_backend
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from sklearn.exceptions import ConvergenceWarning
# Import the necessary models
from sklearn.linear_model import SGDClassifier
from sklearn.metrics import matthews_corrcoef
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.tree import DecisionTreeClassifier

warnings.filterwarnings(action='ignore', category=ConvergenceWarning)
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)


def main(args):
    np.seterr(invalid='ignore')
    # random seeds for the multiple iteration
    random_seeds=[3,7,11]

    # create the path to the input folder
    folder = pathlib.Path(args.i)

    # load MNIST test dataset
    test_dataset = np.loadtxt(args.t, delimiter=',')
    x_test = test_dataset[:, 1:]
    y_test = test_dataset[:, 0]

    # store the output into a csv file
    with open(args.o, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(['seed', 'model', 'malicious', 'dataset_len', 'mcc'])

        for r in tqdm.tqdm(random_seeds):
            # set random seeds
            random.seed(r)
            np.random.seed(r)

            # List of models names and models algorithms
            clf_lr = SGDClassifier(loss='log_loss', penalty='l2', random_state=r)
            clf_svm_linear = SGDClassifier(loss='hinge', penalty='l2', random_state=r)
            clf_knn_1 = KNeighborsClassifier(n_neighbors=1)
            clf_knn_3 = KNeighborsClassifier(n_neighbors=3)
            clf_knn_5 = KNeighborsClassifier(n_neighbors=5)
            clf_knn_7 = KNeighborsClassifier(n_neighbors=7)
            clf_knn_9 = KNeighborsClassifier(n_neighbors=9)
            clf_dt = DecisionTreeClassifier(random_state=r)
            clf_ann = MLPClassifier(activation='relu', solver='adam', random_state=r, verbose=False)

            models = [
                ('LR',  clf_lr), ('SVM', clf_svm_linear),
                ('KNN(1)', clf_knn_1), ('KNN(3)', clf_knn_3), ('KNN(5)', clf_knn_5), ('KNN(7)', clf_knn_7), ('KNN(9)', clf_knn_9),
                ('DT',  clf_dt), ('ANN', clf_ann),
                ('RF',  RandomForestClassifier(random_state=r)),
                ('VF(hard)', VotingClassifier(estimators=[('lr', clf_lr), ('knn_3', clf_knn_3), ('dt', clf_dt), ('ann', clf_ann)], voting='hard')),
                ('VF(soft)', VotingClassifier(estimators=[('lr', clf_lr), ('knn_3', clf_knn_3), ('dt', clf_dt), ('ann', clf_ann)], voting='soft'))
            ]

            for i in tqdm.tqdm(range(0, args.l+1, round(args.bot_per*args.l)), leave=False):

                # load train dataset
                dataset_files = [folder / f'{i}' / f for f in os.listdir(folder / f'{i}') if re.search(f'dataset_[0-9]+.csv', f)]
                dataset_files = sorted(dataset_files)

                train_dataset = None

                for file in tqdm.tqdm(dataset_files, leave=False):
                    with parallel_backend('loky'):
                        temp = np.loadtxt(file, delimiter=',')
                        if train_dataset is None:
                            train_dataset = temp
                        else:
                            train_dataset = np.concatenate((train_dataset, temp))

                        x_train = train_dataset[:, 1:]
                        y_train = train_dataset[:, 0]

                        # For each model
                        for model in models:
                            model[1].fit(x_train, y_train)
                            predictions = model[1].predict(x_test)
                            mcc = matthews_corrcoef(y_test, predictions)

                            writer.writerow([r, f'{model[0]}', i, len(train_dataset), mcc])
                        f.flush()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate Predictions surface from the dataset')
    parser.add_argument('-i', type=str, help='captcha dataset folder', default='results')
    parser.add_argument('-l', type=int, help='number of atackers', default=20)
    parser.add_argument('--bot_per', type=float, help='step percentage for the number of malicious users', default=0.05)
    parser.add_argument('-t', type=str, help='MNIST test dataset', default='dataset/mnist_test.csv')
    parser.add_argument('-o', type=str, help='output file', default='output.csv')
    args = parser.parse_args()

    main(args)
