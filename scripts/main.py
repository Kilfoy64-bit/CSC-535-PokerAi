import pandas as pd
import numpy as np

def main():

    columns = ['suit1', 'card1', 'suit2', 'card2', 'suit3', 'card3', 'suit4', 'card4', 'suit5', 'card5', 'hand']
    poker_hands_training = pd.read_csv("./datasets/poker-hand-training-true.data", header = None,  names = columns)
    print(poker_hands_training.head())


if __name__ == "__main__":
    main()