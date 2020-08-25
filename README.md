# Tweetの感情分析＆ポジ/ネガによるユーザーのクラスタリング

## 目的
#### ➡︎商品やサービスに関するtweetをポジ/ネガ判定し、ポジ/ネガtweetをする人はどんな層の人々なのかを分析する。

サクラレビューやアフィリエイトサイトが乱立する今日で、

・「商品やサービスの真の評判はTwitterに集まるのでは？」<br>
・「Twitterのプロフィール情報はその人の属性をかなり説明するものなのでは？」 

という二つの仮説のもと、真の評判が集まる（はず）tweet情報からをポジ/ネガ分析し、それぞれの感情を抱く潜在的な層をTwitterのプロフィール情報から明らかにしようという試みです。

![Twitter](https://user-images.githubusercontent.com/62980317/91154389-6e9ab080-e6fc-11ea-974d-6d847e578818.jpg) ![パソコン](https://user-images.githubusercontent.com/62980317/91154707-c802df80-e6fc-11ea-8266-5738dc7297d8.jpeg)

## 概要
任意のキーワードを含むツイートとプロフィール情報をTwitter上から収集し、各tweetのポジ/ネガを判定します。<br>
そしてポジ/ネガtweetをしたアカウントを、そのプロフィール情報からクラスタリングします。<br>
感情分析にはBERT(transformers)、クラスタリングにはLDA(gensim)を用いています。


(例)

①「タピオカ」を含むツイートを収集

②収集したツイートのポジ/ネガを判定

③タピオカについてポジティブ（ネガティブ）なツイートをしたアカウントを、プロフィール文の情報を元にクラスタリング

ポジティブクラスタ1➡︎「k-pop・韓国・JK」　　ポジティブクラスタ2➡︎「大学・スタバ・バイト」　　のようなイメージ





## 事前準備

### ①Twitter APIの利用申請を行い、APIキー、トークンを取得してください。 

### ②以下をインストールしてください。

（環境によっては漏れがあるかもしれません。エラーが起きる場合は適宜インストールしてください）
```python
#実行環境
python==3.6.10
tensorflow==2.2.0
$pip install wordcloud
$pip install seaborn
$pip install gensim
$pip install transformers
$pip install pyldavis
$pip install ipython
$pip install requests requests_oauthlib
$brew install mecab
$brew install mecab-ipadic
$brew install swig
$pip install mecab-python3
```

#### ③fine-tuning用データセット作成

BERTの事前学習モデルとして、東北大学の乾研究室が作成したPretrained Japanese BERT modelsを用いています。<br>
https://github.com/cl-tohoku/bert-japanese

このモデルを日本語tweetデータでポジネガ判定できるようfine-tuningします。<br> 

fine-tuningのためのデータセット作成として以下の2種類の方法があります。

(1)特定のキーワードに特化して判定させる場合（300件のデータでfine-tuningした結果、精度75%前後）

ターミナル上で以下のように実行してください
```python
python3 get_tweet.py #分析したいキーワードのツイートを収集します。
python3 preprocessing.py #ツイートを前処理(結果はdataフォルダにprocessed.csvとして保存されます)
```
そしてprocessed.csvを下記表と同じ形式に編集します。<br>
processed_tweetの列以外を削除して、新たにlabelという列を追加してください。<br>
そして各tweetポジティブ(1)なのか、ネガティブ(0)なのかラベル付けを行ってください。

<img width="713" alt="スクリーンショット 2020-08-13 1 52 31" src="https://user-images.githubusercontent.com/62980317/90303682-d9710e00-deea-11ea-84f9-51febc342b14.png">


(2)どのような話題に対しても汎用的な推測を行う場合（精度65~70%前後）

汎用的な話題に対して推測を行うには大量のデータが必要です。<br>
しかし自力で大量にラベル付けを行うのは大変なため、以下で公開されている大規模なTwitter日本語評判分析データセットを用います。<br>
http://www.db.info.gifu-u.ac.jp/data/Data_5d832973308d57446583ed9f <br>
利用方法はhttps://github.com/tatHi/tweet_extructor を参考にしてください。
取得したtweetデータとlabelを上記と同様の形式でcsvファイルにまとめます。

### ④学習

作成したcsvファイルをTwitter_Analysisファイル内に保存して、train_model.ipynbの全てのセルを実行してください。(時間がかかるためGoogle colab等でGPUの利用を推奨)


## 使い方

### 分析
Analysis.py()を実行し、表示に従って操作することで感情分析〜クラスタリングまで行うことができます<br>

Twitter日本語評判分析データセットを使って学習させた重みがある場合、どんな話題にもある程度対応できるため<br>
get_tweet & Analysis.ipynbの全てのセルを実行することで、ツイートの収集〜分析まで一括で行うことができます)

予測結果はresultフォルダに保存されます。


## 参考にした記事

tweet取得<br>
http://ailaby.com/twitter_api/

BERTによる感情分析<br>
https://qiita.com/namakemono/items/4c779c9898028fc36ff3

LDA<br>
http://www.ie110704.net/2018/12/29/wordcloud%E3%81%A8pyldavis%E3%81%AB%E3%82%88%E3%82%8Blda%E3%81%AE%E5%8F%AF%E8%A6%96%E5%8C%96%E3%81%AB%E3%81%A4%E3%81%84%E3%81%A6/
