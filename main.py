# -*- coding: utf-8 -*-

import os
import sys
import argparse
import re
import csv
from collections import Counter
import matplotlib.pyplot as plt

PATTEN = r',|#| |\.|\n|\||\/|='

IGNORE = [
    '-',
    'about',
    'above',
    'across',
    'after',
    'against',
    'among',
    'around',
    'at',
    'before',
    'behind',
    'below',
    'beside',
    'between',
    'by',
    'down',
    'during',
    'for',
    'from',
    'in',
    'inside',
    'into',
    'near',
    'of',
    'off',
    'on',
    'out',
    'over',
    'through',
    'to',
    'toward',
    'under',
    'up',
    'with',
    'aboard',
    'along',
    'amid',
    'as',
    'beneath',
    'beyond',
    'but',
    'concerning',
    'considering',
    'despite',
    'except',
    'following',
    'like',
    'minus',
    'next',
    'onto',
    'opposite',
    'outside',
    'past',
    'per',
    'plus',
    'regarding',
    'round',
    'save',
    'since',
    'than',
    'till',
    'underneath',
    'unlike',
    'until',
    'upon',
    'versus',
    'via',
    'within',
    'without',
    'the',
    'a',
    'was',
    'you',
    'is',
    'are',
    'were',
    'and',
    'be',
    'The',
    'our',
    'Our',
    'As',
    'We',
    'A',
    'no',
    'we',
    'AS',
    'will',
]


def DebugLog(*msgs):
    if False:
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
    with open(file_name, 'w', newline='', encoding='GBK') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerows(data)


def DrawBar(data):
    words = [val[0] for val in data]
    DebugLog('Words: ', words)
    tops = [val[1] for val in data]
    DebugLog('Tops: ', tops)
    plt.rcParams['font.sans-serif'] = ['SimHei']
    fig, ax = plt.subplots()
    ax.barh(words, tops)
    plt.show()


if __name__ == '__main__':
    args = GetArgs()
    ret = Run(args.file_name, args.top_num)
    NicePrint(ret)
    WriteCSV(args.file_name, ret)
    DrawBar(ret)
    sys.exit(0)
