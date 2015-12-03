#!/usr/bin/env LC_ALL=ja_JP.utf-8 python
# -*- coding: utf-8 -*-

import sqlite3
import urllib
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import re

from bs4 import BeautifulSoup

# Yahoo! Developer Network Application ID
appid = ''
# Yahoo!形態素解析API
pageurl = 'http://jlp.yahooapis.jp/MAService/V1/parse'

# 辞書ファイル名
db_file = 'morph_db.db'

# 品詞テーブル
pos_table = {u"名詞":1, u"動詞":2, u"副詞":3, u"形容詞":4}

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

def createDict():
    table_exists = False
    tables = cur.execute(u"select name from sqlite_master")
    for t in tables:
        if( "MorphDict" in t ):
            table_exists = True

    if( not table_exists ):
        sql = """
        create table MorphDict(
            id integer primary key autoincrement,
            pos integer,
            word text
        )"""
        cur.execute(sql)

def insertItem(pos, word):
    c = cur.execute("select * from MorphDict where word == ?", (word,))
    if len(c.fetchall()) == 0:
        cur.execute("insert into MorphDict(pos, word) values(?, ?)", (pos, word))

sentence = '''

'''
# 形態素解析
result = morph(sentence, appid=appid)
for word, reading, pos_name in result:
    print("%s(%s)/%s"%(word, reading, pos_name))

# 必要な品詞の語だけをデータベースに登録
conn = sqlite3.connect(db_file)
cur = conn.cursor()

createDict()
for word, reading, pos_name in result:
    if pos_name in pos_table:
        insertItem(pos_table[pos_name], word)

c = cur.execute(u"select * from MorphDict")
for id, pos, word in c:
    print("%s: %s: %s"%(id, pos, word))

conn.commit()
conn.close()
