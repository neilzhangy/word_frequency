# -*- coding: utf-8 -*-

import os
import sys
import argparse
import re
import csv
from collections import Counter

PATTEN = r',|#| |\.|\n|\||\/'

IGNORE = ['the', 'a', 'if', 'in', 'it', 'of', 'or', 'and', 'an', 'to']


def DebugLog(*msgs):
    if True:
        print('[DEBUG]: ', msgs)


def GetArgs():
    parser = argparse.ArgumentParser(description='Calculate word frequency')
    parser.add_argument('--file', dest='file_name', required=True,
                        help='File name to count the word frequency.')
    parser.add_argument('--top', dest='top_num', type=int, required=True,
                        help='Number of top frequency words to show.')
    args = parser.parse_args()
    return args


def Run(file_name, top_num):
    with open(file_name, encoding='utf-8', mode='r') as f:
        data = f.read()

    word_list = re.split(PATTEN, data)
    DebugLog('Length of the list: %d' % len(word_list))
    word_list = list(filter(None, word_list))
    DebugLog(word_list)

    counter = Counter(word_list)
    for word in list(counter):
        if word in IGNORE:
            del counter[word]
    DebugLog(counter.most_common(top_num))
    return counter.most_common(top_num)


def NicePrint(data):
    print('{:>30s}{:>30s}'.format('单词', '次数'))
    for ele in data:
        print('{:>30s}{:>30s}'.format(str(ele[0]), str(ele[1])))


def WriteCSV(file_name, data):
    file_name = file_name[:-4] + '.csv'
    DebugLog('CSV file name: ' + file_name)
    with open(file_name, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerows(data)


if __name__ == '__main__':
    args = GetArgs()
    ret = Run(args.file_name, args.top_num)
    NicePrint(ret)
    WriteCSV(args.file_name, ret)
    sys.exit(0)
