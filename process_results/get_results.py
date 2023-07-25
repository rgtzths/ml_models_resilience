import argparse

import pandas as pd
import tqdm
from tqdm.contrib import tzip


# Convert the results from the three runs in an average
def convert_to_average(df, output_file):
    models = df['model'].unique().tolist()
    models.sort()

    final_df = pd.DataFrame({"model" : [], "malicious" : [], "dataset_len" : [], "mcc" : []})

    for m in tqdm.tqdm(models):
        model_data = df.loc[df['model']==m]
        data_x = model_data['malicious'].tolist()
        data_y = model_data['dataset_len'].tolist()

        data_z = []
        for i, j in tzip(data_x, data_y, leave=False):
            temp_data = model_data.loc[(model_data['malicious']==i) & (model_data['dataset_len']==j),['mcc']]
            
            result = max(temp_data['mcc'].tolist())

            data_z.append(result)

        final_df = pd.concat([
            pd.DataFrame({
                "model" : [m]*len(data_x),
                "malicious" : data_x,
                "dataset_len" : data_y,
                "mcc" : data_z}
                ),
            final_df]
            )

    final_df.to_csv(output_file, index=None)

def get_results(file, output_file):
    f = open(output_file, "w")
    
    data = pd.read_csv(file, header = 0, index_col=None)
    models = data['model'].unique().tolist()
    models.sort()


    print("-------- Obtaining best performance ---------")
    f.write("-------- Obtaining best performance ---------\n")
    print("{:10s}{:20s}{:15s}{:10s}".format("Model", "Malicious Users", "Dataset Size", "MCC"))
    f.write("{:10s}{:20s}{:15s}{:10s}\n".format("Model", "Malicious Users", "Dataset Size", "MCC"))
    for m in models:
        model_data = data.loc[data['model']==m]
        i = model_data["mcc"].idxmax()
        text = "{:10s}{:<20.0f}{:<15.0f}{:<10.3f}".format(
                data.iloc[i]["model"],
                data.iloc[i]["malicious"], 
                data.iloc[i]["dataset_len"],
                data.iloc[i]["mcc"])
        print(text)
        f.write(text+"\n")

    print("-------- Obtaining breaking point ---------")
    f.write("-------- Obtaining breaking point ---------\n")
    print("{:10s}{:20s}{:15s}{:10s}".format("Model", "Malicious Users", "Dataset Size", "MCC"))
    f.write("{:10s}{:20s}{:15s}{:10s}\n".format("Model", "Malicious Users", "Dataset Size", "MCC"))
    for m in models:
        model_data = data.loc[data['model']==m]
        model_data =  model_data.loc[model_data["mcc"] < 0.70]

        try:
            i = model_data["malicious"].idxmin()
        except:
            i = data.loc[data['model']==m]["mcc"].idxmin()
        text = "{:10s}{:<20.0f}{:<15.0f}{:<10.3f}".format(
                data.iloc[i]["model"],
                data.iloc[i]["malicious"], 
                data.iloc[i]["dataset_len"],
                data.iloc[i]["mcc"])
        print(text)
        f.write(text+"\n")
    
    print("-------- Obtaining worst performance ---------")
    f.write("-------- Obtaining worst performance ---------\n")
    print("{:10s}{:20s}{:15s}{:10s}".format("Model", "Malicious Users", "Dataset Size", "MCC"))
    f.write("{:10s}{:20s}{:15s}{:10s}\n".format("Model", "Malicious Users", "Dataset Size", "MCC"))
    for m in models:
        model_data = data.loc[data['model']==m]
        i = model_data["mcc"].idxmin()
        text = "{:10s}{:<20.0f}{:<15.0f}{:<10.3f}".format(
                data.iloc[i]["model"],
                data.iloc[i]["malicious"], 
                data.iloc[i]["dataset_len"],
                data.iloc[i]["mcc"])

        print(text)
        f.write(text+"\n")
    f.close()

def main(args):
    data = pd.read_csv(args.i, header = 0, index_col=None)
    convert_to_average(data, args.o)
    get_results(args.o, args.f)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Obtain statistical results from the ML dataset')
    parser.add_argument('-i', type=str, help='results dataset (CSV)', default='output.csv')
    parser.add_argument('-o', type=str, help='output file with combined results', default='result.csv')
    parser.add_argument('-f', type=str, help='output file with statistics', default='log.txt')
    args = parser.parse_args()
    
    main(args)