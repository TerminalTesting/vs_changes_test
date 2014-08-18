#! /usr/bin/python
# -*- coding: utf-8 -*-
import unittest
import sys
import os, time
from selenium import webdriver
#from sqlalchemy import create_engine, MetaData



class VSChangesTest(unittest.TestCase):
    
    SITE = 'http://nsk.%s/' % os.getenv('SITE')
    HOST = os.getenv('HOST')
    PORT = os.getenv('PORT')
    SCHEMA = os.getenv('SCHEMA')
    USER = os.getenv('USER')
    PSWD = os.getenv('PSWD')
    ARTSOURCE = '%sartifact/' % os.getenv('BUILD_URL')
    #CONNECT_STRING = 'mysql://%s:%s@%s:%s/%s?charset=utf8' %(USER, PSWD, HOST, PORT, SCHEMA)
    #engine = create_engine(CONNECT_STRING, echo=False) #Значение False параметра echo убирает отладочную информацию
    #metadata = MetaData(engine)
    driver = webdriver.Firefox()

    os.system('find -iname \*.png -delete')


    def tearDown(self):
        """Удаление переменных для всех тестов. Остановка приложения"""
        
        self.driver.get('%slogout' % self.SITE)
        self.driver.close()
        if sys.exc_info()[0]:   
            print sys.exc_info()[0]

    def test_vs(self):
        self.driver.get('%slogin' % self.SITE)
        self.driver.find_element_by_id('username').send_keys(os.getenv('AUTH'))
        self.driver.find_element_by_id('password').send_keys(os.getenv('AUTHPASS'))
        self.driver.find_element_by_class_name('btn-primary').click()
        self.driver.get('%sterminal/admin/' % self.SITE)
        time.sleep(5)
        self.driver.find_element_by_partial_link_text(u'тестовый режим').click()
        self.driver.get('%sterminal/admin/site/terminal/tcategory/list' % self.SITE)

        """ Добавление новой ВС """
        cnt = 0
        time.sleep(10)
        self.driver.find_element_by_class_name('add').click()
        name_input = self.driver.find_element_by_class_name('input-tree-node')
        name_input.clear()
        name_input.send_keys('AutotestVS')
        self.driver.find_elements_by_class_name('save')[1].click()
        time.sleep(5)
        self.driver.get('%sterminal/admin/site/terminal/tcategory/list' % self.SITE)
        li = self.driver.find_element_by_class_name('dynatree-container').find_elements_by_tag_name('li')
        vs_names = [x.find_element_by_tag_name('a').text for x in li]

        if 'AutotestVS' not in vs_names:
            cnt += 1
            print u'Ошибка при добавлении ВС'
            self.driver.get_screenshot_as_file('vsAddError.png')
            print u'Скриншот:\n' + self.ARTSOURCE + 'vsAddError.png'
            print

        """ Перемещение ВС """
        time.sleep(5)
        self.driver.find_element_by_link_text('AutotestVS').click()
        self.driver.find_element_by_link_text(u'Общие настройки').click()
        #self.driver.find_element_by_class_name('sonata-ba-collapsed').click()
        self.driver.find_element_by_id('categoryform_parent').click()
        self.driver.find_element_by_id('categoryform_parent').find_elements_by_tag_name('option')[2].click()
        self.driver.find_element_by_class_name('btn-primary').click()
        self.driver.find_element_by_link_text(u'Общие настройки').click()
        option = self.driver.find_element_by_id('categoryform_parent').find_elements_by_tag_name('option')[2]

        if not option.is_selected():
            cnt += 1
            print u'Ошибка при изменении уровня вложенности ВС'
            self.driver.get_screenshot_as_file('vsNestingLevelChangingError.png')
            print u'Скриншот:\n' + self.ARTSOURCE + 'vsNestingLevelChangingError.png'
            print

        """ Перемещение ВС обратно """
        time.sleep(5)
        self.driver.find_element_by_id('categoryform_parent').click()
        self.driver.find_element_by_id('categoryform_parent').find_elements_by_tag_name('option')[0].click()
        self.driver.find_element_by_class_name('btn-primary').click()
        self.driver.find_element_by_link_text(u'Общие настройки').click()
        option = self.driver.find_element_by_id('categoryform_parent').find_elements_by_tag_name('option')[0]

        if not option.is_selected():
            cnt += 1
            print u'Ошибка при изменении уровня вложенности ВС, возврат к прежним настройкам'
            self.driver.get_screenshot_as_file('vsNestingLevelChangingError.png')
            print u'Скриншот:\n' + self.ARTSOURCE + 'vsNestingLevelChangingError.png'
            print

        """ Добавление РС """
        
        time.sleep(5)
        self.driver.find_element_by_class_name('addRsIb').click()
        time.sleep(10)
        #self.driver.execute_script("""$( '.input-collection' ).append( '<input style="display:none" checked="" name="ib[]" value="8d954cfc-0131-11e0-a3a6-0026188b0a94" type="checkbox">' )""")
        self.driver.find_elements_by_class_name('dynatree-checkbox')[7].click()
        time.sleep(5)
        self.driver.find_element_by_class_name('ui-dialog-buttonset').find_elements_by_tag_name('button')[0].click()
        time.sleep(10)
        self.driver.find_element_by_class_name('btn-primary').click()
        time.sleep(10)
        try:
            self.driver.find_element_by_class_name('adminVsNoChanged')
        except:
            cnt += 1
            print u'Ошибка при добавлении РС'
            self.driver.get_screenshot_as_file('vsRsAddError.png')
            print u'Скриншот:\n' + self.ARTSOURCE + 'vsRsAddError.png'
            print

        """ Удаление РС """
        time.sleep(5)
        self.driver.find_element_by_class_name('addRsIb').click()
        time.sleep(10)
        #self.driver.execute_script("""$( '.input-collection' ).empty()""")
        self.driver.find_elements_by_class_name('dynatree-checkbox')[7].click()
        time.sleep(5)
        self.driver.find_element_by_class_name('ui-dialog-buttonset').find_elements_by_tag_name('button')[0].click()
        time.sleep(10)
        self.driver.find_element_by_class_name('btn-primary').click()
        time.sleep(10)
        try:
            self.driver.find_element_by_class_name('adminVsNoChanged')
            print u'Ошибка при удаление РС'
            self.driver.get_screenshot_as_file('vsRsRemoveError.png')
            print u'Скриншот:\n' + self.ARTSOURCE + 'vsRsRemoveError.png'
            cnt += 1
            print
        except:
            pass

        """ Удаление ВС """
        self.driver.find_element_by_link_text('AutotestVS').click()
        time.sleep(5)
        self.driver.find_element_by_class_name('delete').click()
        conf_alert = self.driver.switch_to_alert()
        conf_alert.accept()
        time.sleep(10)
        li = self.driver.find_element_by_class_name('dynatree-container').find_elements_by_tag_name('li')
        vs_names = [x.find_element_by_tag_name('a').text for x in li]

        if 'AutotestVS' in vs_names:
            cnt += 1
            print u'Ошибка при удалении ВС'
            self.driver.get_screenshot_as_file('vsRemoveError.png')
            print u'Скриншот:\n' + self.ARTSOURCE + 'vsRemoveError.png'
            print

        assert cnt == 0, (u'Errors: %d' % cnt)








        
