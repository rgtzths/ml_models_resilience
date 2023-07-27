import argparse
import csv

def select_sub_matrix(matrix, wp):
    sub_matrix = [[0]*11 for i in range(21)]
    for i in range(wp[0], 21):
        for j in range(wp[1], 11):
            sub_matrix[i][j] = matrix[i][j]
    return sub_matrix

def sub_matrix_bellow_threshold(matrix, wp, threshold):
    for i in range(wp[0], 21, 1):
        for j in range(wp[1], 11, 1):
            if matrix[i][j] >= threshold:
                return False
    return True

def find_worst_point(matrix, threshold):
    wp = [20, 10]

    if sub_matrix_bellow_threshold(matrix, wp, threshold):
        # search on both axis
        while sub_matrix_bellow_threshold(matrix, wp, threshold):
            wp = [wp[0]-1, wp[1]-1]
        wp = [wp[0]+1, wp[1]+1]

        # search on malicious axis only
        while sub_matrix_bellow_threshold(matrix, wp, threshold):
            wp = [wp[0]-1, wp[1]]
        wp = [wp[0]+1, wp[1]]

        # search on dataset axis only
        while sub_matrix_bellow_threshold(matrix, wp, threshold):
            wp = [wp[0], wp[1]-1]
        wp = [wp[0], wp[1]+1]
    
        return wp
    else:
        return None

def main(args):
    threshold = args.t
    f = open(args.o, "w")

    # structures to hold the indexes
    m = [i for i in range(0, 21)]
    d = [i for i in range(18000, 60001, 4200)]

    data = {}

    # read all data and compute the average
    with open(args.i, newline='') as csvfile:
        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
            k = (row['model'], int(row['malicious']), int(row['dataset_len']))
            if k not in data:
                data[k] = []
            data[k].append(float(row['mcc']))

    for k in data:
        data[k] = min(data[k])

    # convert data to another format
    data_per_model = {}
    for k in data:
        model, malicious, dataset_len = k
        if model not in data_per_model:
            data_per_model[model] = [[0]*11 for i in range(21)]
        i = m.index(malicious)
        j = d.index(dataset_len)

        data_per_model[model][i][j] = data[k]

    f.write(f"-------- Results obtained for the file {args.i} ---------\n")
    f.write("{:10s}{:13s}{:20s}{:15s}{:15s}\n".format("Model", "Data point", "% Malicious Users", "Dataset Size", "% of dataset"))
    print(f"-------- Results obtained for the file {args.i} ---------")
    print("{:10s}{:13s}{:20s}{:15s}{:15s}".format("Model", "Data point", "% Malicious Users", "Dataset Size", "% of dataset"))
    for k in data_per_model:
        matrix = data_per_model[k]
        wp = find_worst_point(matrix, threshold)
        if wp is not None:
            p_dataset = round(((d[wp[1]]- 18000)*(wp[0]/20)) / d[wp[1]]  ,2)
            print(f'{k:10s}[{wp[0]:2d}, {wp[1]:2d}]     {m[wp[0]]/20:<20.2f}{d[wp[1]]:<15d}{p_dataset:<15.2f}')
            f.write(f'{k:10s}[{wp[0]:2d}, {wp[1]:2d}]     {m[wp[0]]/20:<20.2f}{d[wp[1]]:<15d}{p_dataset:<15.2f}\n')

        else:
            na = "--"
            print(f'{k:<10s}[{na:<2s}, {na:<2s}]     {na:<20s}{na:<15s}{na:<15s}')
            f.write(f'{k:<10s}[{na:<2s}, {na:<2s}]     {na:<20s}{na:<15s}{na:<15s}\n')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Obtain breaking point from the ML models')
    parser.add_argument('-i', type=str, help='results dataset (CSV)', default='output.csv')
    parser.add_argument('-o', type=str, help='output file with statistics', default='breaking_point.txt')
    parser.add_argument('-t', type=float, help='performance threshold', default=0.7)
    args = parser.parse_args()
    
    main(args)