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
    ひとつのファイルを登録後，シミュレーションが終わるまで待機し，終わり次第次のファイルを自動で登録する．
    ※configureファイルは必ず'configure_'から始まる名前にすること．
    　Work nameはconfigureファイル名から'configure_'が引かれた名前で設定される．

    以下引数．
    --------------------
    retry: int
        Submitに失敗したときリトライする回数(Default: 3)

### auto_download
    CloudRTから自動ダウンロード．
    config_dirで指定したディレクトリ内に入っている.jsonファイルの数だけCloudRTから順番にダンロードする．
    展開後のディレクトリ構成：
        <download_dir>/<work_name>/result/
    ※ダウンロードディレクトリの中身を空にしてから実行すること．
    
### auto_delete
    CloudRTのSimulation workを自動削除．
    標準入力から削除する範囲を指定する．

## 使用ツール
- [CloudRT](http://www.raytracer.cloud/)
- [ChromeDriver](https://sites.google.com/a/chromium.org/chromedriver/)
