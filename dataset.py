# coding: utf-8

__author__ = 'Mário Antunes'
__version__ = '0.1'
__email__ = 'mariolpantunes@gmail.com'
__status__ = 'Development'


import csv
import glob
import os
import random
import re
import uuid
from pathlib import Path
from threading import Lock


def store_labels(path, labels, data):
    Path(path).mkdir(parents=True, exist_ok=True)  # Create dir if not exists
    dataset_files = [f for f in os.listdir(path) if re.search(f'dataset_[0-9]+.csv', f)]
    dataset_files = sorted(dataset_files, key=str.lower)

    if len(dataset_files) > 0:
        last_file = dataset_files[-1]
        idx = int(last_file[8:11])
    else:
        idx = 0
    dataset_new_file = f'dataset_{idx + 1:03d}.csv'

    with open(f'{path}/{dataset_new_file}', 'w') as csv_file:
        writer = csv.writer(csv_file, delimiter=',', quoting=csv.QUOTE_NONNUMERIC)
        for idx, label in labels:
            row = [label]
            row.extend(data[idx])
            writer.writerow(row)


class Dataset:
    def __init__(self, data, labels, path='bots_dataset', base=0.3, step=0.1, left=2, right=2, n_votes=3):
        # save all data and labels
        self.data = data
        self.all_labels = labels
        self.labels = []
        self.path = path
        self.step = step
        self.left = left
        self.right = right
        # compute the percentage of curated labels
        self.curated_labels_size = int(round(len(data) * base))
        # create the base idx to the non-curated labels and the counter
        self.base_idx = self.curated_labels_size
        self.counter = 0
        self.n_votes = n_votes
        self.cache = {}
        self.votes = {}
        self.collected_labels = 0
        self.wrong_labels = 0
        # create the mutex for thread safety
        self.mutex = Lock()
        # store initial part of the dataset
        curated_labels = []
        for i in range(self.curated_labels_size):
            curated_labels.append((i, self.all_labels[i]))
        store_labels(self.path, curated_labels, self.data)

    def get_captcha(self):
        # get a ticket
        ticket = str(uuid.uuid4())
        # randomly select the indexes for left part of the captcha
        left_indexes = random.sample(range(self.curated_labels_size), self.left)

        self.mutex.acquire()
        try:
            # select the right part of the captcha
            right_indexes = []
            for _ in range(self.right):

                # increment the counter for the non curated labels, skiping those that already have N or more votes
                while(self.base_idx + self.counter in self.votes and len(self.votes[self.base_idx + self.counter]) >= self.n_votes):
                    self.counter = (self.counter + 1) % (len(self.data) - self.curated_labels_size)

                right_indexes.append(self.base_idx + self.counter)
                self.counter = (self.counter + 1) % (len(self.data) - self.curated_labels_size)

            # store the information within the cache
            self.cache[ticket] = (left_indexes, right_indexes)
        except:
            raise("Error")

        finally:
            self.mutex.release()

        # create captcha
        data = []
        for i in left_indexes:
            data.append(self.data[i])
        for i in right_indexes:
            data.append(self.data[i])

        labels = []
        for i in left_indexes:
            labels.append(self.all_labels[i])
        for i in right_indexes:
            labels.append(self.all_labels[i])

        captcha = {'ticket': ticket, 'left_idx': left_indexes, 'right_idx': right_indexes, 'data': data,
                   'labels': labels}

        # return the captcha
        return captcha

    def percentage(self):
        return len(self.labels) / self.uncurated()
        
    def uncurated(self):
        return len(self.data) - self.curated_labels_size

    def check_captcha(self, ticket, labels):
        check = store = False
        self.mutex.acquire()
        try:
            # pop data from cache
            left_indexes, right_indexes = self.cache.pop(ticket, ([], []))
            # recreate the left labels
            left_labels = []
            for i in left_indexes:
                left_labels.append(self.all_labels[i])

            # check the left labels
            if left_labels == labels[:self.left]:
                check = True
                # store the values to the right labels
                right_labels = labels[self.left:]

                for i in range(len(right_indexes)):
                    if right_indexes[i] in self.votes:
                        self.votes[right_indexes[i]].append(right_labels[i])                    
                        if len(self.votes[right_indexes[i]]) == self.n_votes: 
                            added = False
                            for label in self.votes[right_indexes[i]]:
                                if self.votes[right_indexes[i]].count(label) > self.n_votes / 2:
                                    self.labels.append((right_indexes[i], label))
                                    self.collected_labels += 1
                                    if self.all_labels[right_indexes[i]] != label:
                                        self.wrong_labels +=1
                                    added = True
                                    break

                            if not added:
                                del self.votes[right_indexes[i]]

                            # check the labels size and store is step is meet
                            if self.percentage() >= self.step:
                                store = True
                                store_labels(self.path, self.labels, self.data)
                                self.labels.clear()
                    else:
                        self.votes[right_indexes[i]] = [right_labels[i]]

                    if len(self.votes[right_indexes[i]]) == self.n_votes: 
                        added = False
                        for label in self.votes[right_indexes[i]]:
                            if self.votes[right_indexes[i]].count(label) > self.n_votes / 2:
                                self.labels.append((right_indexes[i], label))
                                self.collected_labels += 1
                                if self.all_labels[right_indexes[i]] != label:
                                    self.wrong_labels +=1
                                added = True
                                break

                        if not added:
                            del self.votes[right_indexes[i]]

                        # check the labels size and store is step is meet
                        if self.percentage() >= self.step:
                            store = True
                            store_labels(self.path, self.labels, self.data)
                            self.labels.clear()
        except:
            raise("Error")
        finally:
            self.mutex.release()

        return check, store

    def __str__(self):
        return f'({len(self.data)}; {self.curated_labels_size}; {len(self.labels)} ({self.percentage()}))'
