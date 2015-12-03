#!/usr/bin/env LC_ALL=ja_JP.utf-8 python
# -*- coding: utf-8 -*-

import random
import sqlite3
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import re


# 辞書ファイル名
db_file = 'morph_db.db'

# 品詞テーブル
pos_table = {u"名詞":1, u"動詞":2, u"副詞":3, u"形容詞":4}

def getOneWord(pos):
    word = None
    if pos in pos_table.values():
        c = cur.execute(u"select * from MorphDict where pos == ? order by random() limit 1",(pos,))
        id, p, word = c.fetchone()
    return word

conn = sqlite3.connect(db_file)
cur = conn.cursor()


#if random.randint(1,10000) % 2 == 0:

while True:
    noun1 = getOneWord(1)
    noun2 = getOneWord(1)
    adj   = getOneWord(4)
    verb  = getOneWord(2)
    adv   = getOneWord(3)

    candidates = noun1 + noun2 + adj + verb + adv

    matchOB = re.match(u"[ぁ-ゞ]",noun2)
    matchNM = re.match(r"[0-9]", candidates)

    if len(adj)+len(noun1) == 5 and len(adv)+len(verb) == 7 and (len(noun2) == 5 or len(noun2) == 6) and not matchOB and not matchNM:
        print("%s%s  %s%s  %s" % (adj, noun1, adv, verb, noun2))
        break




conn.commit()
conn.close()
