import os
import sys
import time
import tarfile
from selenium import webdriver
from conf import conf

""" [注意]time.sleepを必ず入れること．"""
class AutoDownload():
    def __init__(self):
        self.login_website = 'http://cn.raytracer.cloud:9090/cloudrt/lar/login'
        self.download_website = 'http://cn.raytracer.cloud:9090/cloudrt/download/'
        self.chromedriver_path = conf.chromedriver_path
        self.login_id = conf.login_id
        self.login_pass = conf.login_pass
        self.config_files = [path for path in os.listdir(conf.config_dir) if path.endswith('.json')]
        self.download_dir = conf.download_dir
        self.simulation_profiles = []

    def open_chrome(self):
        chrome_options = webdriver.ChromeOptions()
        prefs = {"download.default_directory" : self.download_dir}
        chrome_options.add_experimental_option("prefs", prefs)
        self.driver = webdriver.Chrome(executable_path=self.chromedriver_path, chrome_options=chrome_options)
        self.driver.get(self.login_website)

    def login(self):
        time.sleep(1)
        self.driver.find_element_by_id('userSigninLogin').send_keys(self.login_id)
        self.driver.find_element_by_id('userSigninPassword').send_keys(self.login_pass)
        time.sleep(1)
        self.driver.find_element_by_css_selector('.ui.blue.button').click()
        time.sleep(1)

    def get_simulation_profiles(self):
        for i in range(1, len(self.config_files) + 1):
            work_name = self.driver.find_element_by_xpath('//div[{}]/div[2]/center'.format(i)).text
            uuid = self.driver.find_element_by_xpath('//div[{}]/div[3]/div[2]/div/small'.format(i)).text
            simulation_prolile = {'work_name' : work_name, 'uuid' : uuid.replace('UUID : ', '')}
            self.simulation_profiles.append(simulation_prolile)

    def download(self):
        uuids = [simulation_profile.get('uuid') for simulation_profile in self.simulation_profiles]
        for i, uuid in enumerate(uuids):
            download_website = self.download_website + uuid + '/result.tar'
            time.sleep(3)
            self.driver.get(download_website)
            print('ダウンロード開始({}/{})'.format(i+1, len(uuids)))
        # ダウンロードの完了を捕捉
        while True:
            is_tarfiles = [download_file.endswith('.tar') for download_file in os.listdir(self.download_dir)]
            exists_false = [is_tarfile for is_tarfile in is_tarfiles if is_tarfile == False]
            if len(exists_false) == 0:
                break
            else:
                time.sleep(3)
        print('ダウンロード完了')

    def open_tar(self):
        os.chdir(self.download_dir)
        for i, simulation_profile in enumerate(self.simulation_profiles):
            work_name = simulation_profile['work_name']
            os.mkdir(work_name)
            time.sleep(0.5)
            if i == 0:
                result_file = 'result.tar'
            else:
                result_file = 'result ({}).tar'.format(i)
            with tarfile.open(result_file, 'r') as tar:
                tar.extractall('{}/'.format(work_name))
            print('展開中... {} => {}/'.format(result_file, work_name))
        print('展開完了')

    def run(self):
        if len(os.listdir(self.download_dir)) != 0:
            print('ダウンロードディレクトリの中身を空にしてください．')
            sys.exit()
        else:
            pass
        self.open_chrome()
        self.login()
        self.get_simulation_profiles()
        self.download()
        self.open_tar()

if __name__ == "__main__":
    adl = AutoDownload()
    adl.run()
