#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import MeCab
from matplotlib import pyplot as plt
from wordcloud import WordCloud
import seaborn as sns


# In[1]:


def sentiment_plot(df,folder_name):#ポジネガ 判定したsentimentが入ったdfを引数に

    posi_tweet_lst = df[df["sentiment"].isin([1])].loc[:,"processed_tweet"].values.tolist()
    posi_tweet = "".join(posi_tweet_lst)
    # MeCabの準備
    tagger = MeCab.Tagger()
    tagger.parse('')
    node = tagger.parseToNode(posi_tweet)
    # 名詞を取り出す
    word_list = []
    while node:
        word_type = node.feature.split(',')[0]
        if word_type == '名詞':
            word_list.append(node.surface)
        node = node.next
    # リストを文字列に変換
    word_chain = ' '.join(word_list)
    # ワードクラウド作成
    W = WordCloud(width=500, height=300,max_words=100, background_color='white', colormap='Dark2', font_path='font/TakaoGothic.ttf').generate(word_chain)
    fig = plt.figure(figsize=(12, 5))
    W.to_file("result/{}/{}".format(folder_name,"positive_tweet_top100.png"))

    
    nega_tweet_lst = df[df["sentiment"].isin([0])].loc[:,"processed_tweet"].values.tolist()
    nega_tweet = "".join(nega_tweet_lst)
    # MeCabの準備
    tagger = MeCab.Tagger()
    tagger.parse('')
    node = tagger.parseToNode(nega_tweet)
    # 名詞を取り出す
    word_list = []
    while node:
        word_type = node.feature.split(',')[0]
        if word_type == '名詞':
            word_list.append(node.surface)
        node = node.next
    # リストを文字列に変換
    word_chain = ' '.join(word_list)
    # ワードクラウド作成
    W = WordCloud(width=500, height=300,max_words=100, background_color='black', colormap='Dark2', font_path='font/TakaoGothic.ttf').generate(word_chain)
    fig = plt.figure(figsize=(12, 5))
    W.to_file("result/{}/{}".format(folder_name,"negative_tweet_top100.png"))
    
    
    df = df.replace({0:"negative",1:"positive"})
    posi_nega_graph = sns.countplot(df["sentiment"])
    figure = posi_nega_graph.get_figure()
    figure.savefig("result/{}/posi_nega_graph.png".format(folder_name))
    
    
    plt.close()




