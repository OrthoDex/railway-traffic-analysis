# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys
import config
from datetime import datetime


def label(change):
    if change < 0.05 and change > -0.05:
        return "flat"
    if change < 0:
        return "down"
    if change > 0:
        return "up"


def find_spd_by_label(group):
    labels = group.groupby("Label")

    for _, group in labels:
        find_same_label_spd(group)

    find_diff_label_spd(labels)


def find_diff_label_spd(label_group):
    movements = list(label_group.groups.keys())
    for name, group in label_group:
        movements.remove(name)
        if not movements:
            pass
        else:
            for label in movements:
                config.di_matrix.ix[
                    config.di_matrix.index.isin(group["Station"]),
                    list(label_group.get_group(label)["Station"].values),
                ] += 1
                config.di_matrix.ix[
                    list(label_group.get_group(label)["Station"].values),
                    config.di_matrix.index.isin(group["Station"]),
                ] += 1


def find_same_label_spd(group):
    for index, row in group.iterrows():
        s = pd.DataFrame()
        s["Change"] = abs(group["% Change"] - row["% Change"])
        s["Station"] = group["Station"]
        calc_spd(s, row["Station"])


def calc_spd(change_list, station):
    threshold = 0.005
    for index, row in change_list.iterrows():
        if row["Change"] > threshold:
            config.di_matrix[station][row["Station"]] += 1


def extract_data(data):

    df = data.copy()
    df["Diff"] = (
        df.groupby("Station")["Passengerdensity"]
        .transform(pd.Series.diff)
        .fillna(value=0)
    )
    df["% Change"] = (
        df.groupby("Station")["Passengerdensity"].pct_change().fillna(value=0)
    )
    df["Label"] = df.copy().apply(lambda row: label(row["% Change"]), axis=1)

    stations = df["Station"].unique()
    values = np.zeros([stations.size, stations.size])
    config.di_matrix = pd.DataFrame(
        data=values, index=stations, columns=stations, dtype="int64"
    )

    year_wise = df.groupby("Year")

    for name, group in year_wise:
        year_group = group[["Station", "% Change", "Label"]]
        find_spd_by_label(year_group)

    print("Distance matrix computation complete.")

    config.di_matrix.to_excel("../distance_matrix_full.xlsx", sheet_name="Sheet1")

    return config.di_matrix


def year_format(year):
    yr = str(year)
    return datetime.strptime(yr[-(len(yr) - 4) :] + "/" + yr[:4], "%m/%Y").date()
