#!/usr/bin/env LC_ALL=ja_JP.utf-8 python
# -*- coding: utf-8 -*-

import sqlite3
import urllib
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from bs4 import BeautifulSoup

COUNT = 3

# Yahoo! Developer Network Application ID
appid = 'dj0zaiZpPXByaVM4WTdYazlxciZzPWNvbnN1bWVyc2VjcmV0Jng9OTI-'
# Yahoo!形態素解析API
pageurl = 'http://jlp.yahooapis.jp/MAService/V1/parse'

# 辞書ファイル名
db_file = 'morph_db.db'

# 品詞テーブル
pos_table = {u"名詞":1, u"動詞":2, u"副詞":3}

def morph(sentence, appid=appid, results="ma", filter='1|2|3|4|5|6|7|8|9|10|11|12|13'):
    postdata = {
        'appid'    : appid,
        'results'  : results,
        'filter'   : filter,
        'response' : 'baseform,reading,pos',
        'sentence' : sentence.encode('utf-8')
    }

    params = urllib.urlencode(postdata).encode(encoding='ascii')
    result = urllib.urlopen(pageurl, params)

    soup = BeautifulSoup(result.read(), "html.parser")
    return [(w.baseform.string, w.reading.string, w.pos.string)
        for w in soup.ma_result.word_list]

def markov(src):
    wordlist = 'morph_db.db'
    markov = {}
    w1=''
    for word in wordlist:
        if w1:
            if (w1) not in markov:
                markov[(w1)] = []
            markov[(w1)].append(word)
        w1=word
    count = 0
    sentence=''
    w1=random.choice(markov.keys())

    while count < COUNT:
        if markov.has_key((w1))==True:
            tmp = random.choice(markov[(w1)])
            sentence += tmp
        w1=tmp
        count +=1
    return sentence
