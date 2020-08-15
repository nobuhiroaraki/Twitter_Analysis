#!/usr/bin/env python
# coding: utf-8

# # データ準備（前処理&感情分析&ポジネガユーザーごとにプロフィールをリスト化）

# In[ ]:


import itertools
import glob
import numpy as np
import pandas as pd
from tqdm import tqdm
import MeCab 
import datetime
import gensim
import matplotlib
import matplotlib.pylab as plt
from matplotlib.backends.backend_pdf import PdfPages
from wordcloud import WordCloud
from PIL import Image
import pyLDAvis
import pyLDAvis.gensim
from stopwords import stopwords
np.random.seed(0)


# In[ ]:


#ポジネガユーザーごとにプロフィールをリスト化
def posi_nega_lst(df):
    positive_lst = df[df["sentiment"].isin([1])].loc[:,["processed_profile"]].values.tolist()
    positive_lst = list(itertools.chain.from_iterable(positive_lst))

    negative_lst = df[df["sentiment"].isin([0])].loc[:,["processed_profile"]].values.tolist()
    negative_lst = list(itertools.chain.from_iterable(negative_lst))
    
    return positive_lst,negative_lst


# # LDA

# In[ ]:


#形態素解析して助詞等の単品で意味を持たない単語を除去してリストに格納
def analyzer(text, mecab, stopwords=[], target_part_of_speech=['proper_noun', 'noun', 'verb', 'adjective']):

    node = mecab.parseToNode(text)
    words = []
    
    while node:
        features = node.feature.split(',')
        
        #特殊文字の除去漏れ等でエラーが起きたらそのデータは諦める
        try:
            surface = features[7]
        except IndexError:
            pass
        
        if (surface == '*') or (len(surface) < 2) or (surface in stopwords):
            node = node.next
            continue
            
        noun_flag = (features[0] == '名詞')
        proper_noun_flag = (features[0] == '名詞') & (features[1] == '固有名詞')
        verb_flag = (features[0] == '動詞') & (features[1] == '自立')
        adjective_flag = (features[0] == '形容詞') & (features[1] == '自立')
        
 
        if ('proper_noun' in target_part_of_speech) & proper_noun_flag:
            words.append(surface)
        elif ('noun' in target_part_of_speech) & noun_flag:
            words.append(surface)
        elif ('verb' in target_part_of_speech) & verb_flag:
            words.append(surface)
        elif ('adjective' in target_part_of_speech) & adjective_flag:
            words.append(surface)
        
        node = node.next

    return words


# In[ ]:


def plot_best_topics(sentiment_lst):
 
    mecab = MeCab.Tagger()

    texts = []
    for profile in sentiment_lst:
        try:
            profile = ''.join(profile)
        except:
            continue

        words = analyzer(profile, mecab, stopwords=stopwords.stopwords, target_part_of_speech=['noun', 'proper_noun'])
        
        texts.append(words)
        
    dictionary = gensim.corpora.Dictionary(texts)
    dictionary.filter_extremes(no_below=1, no_above=0.9)
    corpus = [dictionary.doc2bow(t) for t in texts]



    start = 2
    limit = 50
    step = 2

    coherence_vals = []
    perplexity_vals = []

    for n_topic in tqdm(range(start, limit, step)):

        lda_model = gensim.models.ldamodel.LdaModel(corpus=corpus, id2word=dictionary, num_topics=n_topic, random_state=0)
        perplexity_vals.append(np.exp2(-lda_model.log_perplexity(corpus)))
        coherence_model_lda = gensim.models.CoherenceModel(model=lda_model, texts=texts, dictionary=dictionary, coherence='c_v')
        coherence_vals.append(coherence_model_lda.get_coherence())
    

    x = range(start, limit, step)

    fig, ax1 = plt.subplots(figsize=(12,5))

    c1 = 'darkturquoise'
    ax1.plot(x, coherence_vals, 'o-', color=c1)
    ax1.set_xlabel('Num Topics')
    ax1.set_ylabel('Coherence', color=c1); ax1.tick_params('y', colors=c1)

    c2 = 'slategray'
    ax2 = ax1.twinx()
    ax2.plot(x, perplexity_vals, 'o-', color=c2)
    ax2.set_ylabel('Perplexity', color=c2); ax2.tick_params('y', colors=c2)

    ax1.set_xticks(x)
    fig.tight_layout()
    plt.show()
    
    return corpus,dictionary


