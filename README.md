# Auto CloudRT
CloudRTを自動で処理します．
## 準備
confディレクトリを作成し，その直下にconf.pyファイルを作成する．

conf.pyに以下のパラメータを記述すること．

```python:conf.py
'''
--------------------
パラメータの説明
--------------------
login_id: string
    CloudRTのID
login_pass: string
    CloudRTのPassword
chromedriver_path: string
    ChromeDriver.exeのパス
config_dir: string
    MATLABで作成したCloudRTのconfigureファイルが置かれているディレクトリのパス
download_dir: string
    ダウンロードファイルが置かれるディレクトリのパス

※パスは絶対パスで記述すること．
--------------------
'''

login_id = '<YOUR ID>'
login_pass = '<YOUR PASSWORD>'
chromedriver_path = r'<YOUR CHROMEDRIVER PATH>'
config_dir = r'<YOUR CONFIG DIR>'
download_dir = r'<YOUR DOWNLOAD DIR>'

```

## 説明
### auto_simulation
    CloudRTに自動登録．
    以下引数．
    --------------------
    retry: int
        Submitに失敗したときリトライする回数(Default: 3)
### auto_download
    CloudRTから自動ダウンロード．
    以下引数．
    --------------------
    rename: bool
        .tarファイル展開後のディレクトリをリネームするかどうか(Default: True)
        (TrueならばWork nameにリネーム)

## 使用ツール
- [CloudRT](http://www.raytracer.cloud/)
- [ChromeDriver](https://sites.google.com/a/chromium.org/chromedriver/)
