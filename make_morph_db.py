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
探査機はやぶさ２、小惑星へ進路変更　成否判明は来週以降
産経新聞 12月3日(木)19時16分配信
 探査機はやぶさ２、小惑星へ進路変更　成否判明は来週以降
はやぶさ2の軌道変更（写真：産経新聞）　宇宙航空研究開発機構（ＪＡＸＡ）の小惑星探査機「はやぶさ２」が３日夜、目的地の小惑星「リュウグウ」に向かうため、地球の引力を利用して軌道を変更した。探査実現に欠かせない重要なステップで、正しい軌道に乗ったかは１０日以降に判明する。　計画では、はやぶさ２は３日午後７時８分、米ハワイ付近の高度３０９０キロで地球に最接近。相模原市にあるＪＡＸＡの管制室では、研究者らが緊張した様子で機体の状態を示す画面を見守った。　取材に応じた津田雄一プロジェクトマネージャは「気が抜けない運用を続けている。管制室には打ち上げ時のような緊張感がある」と話した。　はやぶさ２は太陽の周りを回る地球に対し、後ろから追い掛けるように接近。軌道は引力の影響で曲がり、小惑星へと進路を変える。地球の運動エネルギーを受けてスピードも秒速約１．６キロ加速する。　この方法はフィギュアスケートのペア競技で、滑走する男性が女性の手を取り、回転しながら手を離すと女性が勢いよく滑っていく様子に似ている。　軌道を正確に計算し、機体の位置を制御することが成功の鍵を握る。日本は昭和６２年以降、この方法による軌道変更を５機の探査機で計約３０回実施し、１回を除いて成功させている。
トラブル急増「掃除サービス」　国民生活センターが注意呼びかけ
フジテレビ系（FNN） 12月3日(木)17時35分配信
年末を前に、国民生活センターが注意を呼びかけた。
国民生活センターに寄せられた掃除サービスに関する相談は、近年、増加傾向にあり、2014年度は919件と、1,000件近くにのぼっている。
相談内容としては、「見積時よりも作業時間が短く、掃除が雑」といったサービスの品質や変色・破損に関する相談に加え、安い料金を提案したあと、高額なサービスを勧誘する事業者もみられるという。
こうしたトラブルは、掃除サービスを行う事業者が、認可や資格なしに営業できることが背景にある。
国民生活センターによると、エアコンの掃除を依頼したら、上のふたが落ちて折れてしまったというもの。
また、ハウスクリーニング業者に玄関のワックス塗りを依頼したところ、上がりがまちの色がはげ、色が落ちてしまった。
さらに、見積もりでは、2人の業者が1時間半の作業で3万円だったが、実際には1人で来て、1時間で3万円を請求されたといったトラブルがあるという。
シャーロット、泉ピン子と再会に涙「ありがとう」
オリコン 12月3日(木)17時46分配信
 シャーロット、泉ピン子と再会に涙「ありがとう」
『マッサン』で共演した泉ピン子（右）のサプライズ登場に涙したシャーロット・ケイト・フォックス（左）（C）ORICON NewS inc.　米女優のシャーロット・ケイト・フォックスが3日、東京・東急シアターオーブでブロードウェイミュージカル『シカゴ』来日公演のプレスコールに出席。NHK連続テレビ小説『マッサン』で義母を演じた女優・泉ピン子がサプライズで花束を持って登場すると「うれしい、とても感動した。ありがとう」と日本語で感謝を伝え、涙を流して再会を喜んだ。
【動画】シャーロット、ピン子登場サプライズに涙　泉を見たシャーロットは涙を流して感激。泉は「うちの嫁です。知らないうちにブロードウェイデビューしていて、全然イメージ違った」と驚いていたが「夢かなってよかったね。この人はすごく頑張り屋。『マッサン』無駄じゃなかった。あれで頑張ったから今がある」とねぎらっていた。　「エリーに会いに来るお客さんも多いと思うし、母としてもうれしい。ドラマのなかではいろいろありましたけれど、誕生日にもらったストールはずっと使っています」と優しい目で見つめ、報道陣に向かって「なるべく大きく扱ってください」と“母”らしいお願い。何度もしっかり抱き合い、「風邪対策はしっかりね」と気遣っていた。　来日公演初日を明日に控えて、シャーロットは「生まれ故郷でブロードウェイデビューできて、2つ目の故郷である日本にも戻って来ることができて素晴らしい体験をしている」と話していた。そのほか、アムラ＝フェイ・ライト、トム・ヒューイット、ロズ・ライアンが出席。12月4日～23日まで東京・東急シアターオーブにて来日公演が行われる。
　フェイスブックのCEO、マーク・ザッカーバーグ氏（31）は1日、フェイスブック株の99パーセントにあたる450億ドル（約5.5兆円）を、人間の可能性を伸ばすことと平等の促進を目的とする慈善運動のために寄付することを、娘に宛てた手紙の中で明らかにした。

　同氏のフェイスブックで公表された手紙は、歌手のシャキーラや米カリフォルニア州元知事アーノルド・シュワルツェネッガー氏、マイクロソフト設立者ビル・ゲイツ氏の妻メリンダ・ゲイツさんを含む57万人以上から「いいね！」を獲得した。
　ゲイツ氏やウォーレン・バフェット氏など著名な億万長者たちも、自ら慈善財団を設立している。

　ザッカーバーグ氏は、妻プリシラ・チャンさんと共に今回の「チャン・ザッカーバーグ・イニシアチブ」を管理しながら、世界最大のSNS、フェイスブックのCEOとしてこれからも従事し、企業支配権を維持する。
　今後3年間に亘り、毎年10億ドル（約1234億円）を寄付に充てるという。12月2日付でフェイスブックの時価は3300億ドルだった。
　
　同氏にとって、今回が初めての慈善活動ではない。
　26歳で「ギビング・プレッジ」と契約しており、これは世界中の資産家が、生涯中もしくは死後に資産の半分以上を慈善活動に寄付する運動だ。

　映像は、出産前の夫婦をインタビューしたもの。

（アメリカ、12月2日、取材・動画：ロイター、日本語翻訳：アフロ）
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
