import csv
import os
import sys
from random import randint


def gen_hand() -> dict:
    hand = {}
    for item in ['d1s', 'd2s', 'f1s', 'f2s', 'f3s', 't1s', 'r1s']:
        hand[item] = randint(1, 4)
    for item in ['d1', 'd2', 'f1', 'f2', 'f3', 't1', 'r1']:
        hand[item] = randint(1, 13)
    return hand


def no_dup(hand: dict) -> bool:
    '''
    Brute force check for verifying no duplicate cards
    '''
    checkhands = list(hand.keys())
    for i in range(len(checkhands), 2):
        current_rank = checkhands[i]
        current_suit = checkhands[i+1]
        for j in range(i+2, len(checkhands), 2):
            if current_rank == checkhands[j] and current_suit == checkhands[j+1]:
                return False
    return True


'''
Column name translation:
d* -> Initial draw
f* -> Flop
t* -> Turn
r* -> River
*s -> Suit indicator

1 -> Hearts
2 -> Spades
3 -> Diamonds
4 -> Clubs

1 - 2
2 - 3
3 - 4
4 - 5
5 - 6
6 - 7
7 - 8
8 - 9
9 - 10
10 - J
11 - Q
12 - K
13 - A
'''
csvfile = open('./datasets/hands.csv', 'w', newline='')
columns = ['d1', 'd1s', 'd2', 'd2s', 'f1', 'f1s',
           'f2', 'f2s', 'f3', 'f3s', 't1', 't1s', 'r1', 'r1s']
writer = csv.DictWriter(csvfile, fieldnames=columns)
writer.writeheader()
for i in range(5000):
    hand = gen_hand()
    while not no_dup(hand):
        hand = gen_hand()
    writer.writerow(hand)
csvfile.close()
