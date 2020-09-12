# Tweetの感情分析＆ポジ/ネガによるアカウントのクラスタリング

## 目的
#### ➡︎特定のキーワードを含むtweetをポジ/ネガ判定し、特定のキーワードについてポジ/ネガtweetをする人はどんな層の人々なのかを分析する

サクラレビューやアフィリエイトサイトが乱立し、信頼できる「真の評判」を見分けるのが難しい今日で、

・「商品やサービスの「真の評判」はTwitterに集まるのでは？」<br>
・「Twitterのプロフィール情報はその人の属性をかなり説明するものなのでは？」 

という二つの仮説のもと、真の評判が集まる（はず）tweet情報からをポジ/ネガ分析し、<br>
それぞれの感情を抱く潜在的な層をTwitterのプロフィール情報から明らかにしようという試みです。

![img_1598775840](https://user-images.githubusercontent.com/62980317/91654890-9e282f00-eae7-11ea-9fe8-3354e6fecba6.jpg)

## 概要
任意のキーワードを含むツイートとプロフィール情報をTwitter上から収集し、各tweetのポジ/ネガを判定します。<br>
そしてポジ/ネガtweetをしたアカウントを、そのプロフィール情報からクラスタリングします。<br>
感情分析にはBERT(transformers)、クラスタリングにはLDA(gensim)を用いています。<br>
dockerで環境を構築しています。<br>
もしdocker環境が整っていないようであればこのリポジトリをcloneして使ってください。

(例)

①「タピオカ」を含むツイートを収集

②収集したツイートのポジ/ネガを判定

③タピオカについてポジティブ（ネガティブ）なツイートをしたアカウントを、プロフィール文の情報を元にクラスタリング

ポジティブクラスタ1➡︎「k-pop・韓国・JK」　　ポジティブクラスタ2➡︎「大学・スタバ・バイト」のようなイメージ



## 利用方法

### ①Twitter APIの利用申請を行い、APIキー、トークンを取得

### ②リポジトリをクローン
```
git clone https://github.com/nobuhiroaraki/Twitter_Analysis.git
```

### ③ Twitter_Analysisフォルダをgoogle driveにアップロード

### ④Google Colab上の環境構築

GPUに接続してdriveにマウントします。

接続できたら以下のコマンドを入力してください。

```python
cd drive/My\ Drive/Twitter_Analysis

!pip install tensorflow
!pip install wordcloud
!pip install seaborn
!pip install gensim
!pip install transformers
!pip install pyldavis
!pip install ipython
!pip install requests requests_oauthlib
!pip install emoji
!apt install aptitude
!aptitude install mecab libmecab-dev mecab-ipadic-utf8 git make curl xz-utils file -y
!git clone --depth 1 https://github.com/neologd/mecab-ipadic-neologd.git
!echo yes | mecab-ipadic-neologd/bin/install-mecab-ipadic-neologd -n
!apt-get -q -y install swig 
!pip install mecab-python3
```

### ⑤fine-tuning用データセット作成

BERTの事前学習モデルとして、東北大学の乾研究室が作成したPretrained Japanese BERT modelsを用いています。<br>
https://github.com/cl-tohoku/bert-japanese

このモデルを日本語tweetデータでポジネガ判定できるようfine-tuningします。<br> 

fine-tuningのためのデータセット作成として以下の2種類の方法があります。


#### (1)どのような話題に対しても汎用的に推測を行う場合（精度65~70%前後）

様々な話題に対して汎用的に推測を行うには大量のデータが必要です。<br>
しかし自力で大量にラベル付けを行うのは大変なため、以下で公開されている大規模なTwitter日本語評判分析データセットを用います。<br>
http://www.db.info.gifu-u.ac.jp/data/Data_5d832973308d57446583ed9f


利用方法はhttps://github.com/tatHi/tweet_extructor を参考にしてください。<br>


取得したtweetデータと感情判定(ポジティブ=1、ネガティブ=0)を、下記と同様の形式でcsvファイルにまとめます。


<img width="716" alt="スクリーンショット 2020-08-26 18 57 09" src="https://user-images.githubusercontent.com/62980317/91290065-1fbd4b80-e7ce-11ea-98cd-b5ee06236764.png">

#### (2)特定のキーワードに特化して判定させる場合（300件のデータでfine-tuningした結果、精度75%前後）

notebook上で以下のように実行し、表示に従って操作してください
```python
from get_tweet import get_tweet
from preprocessing import preprocessing
get_tweet()
preprocessing()
```
そしてprocessed.csvを上記表と同じ形式に編集します。<br>
そして各tweetをポジティブ(1)なのか、ネガティブ(0)なのかラベル付けを行ってください。



### ⑥学習

作成したcsvファイルをtrain_dataフォルダ内に保存して、
notebook上で以下のように実行し、表示に従って操作してください
```python
from train_model import train_model
train_model()
```

## 分析
notebook上で以下のように実行し、表示に従って操作してください
```python
from train_model import train_model
train_model()
```
表示に従って操作することでツイートの収集・感情分析・クラスタリングを行うことができます。

分析結果はresultフォルダに保存されます。


## 結果例

### 「タピオカ」を含むツイートをしたアカウントを、プロフィール情報をもとにクラスタリングした結果(抜粋)

#### ポジティブクラスタ例

![3topics_positive_group1](https://user-images.githubusercontent.com/62980317/91171837-2a1c0e80-e716-11ea-96e2-fb20db7a8b96.png)

<img width="1415" alt="スクリーンショット 2020-08-25 20 32 57" src="https://user-images.githubusercontent.com/62980317/91171854-3738fd80-e716-11ea-80f0-6bad3cab955e.png">

#### ネガティブクラスタ例

![4topics_negative_group2](https://user-images.githubusercontent.com/62980317/91171975-6d767d00-e716-11ea-9ecf-6795a8598813.png)

<img width="1408" alt="スクリーンショット 2020-08-25 20 32 16" src="https://user-images.githubusercontent.com/62980317/91171988-71a29a80-e716-11ea-9e80-6b958f882f02.png">


## 参考にした記事

http://ailaby.com/twitter_api/ <br>
https://qiita.com/namakemono/items/4c779c9898028fc36ff3 <br>
http://www.ie110704.net/2018/12/29/wordcloud%E3%81%A8pyldavis%E3%81%AB%E3%82%88%E3%82%8Blda%E3%81%AE%E5%8F%AF%E8%A6%96%E5%8C%96%E3%81%AB%E3%81%A4%E3%81%84%E3%81%A6/