# In[ ]:


def get_topic_num(df):#感情分析した結果（sentiment）と前処理したprofile(preprocessed_profile)が入ったデータフレームを引数に
    
    #ポジ/ネガ 郡でプロフィールを各リストに分ける
    positive_lst,negative_lst = posi_nega_lst(df)
    
    #プロフィールをでグループに分けるのに、最適なトピック数を算出
    print("分析するキーワードについてポジティブにツイートしたユーザーを、プロフィール情報に基づいてクラスタリングします")
    print("以下に表示されるグラフは何クラスタに分けるかの目安です。横軸がクラスタ数です。グラフ出力後に入力を求められます")
    print("水色のCoherenceが高い値かつ、グレーのPerplexityが低い値を示す数値がうまく分けられるクラスタ数だとされています")
    print("しかし正確なものでは無いため、分析する目的や結果を見て調整してください。")
    posi_corpus,posi_dictionary = plot_best_topics(positive_lst)
    print("分析するキーワードについてネガティブにツイートしたユーザーを、プロフィール情報に基づいてクラスタ分けします")
    print("以下に表示されるグラフは何クラスタに分けるかの目安です。横軸がクラスタ数です。グラフ出力後に入力を求められます")
    print("水色のCoherenceが高い値かつ、グレーのPerplexityが低い値を示す数値がうまく分けられるクラスタ数だとされています")
    print("しかし正確なものでは無いため、分析する目的や結果を見て調整してください。")
    nega_corpus,nega_dictionary = plot_best_topics(negative_lst)
    return posi_corpus,posi_dictionary,nega_corpus,nega_dictionary


# In[ ]:


def plot_topics(posi_corpus,posi_dictionary,nega_corpus,nega_dictionary,folder_name):
    posi_topics = int(input("ポジティブクラスタはいくつに分けますか？数字を半角で入力してください"))
    nega_topics = int(input("ネガティブクラスタはいくつに分けますか？数字を半角で入力してください"))
    #positive
    lda_model = gensim.models.ldamodel.LdaModel(corpus=posi_corpus, id2word=posi_dictionary, num_topics=posi_topics, random_state=0)

    
    for i, t in enumerate(range(lda_model.num_topics)):

        x = dict(lda_model.show_topic(t, 30))
        im = WordCloud(
            font_path='font/TakaoGothic.ttf',
            width=500, height=300,max_words=100, colormap='Dark2',
            background_color='white',random_state=0).generate_from_frequencies(x)
        
        im.to_file('result/{}/positive_group/{}topics_positive_group{}.png'.format(folder_name,posi_topics,i))


    
    #pyLDAvis.enable_notebook()
 
    posi_vis = pyLDAvis.gensim.prepare(lda_model, posi_corpus, posi_dictionary, sort_topics=False)

    pyLDAvis.save_html(posi_vis, 'result/{}/positive_group/{}topics_positive_output.html'.format(folder_name,posi_topics))
    
    #negative
    lda_model = gensim.models.ldamodel.LdaModel(corpus=nega_corpus, id2word=nega_dictionary, num_topics=nega_topics, random_state=0)


    for i, t in enumerate(range(lda_model.num_topics)):

        x = dict(lda_model.show_topic(t, 30))
        im = WordCloud(
            font_path='font/TakaoGothic.ttf',
            width=500, height=300,max_words=100, colormap='Dark2',
            background_color='black',random_state=0).generate_from_frequencies(x)
        
        im.to_file('result/{}/negative_group/{}topics_negative_group{}.png'.format(folder_name,nega_topics,i))


    
     #pyLDAvis.enable_notebook()
 
    nega_vis = pyLDAvis.gensim.prepare(lda_model, nega_corpus, nega_dictionary, sort_topics=False)

    pyLDAvis.save_html(nega_vis, 'result/{}/negative_group/{}topics_negative_output.html'.format(folder_name,nega_topics))
    print("クラスタリングした結果がresultフォルダのpositive/negative_groupフォルダに保存されます")
