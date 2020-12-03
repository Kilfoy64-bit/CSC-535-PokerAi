import pandas as pd
import numpy as np
from statistics import mode
from collections import Counter

df = pd.read_csv("./datasets/randomgames.csv")


def seqsize(rowdata: list) -> int:
    s = set(rowdata)
    longest = 0
    for i in s:
        if i-1 not in s:
            current = i
            streak = 0
            while i in s:
                i += 1
                streak += 1
                longest = max(longest, streak)
    return longest


def draw_md(data: pd.DataFrame) -> pd.DataFrame:
    df = pd.DataFrame(columns=["cardmed", "cardrng", "mcsuitprob",
                               "duprcards", "duprgszmax", "maxseqsize", "winner"])
    card_col = ["d1", "d2"]
    suit_col = ["d1s", "d2s"]
    # get median
    df["cardmed"] = data[card_col].median(axis=1)
    # get range
    df["cardrng"] = data[card_col].max(axis=1) - data[card_col].min(axis=1)
    # Get probability of suit mode
    for row in data.iterrows():
        rowdata = [row[1].tolist()[x] for x in range(4) if x % 2 == 1]
        df.loc[row[0], "mcsuitprob"] = rowdata.count(
            mode(rowdata))/len(rowdata)
        rowdata = sorted([row[1].tolist()[x] for x in range(4) if x % 2 == 0])
        c = Counter(rowdata)
        # Get number of duplicate rank cards
        df.loc[row[0], "duprcards"] = sum([x for x in c.values() if x > 1])
        # Get size of largest duplicate rank groups
        df.loc[row[0], "duprgszmax"] = c.most_common()[0][1]
        # Get max sequence size
        df.loc[row[0], "maxseqsize"] = seqsize(rowdata)
    df["winner"] = data["winner"]
    return df


def flop_md(data: pd.DataFrame) -> pd.DataFrame:
    df = pd.DataFrame(columns=[
                      "cardmed", "cardrng", "mcsuitprob", "duprcards", "duprgszmax", "maxseqsize", "winner"])
    card_col = ["d1", "d2", "f1", "f2", "f3"]
    suit_col = [x + "s" for x in card_col]
    # get median
    df["cardmed"] = data[card_col].median(axis=1)
    # get range
    df["cardrng"] = data[card_col].max(axis=1) - data[card_col].min(axis=1)
    # Get probability of suit mode
    for row in data.iterrows():
        rowdata = [row[1].tolist()[x] for x in range(10) if x % 2 == 1]
        df.loc[row[0], "mcsuitprob"] = rowdata.count(
            mode(rowdata))/len(rowdata)
        rowdata = sorted([row[1].tolist()[x] for x in range(10) if x % 2 == 0])
        c = Counter(rowdata)
        # Get number of duplicate rank cards
        df.loc[row[0], "duprcards"] = sum([x for x in c.values() if x > 1])
        # Get size of largest duplicate rank groups
        df.loc[row[0], "duprgszmax"] = c.most_common()[0][1]
        # Get max sequence size
        df.loc[row[0], "maxseqsize"] = seqsize(rowdata)
    df["winner"] = data["winner"]
    return df


def turn_md(data: pd.DataFrame) -> pd.DataFrame:
    df = pd.DataFrame(columns=[
                      "cardmed", "cardrng", "mcsuitprob", "duprcards", "duprgszmax", "maxseqsize", "winner"])
    card_col = ["d1", "d2", "f1", "f2", "f3", "t1"]
    suit_col = [x + "s" for x in card_col]
    # get median
    df["cardmed"] = data[card_col].median(axis=1)
    # get range
    df["cardrng"] = data[card_col].max(axis=1) - data[card_col].min(axis=1)
    # Get probability of suit mode
    for row in data.iterrows():
        rowdata = [row[1].tolist()[x] for x in range(12) if x % 2 == 1]
        df.loc[row[0], "mcsuitprob"] = rowdata.count(
            mode(rowdata))/len(rowdata)
        rowdata = sorted([row[1].tolist()[x] for x in range(12) if x % 2 == 0])
        c = Counter(rowdata)
        # Get number of duplicate rank cards
        df.loc[row[0], "duprcards"] = sum([x for x in c.values() if x > 1])
        # Get size of largest duplicate rank groups
        df.loc[row[0], "duprgszmax"] = c.most_common()[0][1]
        # Get max sequence size
        df.loc[row[0], "maxseqsize"] = seqsize(rowdata)
    df["winner"] = data["winner"]
    return df


def river_md(data: pd.DataFrame) -> pd.DataFrame:
    df = pd.DataFrame(columns=[
                      "cardmed", "cardrng", "mcsuitprob", "duprcards", "duprgszmax", "maxseqsize", "winner"])
    card_col = ["d1", "d2", "f1", "f2", "f3", "t1", "r1"]
    suit_col = [x + "s" for x in card_col]
    # get median
    df["cardmed"] = data[card_col].median(axis=1)
    # get range
    df["cardrng"] = data[card_col].max(axis=1) - data[card_col].min(axis=1)
    # Get probability of suit mode
    for row in data.iterrows():
        rowdata = [row[1].tolist()[x] for x in range(14) if x % 2 == 1]
        df.loc[row[0], "mcsuitprob"] = rowdata.count(
            mode(rowdata))/len(rowdata)
        rowdata = sorted([row[1].tolist()[x] for x in range(14) if x % 2 == 0])
        c = Counter(rowdata)
        # Get number of duplicate rank cards
        df.loc[row[0], "duprcards"] = sum([x for x in c.values() if x > 1])
        # Get size of largest duplicate rank groups
        df.loc[row[0], "duprgszmax"] = c.most_common()[0][1]
        # Get max sequence size
        df.loc[row[0], "maxseqsize"] = seqsize(rowdata)
    df["winner"] = data["winner"]
    return df

def main():
    draw_md(df).to_csv("./datasets/drawmd.csv", index=False)
    flop_md(df).to_csv("./datasets/flopmd.csv", index=False)
    turn_md(df).to_csv("./datasets/turnmd.csv", index=False)
    river_md(df).to_csv("./datasets/rivermd.csv", index=False)

if __name__ == "__main__":
    main()