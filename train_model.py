#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import tensorflow as tf
import transformers
from tensorflow import keras
from transformers import BertTokenizer
from sklearn.metrics import accuracy_score
import logging
logging.basicConfig(level=logging.ERROR)


# In[2]:


def train_model(train_path,test_path,num_epoch=10):
  # 訓練データ
  train_df = pd.read_csv(train_path)
  train_texts = train_df.loc[:,"processed_tweet"].values.tolist()
  train_labels =train_df.loc[:,"label"].values.tolist() # 1: 好き, 0: 嫌い
  # テストデータ
  test_df = pd.read_csv(test_path)
  test_texts = test_df.loc[:,"processed_tweet"].values.tolist()
  test_labels =test_df.loc[:,"label"].values.tolist() # 1: 好き, 0: 嫌い
  # model_nameはここから取得(cf. https://huggingface.co/transformers/pretrained_models.html)
  model_name = "cl-tohoku/bert-base-japanese"


  # テキストのリストをtransformers用の入力データに変換
  def to_features(texts, max_length):
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
      model.compile(optimizer=optimizer, loss="binary_crossentropy", metrics=["acc"])
      return model

  num_classes = 2
  max_length = 140
  batch_size = 10
  epochs = num_epoch

  x_train = to_features(train_texts, max_length)
  y_train = tf.keras.utils.to_categorical(train_labels, num_classes=num_classes)
  model = build_model(model_name, num_classes=num_classes, max_length=max_length)

  # 訓練
  model.fit(
      x_train,
      y_train,
      batch_size=batch_size,
      epochs=epochs
  )


  #モデル保存
  model.save_weights("weights/checkpoint")
  print("学習した重みをweightsフォルダに保存しました")
  # 予測
  x_test = to_features(test_texts, max_length)
  y_test = np.asarray(test_labels)
  y_preda = model.predict(x_test)
  y_pred = np.argmax(y_preda, axis=1)
  print("Accuracy: %.5f" % accuracy_score(y_test, y_pred))
  print("TRUE")
  print(y_test)
  print("PREDICT")
  print(y_pred)


# In[ ]:


if __name__ == "__main__":
    train_path = input("訓練データのcsvファイルのpathを入力してください")
    test_path = input("テストデータのcsvファイルのpathを入力してください")
    num_epoch = int(input("何エポックで学習させるか入力してください"))
    train_model(train_path,test_path,num_epoch)

