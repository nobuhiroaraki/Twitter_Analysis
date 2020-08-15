# Twitter感情分析＆トピック分類

任意のキーワードを含むツイートとプロフィール情報をTwitter上から収集し、各tweetのポジ/ネガを判定します。そしてポジ/ネガtweetをしたアカウントをプロフィール情報をもとにクラスタリングします。

感情分析にはBERT、クラスタリングにはLDAを用いています。


# 事前準備
①Twitter APIの利用申請を行い、APIキー、トークンを取得してください。 <br> https://www.itti.jp/web-direction/how-to-apply-for-twitter-api/

# 使い方
①学習
BERTの事前学習モデルとしては東北大学の乾研究室が作成したものを用いています。<br> https://huggingface.co/transformers/pretrained_models.html <br>

このモデルを日本語tweetデータでポジネガ判定できるようfine-tuningするために、http://www.db.info.gifu-u.ac.jp/data/Data_5d832973308d57446583ed9f で公開されているTwitter日本語評判分析データセットを用います。<br>
利用方法はhttps://github.com/tatHi/tweet_extructor 参考にしてください。<br>

取得したtweetデータとlabelを以下のような形式でcsvファイルにまとめます。





train_model.ipynb(py)を
get_tweet & Analysis.ipynbをjupyternotebook上で実行すればツイートの収集〜クラスタリングから



## Requirement

```python
pip install wordcloud
pip install seaborn
pip install gensim
pip install pyldavis
pip install ipython
```
### 参考にした記事
tweet取得<br>
http://ailaby.com/twitter_api/

BERTによる感情分析<br>
https://qiita.com/namakemono/items/4c779c9898028fc36ff3

LDA<br>

http://www.ie110704.net/2018/12/29/wordcloud%E3%81%A8pyldavis%E3%81%AB%E3%82%88%E3%82%8Blda%E3%81%AE%E5%8F%AF%E8%A6%96%E5%8C%96%E3%81%AB%E3%81%A4%E3%81%84%E3%81%A6/

http://www.ie110704.net/2018/12/29/wordcloud%E3%81%A8pyldavis%E3%81%AB%E3%82%88%E3%82%8Blda%E3%81%AE%E5%8F%AF%E8%A6%96%E5%8C%96%E3%81%AB%E3%81%A4%E3%81%84%E3%81%A6/

