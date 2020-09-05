#!/usr/bin/env python
# coding: utf-8



from preprocessing import preprocessing
from sentiment_predict import sentiment_predict
from sentiment_plot import sentiment_plot
from LDA import posi_nega_lst,analyzer,plot_best_topics,get_topic_num,plot_topics
from stopwords import stopwords
import pandas as pd
import os
import warnings
warnings.simplefilter('ignore')

# In[ ]:


def Analysis():
    
    while True:
        folder_name = input("分析結果を格納するフォルダ名を入力してください。resultフォルダの中に新しく作成されます")
        try:
            os.mkdir("result/{}".format(folder_name))
            break
        except FileExistsError:
            print("同じ名前のフォルダがすでに存在しています。名前を変えてください")
            continue
    tweetdata_name = input("分析するtwitterデータファイルをdataフォルダに入れて、そのファイル名を入力してください(.csvまで)")
    tweet_path = "data/{}".format(tweetdata_name)
    df = preprocessing(tweet_path)
    df = sentiment_predict(df,folder_name)
    sentiment_plot(df,folder_name)
    posi_corpus,posi_dictionary,nega_corpus,nega_dictionary = get_topic_num(df)
    os.mkdir("result/{}/positive_group".format(folder_name))
    os.mkdir("result/{}/negative_group".format(folder_name))
    plot_topics(posi_corpus,posi_dictionary,nega_corpus,nega_dictionary,folder_name)
    while True:
        finish_or_continue = int(input("グループ数を変更して分析し直す場合は[1]を、終了する場合は[2]を押してください"))
        if finish_or_continue == 1:
            plot_topics(posi_corpus,posi_dictionary,nega_corpus,nega_dictionary,folder_name)
        elif finish_or_continue == 2:
            break
        else:
            print("半角で1か2を押してください")
            continue


# In[ ]:

if __name__ == "__main__":
    Analysis()


# In[ ]:




