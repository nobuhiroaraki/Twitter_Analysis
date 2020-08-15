#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow import keras
import transformers
from transformers import BertTokenizer
import warnings
warnings.simplefilter('ignore')


# In[ ]:


# 単一テキストをクラス分類するモデルの構築
def build_model(model_name, num_classes, max_length):
    input_shape = (max_length, )
    input_ids = tf.keras.layers.Input(input_shape, dtype=tf.int32)
    attention_mask = tf.keras.layers.Input(input_shape, dtype=tf.int32)
    token_type_ids = tf.keras.layers.Input(input_shape, dtype=tf.int32)
    bert_model = transformers.TFBertModel.from_pretrained(model_name)
    last_hidden_state, pooler_output = bert_model(
        input_ids,
        attention_mask=attention_mask,
        token_type_ids=token_type_ids
    )
    output = tf.keras.layers.Dense(num_classes, activation="softmax")(pooler_output)
    model = tf.keras.Model(inputs=[input_ids, attention_mask, token_type_ids], outputs=[output])
    optimizer = tf.keras.optimizers.Adam(learning_rate=3e-5, epsilon=1e-08, clipnorm=1.0)
    model.compile(optimizer=optimizer, loss="binaey_crossentropy", metrics=["acc"])
    return model


# In[ ]:


# テキストのリストをtransformers用の入力データに変換
def to_features(texts, max_length):
    model_name = "cl-tohoku/bert-base-japanese"
    tokenizer = BertTokenizer.from_pretrained(model_name)
    shape = (len(texts), max_length)
    # input_idsやattention_mask, token_type_idsの説明はglossaryに記載(cf. https://huggingface.co/transformers/glossary.html)
    input_ids = np.zeros(shape, dtype="int32")
    attention_mask = np.zeros(shape, dtype="int32")
    token_type_ids = np.zeros(shape, dtype="int32")
    for i, text in enumerate(texts):
        try:
            encoded_dict = tokenizer.encode_plus(text, max_length=max_length, pad_to_max_length=True)
        except:
            pass
        input_ids[i] = encoded_dict["input_ids"]
        attention_mask[i] = encoded_dict["attention_mask"]
        token_type_ids[i] = encoded_dict["token_type_ids"]
    return [input_ids, attention_mask, token_type_ids]


# In[ ]:


def sentiment_predict(df,folder_name):
    model_name = "cl-tohoku/bert-base-japanese"
    num_classes = 2
    max_length = 140
    batch_size = 10

    # テストデータ
    test_texts = df.loc[:,"processed_tweet"].values.tolist()
    
    #学習済モデルロード
    load_model = build_model(model_name, num_classes=num_classes, max_length=max_length)
    load_model.load_weights('weights/checkpoint')


    # 予測
    print("各ツイートがポジティブなのかネガティブなのか判定しています。時間がかかるためしばらくお待ちください")
    x_test = to_features(test_texts, max_length)
    y_preda = load_model.predict(x_test)
    y_pred = np.argmax(y_preda, axis=1)

    
    df["sentiment"] = y_pred
    print("判定が完了しました")
    
    negative_count = df["sentiment"]==0
    positive_count = df["sentiment"]==1
    
    if negative_count.sum()==0:
        print("nagativeと予測されたツイートが一つもありません。学習しなおしてください")
    elif positive_count.sum()==0:
        print("positiveと予測されたツイートが一つもありません。学習しなおしてください")
    
    df.to_csv("result/{}/eval_result.csv".format(folder_name))
    
    return df

