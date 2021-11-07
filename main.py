# -*- coding: utf-8 -*-

import os
import sys
import argparse
import re
import csv
import requests
from collections import Counter
import matplotlib.pyplot as plt
import html_text

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
    '&', 'de', 'la', 'this', 'that', 'e', 'com',
]


def DebugLog(*msgs):
    if True:
        print('[DEBUG]: ', msgs)


def GetArgs():
    parser = argparse.ArgumentParser(description='Calculate word frequency')
    parser.add_argument('--file', dest='file_name', required=False,
                        help='File name to count the word frequency.')
    parser.add_argument('--top', dest='top_num', type=int, required=True,
                        help='Number of top frequency words to show.')
    parser.add_argument('--url', dest='url_file', required=False,
                        help='File with URLs to count the word frequency.')
    args = parser.parse_args()
    return args

def FixUrl(url):
    DebugLog('Before Url: %s' % url)
    regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    url = url.strip().rstrip()
    DebugLog('After Url: %s' % url)
    if not re.match(regex, url):
        DebugLog("It's not a correct URL!")
        return ''
    return url


def GetHtmlContent(url):
    data = ''
    try:
        req = requests.get(FixUrl(url),  timeout=30)
        data = req.text
        req.close()
    except:
        pass
    return data

def Count(data, top_num):
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

def FromSingleTxt(file_name, top_num):
    with open(file_name, encoding='utf-8', mode='r') as f:
        data = f.read()
    return Count(data, top_num)

def FromUrlTxt(file_name, top_num):
    with open(file_name, encoding='utf-8', mode='r') as f:
        lines = f.readlines()
    to_analyse = ''
    for line in lines:
        web_html = GetHtmlContent(line.rstrip())
        text = html_text.extract_text(web_html)
        to_analyse = to_analyse + ' ' + text
    return Count(to_analyse, top_num) 
        

def NicePrint(data):
    print('{:>30s}{:>30s}'.format('单词', '次数'))
    for ele in data:
        print('{:>30s}{:>30s}'.format(str(ele[0]), str(ele[1])))


def WriteCSV(file_name, data):
    file_name = file_name[:-4] + '.csv'
    DebugLog('CSV file name: ' + file_name)
    with open(file_name, 'w', newline='', encoding='utf-8') as csvfile:
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
    if args.file_name:
        ret = FromSingleTxt(args.file_name, args.top_num)
        NicePrint(ret)
        WriteCSV(args.file_name, ret)
        DrawBar(ret)      
    elif args.url_file:
        ret = FromUrlTxt(args.url_file, args.top_num)
        NicePrint(ret)
        WriteCSV(args.url_file, ret)
        DrawBar(ret) 
    
    sys.exit(0)
