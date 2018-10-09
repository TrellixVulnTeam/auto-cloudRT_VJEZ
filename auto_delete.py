import sys
import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from conf import conf

""" [注意]time.sleepを必ず入れること．"""
class AutoDelete():
    def __init__(self):
        self.website = 'http://www.raytracer.cloud/cloudrt/lar/login'
        self.chromedriver_path = conf.chromedriver_path
        self.login_id = conf.login_id
        self.login_pass = conf.login_pass
        self.simulation_profiles = []

    def open_chrome(self):
        self.driver = webdriver.Chrome(executable_path=self.chromedriver_path)
        self.driver.get(self.website)

    def login(self):
        self.driver.find_element_by_id('userSigninLogin').send_keys(self.login_id)
        self.driver.find_element_by_id('userSigninPassword').send_keys(self.login_pass)
        time.sleep(2)
        self.driver.find_element_by_css_selector('.ui.blue.button').click()

    def get_all_simulation_profiles(self):
        i = 1
        while True:
            try:
                work_name = self.driver.find_element_by_xpath('//div[{}]/div[2]/center'.format(i)).text
                uuid = self.driver.find_element_by_xpath('//div[{}]/div[3]/div[2]/div/small'.format(i)).text
                simulation_prolile = {'work_name' : work_name, 'uuid' : uuid.replace('UUID : ', '')}
                self.simulation_profiles.append(simulation_prolile)
                i += 1
            except NoSuchElementException:
                break

    def print_all_simulation_profiles(self):
        print('-'*50)
        print('Work No.: Work Name')
        print('-'*50)
        for i, simulation_profile in enumerate(self.simulation_profiles):
            print('{}: {}'.format(i+1, simulation_profile['work_name']))
        print('-'*50)

    def get_delete_index(self):
        print('削除するWork No.の範囲を入力してください．')
        while True:
            try:
                self.start_index = int(input('Start No.: '))
                self.end_index = int(input('End No.: '))
                if self.start_index > self.end_index:
                    print('Start No. < End No. で入力してください．')
                else:
                    break
            except ValueError:
                sys.exit('正しい値を入力してください．')

    def delete(self):
        self.get_delete_index()
        print('-'*50)
        for i in range(self.end_index, self.start_index-1, -1):
            print('{}: {}'.format(i, self.simulation_profiles[i-1]['work_name']))
        print('-'*50)
        check = input('上記のSimulation workを削除します．[y/n]: ')
        if check == 'y' or check == 'yes':
            for i in range(self.end_index, self.start_index-1, -1):
                self.driver.find_element_by_xpath('//div[{}]/div[4]/div[2]/div[3]/a'.format(i)).click()
                print('{}: {} => Deleted.'.format(i, self.simulation_profiles[i-1]['work_name']))
                time.sleep(3)
            print('Complete.')
        else:
            pass

    def run(self):
        self.open_chrome()
        self.login()
        print('Simulation workのリストを取得します．')
        self.get_all_simulation_profiles()
        self.print_all_simulation_profiles()
        self.delete()

if __name__ == "__main__":
    adel = AutoDelete()
    adel.run()
