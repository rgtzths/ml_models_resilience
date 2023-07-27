#!/usr/bin/env python3
# coding: utf-8

__author__ = 'Mário Antunes'
__version__ = '0.1'
__email__ = 'mariolpantunes@gmail.com'
__status__ = 'Development'


import argparse
import enum
import logging
import statistics

import pandas as pd
import plotly.graph_objects as go
import tqdm
from tqdm.contrib import tzip

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)


class Aggregation(enum.Enum):
    min = 'min'
    max = 'max'
    mean = 'mean'
    median = 'median'

    def __str__(self):
        return self.value


def multi_plot(df, args, addAll = True):
    fig = go.Figure()

    # Get the models within the CSV file
    if not args.m: 
        models = df['model'].unique().tolist()
    else:
        models = args.m
    
    # Generate all the data for plotly
    for m in tqdm.tqdm(models):
        model_data = df.loc[df['model']==m]
        data_x = [round(x/20,2) for x in model_data['malicious'].tolist()]
        data_y = [round(x/60000,2) for x in model_data['dataset_len'].tolist()]

        data_z = []
        for i, j in tzip(model_data['malicious'].tolist(), model_data['dataset_len'].tolist(), leave=False):
            temp_data = model_data.loc[(model_data['malicious']==i) & (model_data['dataset_len']==j),['mcc']]
            
            if args.a is Aggregation.max:
                result = max(temp_data['mcc'].tolist())
            elif args.a is Aggregation.min:
                result = min(temp_data['mcc'].tolist())
            elif args.a is Aggregation.mean:
                result = statistics.mean(temp_data['mcc'].tolist())
            else:
                result = statistics.median(temp_data['mcc'].tolist())

            data_z.append(result)

        fig.add_trace(
            go.Scatter3d(
                x=data_x,
                y=data_y,
                z=data_z,
                mode='markers',
                marker_color = models.index(m),
                name = m
            )
        )

    axis = dict(range = [-0.1, 1])

    camera = dict(
        center=dict(x=0, y=0, z=0),
        eye=dict(x=-0.1, y=2, z=0.4)
    )

    fig.update_layout(scene=dict(zaxis = axis), scene_camera=camera)
    fig.update_layout(scene = dict(
                    xaxis_title='% of malicious users',
                    yaxis_title='% of training examples',
                    zaxis_title='MCC'))
    
    fig.update_layout(
        height=700,
        width=800,
        margin=dict(t=0, b=0, l=0, r=0),
    )
    
    button_all = dict(label = 'All', method = 'restyle', args = [{'visible': [True]*len(models), 'title': 'All', 'showlegend':True}])

    def create_layout_button(column):
        visible = []
        for m in models:
            if m == column:
                visible.append(True)
            else:
                visible.append(False)
        return dict(label = column, method = 'restyle', args = [{'visible': visible, 'title': column, 'showlegend': True}])
    
    buttons = ([button_all] * addAll) + list(map(lambda column: create_layout_button(column), models))
    
    if args.f == "pdf":
        fig.write_image(args.o)
    elif args.f == "html":
        fig.write_html(args.o, include_plotlyjs=False, include_mathjax=False, full_html=False)
        fig.update_layout(updatemenus=[go.layout.Updatemenu(active = 0, buttons = buttons, x=0.1, xanchor="left", y=1.1, yanchor="top")])
    else:
        fig.update_layout(updatemenus=[go.layout.Updatemenu(active = 0, buttons = buttons, x=0.1, xanchor="left", y=1.1, yanchor="top")])
        fig.show(renderer=args.f)


def main(args):
    # load CSV
    data = pd.read_csv(args.i, header = 0)
    multi_plot(data,args)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Plot data from the ML dataset')
    parser.add_argument('-i', type=str, help='output dataset CSV', default='output.csv')
    parser.add_argument('-a', type=Aggregation, choices=list(Aggregation), default='min')
    parser.add_argument('-f', type=str, help="Choose the format of the image (html, pdf, or browser)", default='browser')
    parser.add_argument('-o', type=str, help="Output file name", default='plots/figure1.pdf')
    parser.add_argument('-m', type=str, nargs="+", help="Models to consider", default=None)
    args = parser.parse_args()
    
    main(args)