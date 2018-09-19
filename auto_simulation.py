import os
import sys
import time
from selenium import webdriver
from conf import conf

""" [注意]time.sleepを必ず入れること．"""
class AutoSimulation():
    """
    CloudRTに自動登録．
    以下パラメータ．
    --------------------
    chromedriver_path: string
        ChromeDriver.exeが置いてあるディレクトリパス
    config_dir: string
        MATLABで作成したCloudRTの設定ファイルが置いてあるディレクトリパス
    retry: int
        Submitに失敗したときリトライする回数
    --------------------
    """
    def __init__(self, retry=3):
        self.website = 'http://www.raytracer.cloud/cloudrt/lar/login'
        self.chromedriver_path = conf.chromedriver_path
        self.login_id = conf.login_id
        self.login_pass = conf.login_pass
        self.config_dir = conf.config_dir
        self.config_files = [path for path in os.listdir(self.config_dir) if path.endswith('.json')]
        self.work_names = ([self.config_files[i].replace('configure_', '').replace('.json', '') 
                            for i in range(len(self.config_files))])
        self.retry = retry

    def open_chrome(self):
        self.driver = webdriver.Chrome(executable_path=self.chromedriver_path)
        self.driver.get(self.website)

    def login(self):
        self.driver.find_element_by_id('userSigninLogin').send_keys(self.login_id)
        self.driver.find_element_by_id('userSigninPassword').send_keys(self.login_pass)
        time.sleep(2)
        self.driver.find_element_by_css_selector('.ui.blue.button').click()

    def submit(self, work_name, configuration_file):
        self.driver.find_element_by_id('name').send_keys(work_name)
        self.driver.find_element_by_class_name('webuploader-element-invisible').send_keys(configuration_file)
        # Computing nodesを2に設定
        self.driver.find_element_by_css_selector('.dropdown.icon').click()
        time.sleep(1)
        self.driver.find_element_by_xpath('//div[@data-value="2"]').click()
        time.sleep(2)
        try:
            self.driver.find_element_by_css_selector('.ui.blue.button').click()
            err = ''
        except:
            err = '登録できませんでした．'
        return err

    def quit_driver(self):
        self.driver.quit()

    def run(self):
        self.open_chrome()
        self.login()
        # CloudRT実行
        for i, (work_name, config_file) in enumerate(zip(self.work_names, self.config_files)):
            # New workに移動
            time.sleep(1)
            self.driver.find_element_by_link_text('New work').click()
            for r in range(self.retry):
                res = self.submit(work_name, os.path.join(self.config_dir, config_file))
                print(work_name, os.path.join(self.config_dir, config_file))
                if res == '':
                    # 正常動作時
                    print('登録完了({}/{})'.format(i+1, len(self.config_files)))
                    break
                elif res != '' and i < self.retry-1:
                    # Submitでエラー発生時
                    print(res)
                    print('リトライします．')
                    self.driver.refresh()
                    self.driver.switch_to_alert().accept()
                else:
                    # リトライを繰り返しても登録できない場合
                    print(res)
                    print('処理を終了します．')
                    sys.exit(1)
            # 2018/08/18リリースのCloudRTでは1つのシミュレーションが終わるまで
            # 新たに登録することができなくなったので，終わるまでの時間を入力する
            time.sleep(5)

if __name__ == "__main__":
    asim = AutoSimulation()
    asim.run()
    asim.quit_driver()
