#%matplotlib inline
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys
import config

def label(change):
    if change < 0.05 and change > -0.05:
        return "flat"
    if change < 0:
        return "down"
    if change > 0:
        return "up"

def find_spd_by_label(group):
    labels = group.groupby("Label")

    find_diff_label_spd(labels)

    for name, group in labels:
        find_same_label_spd(group)

def find_diff_label_spd(label_group):
    movements = list(label_group.groups.keys())
    for name, group in label_group:
        movements.remove(name)
        if not movements:
            pass
        else:
            for label in movements:
                config.di_matrix.ix[config.di_matrix.index.isin(group['Station']), list(label_group.get_group(label)['Station'].values)] += 1

def find_same_label_spd(group):
    for index, row in group.iterrows():
        s = pd.DataFrame()
        s['Change'] = abs(group['% Change'] - row['% Change'])
        s['Station'] = group['Station']
        calc_spd(s, row['Station'])

def calc_spd(change_list, station):
    threshold = 0.005
    for index, row in change_list.iterrows():
        if row['Change'] > threshold:
            config.di_matrix[station][row['Station']] += 1

def main(arg):
    peak = arg[0]
    df = pd.read_excel('means_'+ peak + '.xlsx', 'Sheet1')
    df['Station'] = pd.Series(df['Station']).fillna(method='ffill')

    df['Diff'] = df.groupby('Station')['Means AM Peak'].transform(pd.Series.diff).fillna(value=0)
    df['% Change'] = df.groupby('Station')["Means AM Peak"].pct_change().fillna(value=0)
    df['Label'] = df.apply(lambda row: label(row['% Change']), axis=1)

    df.to_excel('change_values_' + peak + '.xlsx', sheet_name='Sheet1')

    stations = df["Station"].unique()
    values = np.zeros([stations.size, stations.size])
    config.di_matrix = pd.DataFrame(data=values,index=stations,columns=stations,dtype='int64')

    year_wise = df.groupby("Year")

    for name, group in year_wise:
        year_group = group[['Station','% Change','Label']]
        find_spd_by_label(year_group)

    config.di_matrix.to_excel('distance_matrix_' + peak + '.xlsx', sheet_name='Sheet1')

if __name__ == '__main__':
    main(sys.argv[1:])
