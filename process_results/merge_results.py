#!/usr/bin/env python3
# coding: utf-8

__author__ = 'Rafael Teixeira'
__version__ = '0.1'
__email__ = 'rafaelgteixeira@ua.pt'
__status__ = 'Development'

import argparse

import pandas as pd
import tqdm
from tqdm.contrib import tzip


# for each model create a seperate csv with the models used in different datasets
def merge_datasets(dfs, output_folder):
    df = pd.read_csv(dfs["random"], index_col=None, header=0)
    models = df['model'].unique().tolist()
    models.sort()

    for m in tqdm.tqdm(models):
        final_df = pd.DataFrame({"model" : [], "malicious" : [], "dataset_len" : [], "mcc" : []})

        for df in dfs:
            data = pd.read_csv(dfs[df], index_col=None, header=0)
            model_data = data.loc[data['model']==m]
            data_x = model_data['malicious'].tolist()
            data_y = model_data['dataset_len'].tolist()

            data_z = []
            for i, j in tzip(data_x, data_y, leave=False):
                temp_data = model_data.loc[(model_data['malicious']==i) & (model_data['dataset_len']==j),['mcc']]
                
                result = max(temp_data['mcc'].tolist())

                data_z.append(result)

            final_df = pd.concat([
                pd.DataFrame({
                    "model" : [m+"_"+df]*len(data_x),
                    "malicious" : data_x,
                    "dataset_len" : data_y,
                    "mcc" : data_z}
                    ),
                final_df]
                )

        final_df.to_csv(output_folder+m+".csv", index=None)


merge_datasets(
    {"flip" : "results_no_voting/flip/flip_contaminated.csv", 
    "random" : "results_no_voting/random/random_contaminated.csv",
    "switch" : "results_no_voting/switch/switch_contaminated.csv"},
     "results_no_voting/merged/")