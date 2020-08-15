#!/usr/bin/env python
# coding: utf-8

# In[6]:


import MeCab
import re
import pandas as pd
import pprint
import emoji
import urllib.request
import unicodedata
import string
import numpy as np


# # 前処理

def preprocessing(tweet_path):#(tweet情報を格納したcsvファイルのpath)
    """
    tweetとprofileを前処理する関数
    """
    df = pd.read_csv(tweet_path,engine='python',index_col=0)
    #分析の妥当性のために同一人物のツイートを削除
    df = df[~df.duplicated(subset='user_id', keep='last')].reset_index(drop=True)
    #tweetの処理
    tweet_lst = df.loc[:,["tweet"]].values.tolist()
    processed_tweet = []

    #特殊記号リスト
    pattern = '[!"#$%&\'\\\\()*+,-. 𓂃𓈒𓏸 ✫ ▷ ∞ ᐢ̫ᐢ ☞ ❐❐❐❐❐❐ – ä ◟̽̽﹆ ✿ ᎒ ╱ È ⌗ ░░░▒▓▓▒░░░  𓊝 ••éñ 𖥻𖥻 ➫➫ ¿ ꏍ҂𓄹ûè•’•çãê☭ /:;<=>? ¬ ü 𓆏 ψψ☉☾ @[\\]^_`{|}~ ̇⸜ू ◡◜࿁◝ ᅠᅠᅠ⠀⠀… ’ ’ í「」Д ゞ定️⃣️⃣ ๑⃙⃘ˊ « ✧✵✧✵✧༆—╰─➛˗ˏˋˎ˗ σ´σ á ⤷⃤ ‘ ∙ , ・・;・ ...   ᷄   ━゚ ゚━ꪔ̤̮ꪔ̤ 罒 ᜦ  ᐛ و  ˆΟˆ  ❀٩ ❝❞  ꒳ ۶» ̀  〇〔〕“”◇ᴗ●↓→♪★⊂⊃※△□◎ 〜 ọ  ́〈〉⌘  ó̴̶̷̥  ♡ ↑ ↓ → ←『』【】＆＊・【】●ㅅ●Ф☆✩︎♡→←▼①②③④⑤『』ω《》∠∇∩♪∀◞ཀCщ≧≦ ́◤◢■◆★※↑↓〇◯○◎⇒▽◉Θ♫♬〃“”◇ᄉ⊂⊃д ٫ （）＄＃＠。、？！｀＋￥％,]'
    
    for tweet in tweet_lst:
        tweet = str(tweet)
        tweet = tweet = unicodedata.normalize("NFKC", tweet)  # 全角記号を半角へ置換
        tweet = re.sub(r'[!-~]', "", tweet)#半角記号,数字,英字を削除
        tweet = ''.join(['' if c in emoji.UNICODE_EMOJI else c for c in tweet]) # 絵文字削除
        tweet = re.sub(r"(https?|ftp)(:\/\/[-_\.!~*\'()a-zA-Z0-9;\/?:\@&=\+$,%#]+)", "" ,tweet)#URL削除
        tweet =  re.sub(pattern, '', tweet) # 不要記号削除
        tweet = re.sub("[?:u3000|amp|xa|n]","",tweet)#漏れを微調整
        if tweet =='':#前処理した結果空欄になったら削除対象に
            tweet = None
        processed_tweet.append(tweet)


    #profileの処理
    profile_lst = df.loc[:,["profile"]].values.tolist() 
    processed_profile = []
    for profile in profile_lst:
        profile = str(profile)
        profile = profile = unicodedata.normalize("NFKC", profile)  # 全角記号を半角へ置換
        profile = re.sub(r'[!-~]', "", profile)#半角記号,数字,英字を削除
        profile = ''.join(['' if c in emoji.UNICODE_EMOJI else c for c in profile]) # 絵文字削除
        profile = re.sub(r"(https?|ftp)(:\/\/[-_\.!~*\'()a-zA-Z0-9;\/?:\@&=\+$,%#]+)", "" ,profile)#URL削除
        profile =  re.sub(pattern, '', profile) # 不要記号削除
        profile = re.sub("[?:u3000|amp|xa|n]","",profile)#漏れを微調整
        if profile =='':#前処理した結果空欄になったら削除対象に
            profile = None
        processed_profile.append(profile)
            
    processed_df = pd.DataFrame(processed_profile,columns=["processed_profile"])
    processed_df["processed_tweet"] = processed_tweet

    df = pd.concat([df,processed_df],axis=1)
    df = df.dropna(how="any").reset_index(drop=True)
    print("分析可能なデータは{}件です".format(df.shape[0]))
    
    return df

if __name__ == "__main__":
    tweetdata_name = input("分析するtwitterデータファイルをdataフォルダに入れて、そのファイル名を入力してください(.csvまで)")
    tweet_path = "data/{}".format(tweetdata_name)
    df = preprocessing(tweet_path)
    df.to_csv("data/processed.csv")
    print("前処理した結果をdataフォルダに保存しました")
