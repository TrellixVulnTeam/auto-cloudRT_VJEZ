import os
import sys
import time
from selenium import webdriver
from conf import conf

""" [注意]time.sleepを必ず入れること．"""
class AutoDownload():
    def __init__(self, rename=True):
        self.login_website = 'http://www.raytracer.cloud/cloudrt/lar/login'
        self.download_website = 'http://www.raytracer.cloud/cloudrt/download/'
        self.chromedriver_path = conf.chromedriver_path
        self.login_id = conf.login_id
        self.login_pass = conf.login_pass
        self.config_files = [path for path in os.listdir(conf.config_dir) if path.endswith('.json')]
        self.download_dir = conf.download_dir
        self.simulation_proliles = []
        self.rename = rename

    def open_chrome(self):
        chrome_options = webdriver.ChromeOptions()
        prefs = {"download.default_directory" : self.download_dir}
        chrome_options.add_experimental_option("prefs", prefs)
        self.driver = webdriver.Chrome(executable_path=self.chromedriver_path, chrome_options = chrome_options)
        self.driver.get(self.login_website)

    def login(self):
        time.sleep(1)
        self.driver.find_element_by_id('userSigninLogin').send_keys(self.login_id)
        self.driver.find_element_by_id('userSigninPassword').send_keys(self.login_pass)
        time.sleep(1)
        self.driver.find_element_by_css_selector('.ui.blue.button').click()
        time.sleep(1)

    def get_simulation_profiles(self):
        """ シミュレーションのWork nameとUUIDをセットで返します． """
        for i in range(1, len(self.config_files) + 1):
            work_name = self.driver.find_element_by_xpath('//div[{}]/div[2]/center'.format(i)).text
            uuid = self.driver.find_element_by_xpath('//div[{}]/div[3]/div[2]/div/small'.format(i)).text
            simulation_prolile = {'work_name' : work_name, 'uuid' : uuid.replace('UUID : ', '')}
            self.simulation_proliles.append(simulation_prolile)
        return self.simulation_proliles

    def download(self, uuids):
        for i, uuid in enumerate(uuids):
            download_website = self.download_website + uuid + '/result.tar'
            time.sleep(3)
            self.driver.get(download_website)
            print('ダウンロード開始({}/{})'.format(i+1, len(uuids)))

    def open_tar(self):
        """ 未実装．手動で展開してください． """
        while True:
            q1 = input('展開しましたか？[y/n]: ')
            if q1 == 'y' or q1 == 'yes':
                break
            else:
                q2 = input('処理を終了しますか？[y/n]: ')
                if q2 == 'y' or q1 == 'yes':
                    sys.exit()
                else:
                    pass

    def re_name(self, simulation_profiles):
        os.chdir(self.download_dir + r'\lustre\jobs')
        for simulation_profile in simulation_profiles:
            os.rename(simulation_profile['uuid'], simulation_profile['work_name'])

    def run(self):
        self.open_chrome()
        self.login()
        simulation_profiles = self.get_simulation_profiles()
        uuids = [d.get('uuid') for d in simulation_profiles]
        self.download(uuids)
        if self.rename == True:
            self.open_tar()
            self.re_name(simulation_profiles)
        else:
            pass

if __name__ == "__main__":
    adl = AutoDownload(rename=True)
    adl.run()
