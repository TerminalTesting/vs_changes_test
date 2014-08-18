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
        self.driver.find_elements_by_class_name('dynatree-checkbox')[2].click()
        time.sleep(5)
        self.driver.find_element_by_class_name('ui-dialog-buttonset').find_elements_by_tag_name('button')[0].click()
        time.sleep(15)
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

        """ Изменение данных ВС """
        #Общие настройки
        self.driver.find_element_by_link_text(u'Общие настройки').click()
        self.driver.find_element_by_id('categoryform_active').click()
        self.driver.find_element_by_id('categoryform_name').clear()
        self.driver.find_element_by_id('categoryform_name').send_keys('AutotestVSName')
        self.driver.find_element_by_id('categoryform_alias').clear()
        self.driver.find_element_by_id('categoryform_alias').send_keys('AutotestVSAlias')
        self.driver.find_element_by_id('categoryform_menuColumnNumber').click()
        self.driver.find_element_by_id('categoryform_menuColumnNumber').find_elements_by_tag_name('option')[1].click()
        self.driver.execute_script("""$( '#categoryform_sort' ).attr('value', 777 )""")
        self.driver.find_element_by_id('categoryform_description').send_keys('AutotestVSDescription')
        self.driver.find_element_by_id('categoryform_picture').send_keys('AutotestVSPicture')
        
        self.driver.find_element_by_id('categoryform_flagBrand').click()
        self.driver.find_element_by_id('categoryform_flagNew').click()
        self.driver.find_element_by_id('categoryform_flagBrandLevel').click()
        self.driver.find_element_by_id('categoryform_flagHideBrandLevel').click()
        self.driver.find_element_by_id('categoryform_flagTermShow').click()
        self.driver.find_element_by_id('categoryform_flagSetGroup').click()
        self.driver.find_element_by_id('categoryform_showPromoBlock').click()
        
        self.driver.find_element_by_id('categoryform_externalLink').send_keys('AutotestVSLink')

        #Служебные настройки
        self.driver.find_element_by_link_text(u'Служебные настройки').click()
        #self.driver.find_element_by_id('categoryform_oldId').send_keys('AutotestVSoldId')
        #self.driver.find_element_by_id('categoryform_oldAlias').send_keys('AutotestVSoldAlias')

        #SEO - настройки
        self.driver.find_element_by_link_text(u'SEO - настройки').click()
        self.driver.find_element_by_id('categoryform_metaTitle').send_keys('AutotestVSmetaTitle')
        self.driver.find_element_by_id('categoryform_metaKeywords').send_keys('AutotestVSmetaKeywords')
        self.driver.find_element_by_id('categoryform_metaDescription').send_keys('AutotestVSmetaDescription')
        self.driver.find_element_by_id('categoryform_metaH1').send_keys('AutotestVSmetaH1')
        self.driver.find_element_by_id('categoryform_singularName').send_keys('AutotestVSsingularName')
        self.driver.find_element_by_id('categoryform_translitName').send_keys('AutotestVStranslitName')
        
        self.driver.find_element_by_class_name('btn-primary').click()#save changes

        #Общие настройки
        self.driver.find_element_by_link_text(u'Общие настройки').click()
        if not self.driver.find_element_by_id('categoryform_active').is_selected():
            cnt += 1
            print 'Флаг активности не снялся'
            print
        if self.driver.find_element_by_id('categoryform_name').get_attribute('value') != 'AutotestVSName':
            cnt += 1
            print 'Текст categoryform_name не изменился - ', self.driver.find_element_by_id('categoryform_name').get_attribute('value')
            print
        if self.driver.find_element_by_id('categoryform_alias').get_attribute('value') != 'AutotestVSAlias':
            cnt += 1
            print 'Текст categoryform_alias не изменился - ', self.driver.find_element_by_id('categoryform_alias').get_attribute('value')
            print
        self.driver.find_element_by_id('categoryform_menuColumnNumber').click()
        if self.driver.find_element_by_id('categoryform_menuColumnNumber').find_elements_by_tag_name('option')[1].get_attribute('selected') != 'selected':
            cnt += 1
            print 'Значение в categoryform_menuColumnNumber не изменилось - ', self.driver.find_element_by_id('categoryform_menuColumnNumber').find_elements_by_tag_name('option')[1].get_attribute('selected')
            print
        if self.driver.find_element_by_id('categoryform_sort').get_attribute('value') != '777':
            cnt += 1
            print 'Значение в categoryform_sort не изменилось - ', self.driver.find_element_by_id('categoryform_sort').get_attribute('value')
            print
        if self.driver.find_element_by_id('categoryform_description').get_attribute('value') != 'AutotestVSDescription':
            cnt += 1
            print 'Текст categoryform_description не изменился - ', self.driver.find_element_by_id('categoryform_description').get_attribute('value')
            print
        if self.driver.find_element_by_id('categoryform_picture').get_attribute('value') != 'AutotestVSPicture':
            cnt += 1
            print 'Текст categoryform_picture не изменился - ', self.driver.find_element_by_id('categoryform_picture').get_attribute('value')
            print
        
        if not self.driver.find_element_by_id('categoryform_flagBrand').is_selected():
            cnt += 1
            print 'Флаг Brand не установился'
            print
        if not self.driver.find_element_by_id('categoryform_flagNew').is_selected():
            cnt += 1
            print 'Флаг New не установился'
            print
        if not self.driver.find_element_by_id('categoryform_flagBrandLevel').is_selected():
            cnt += 1
            print 'Флаг BrandLevel не установился'
            print
        if not self.driver.find_element_by_id('categoryform_flagHideBrandLevel').is_selected():
            cnt += 1
            print 'Флаг HideBrandLevel не установился'
            print
        if self.driver.find_element_by_id('categoryform_flagTermShow').is_selected():
            cnt += 1
            print 'Флаг TermShow не снялся'
            print
        if not self.driver.find_element_by_id('categoryform_flagSetGroup').is_selected():
            cnt += 1
            print 'Флаг SetGroup не установился'
            print
        if not self.driver.find_element_by_id('categoryform_showPromoBlock').is_selected():
            cnt += 1
            print 'Флаг PromoBlock не установился'
            print
        
        if self.driver.find_element_by_id('categoryform_externalLink').get_attribute('value') != 'AutotestVSLink':
            cnt += 1
            print 'Текст externalLink не изменился - ', self.driver.find_element_by_id('categoryform_externalLink').get_attribute('value')
            print

        #Служебные настройки
        self.driver.find_element_by_link_text(u'Служебные настройки').click()
        #if self.driver.find_element_by_id('categoryform_oldId').get_attribute('value') != 'AutotestVSoldId':
        #    cnt += 1
        #    print 'Текст categoryform_oldId не изменился - ', self.driver.find_element_by_id('categoryform_oldId').get_attribute('value')
        #    print
        #if self.driver.find_element_by_id('categoryform_oldAlias').get_attribute('value') != 'AutotestVSoldAlias':
        #    cnt += 1
        #    print 'Текст categoryform_oldAlias не изменился - ', self.driver.find_element_by_id('categoryform_oldAlias').get_attribute('value')
        #    print

        #SEO - настройки
        self.driver.find_element_by_link_text(u'SEO - настройки').click()
        if self.driver.find_element_by_id('categoryform_metaTitle').get_attribute('value') != 'AutotestVSmetaTitle':
            cnt += 1
            print 'Текст categoryform_metaTitle не изменился - ', self.driver.find_element_by_id('categoryform_metaTitle').get_attribute('value')
            print
        if self.driver.find_element_by_id('categoryform_metaKeywords').get_attribute('value') != 'AutotestVSmetaKeywords':
            cnt += 1
            print 'Текст categoryform_metaKeywords не изменился - ', self.driver.find_element_by_id('categoryform_metaKeywords').get_attribute('value')
            print
        if self.driver.find_element_by_id('categoryform_metaDescription').get_attribute('value') != 'AutotestVSmetaDescription':
            cnt += 1
            print 'Текст categoryform_metaDescription не изменился - ', self.driver.find_element_by_id('categoryform_metaDescription').get_attribute('value')
            print
        if self.driver.find_element_by_id('categoryform_metaH1').get_attribute('value') != 'AutotestVSmetaH1':
            cnt += 1
            print 'Текст categoryform_metaH1 не изменился - ', self.driver.find_element_by_id('categoryform_metaH1').get_attribute('value')
            print
        if self.driver.find_element_by_id('categoryform_singularName').get_attribute('value') != 'AutotestVSsingularName':
            cnt += 1
            print 'Текст categoryform_singularName не изменился - ', self.driver.find_element_by_id('categoryform_singularName').get_attribute('value')
            print
        if self.driver.find_element_by_id('categoryform_translitName').get_attribute('value') != 'AutotestVStranslitName':
            cnt += 1
            print 'Текст categoryform_translitName не изменился - ', self.driver.find_element_by_id('categoryform_translitName').get_attribute('value')
            print

        

        """ Удаление ВС """
        self.driver.find_element_by_link_text('AutotestVSName').click()
        time.sleep(5)
        self.driver.find_element_by_class_name('delete').click()
        self.driver.switch_to_alert().accept()
        time.sleep(10)
        li = self.driver.find_element_by_class_name('dynatree-container').find_elements_by_tag_name('li')
        vs_names = [x.find_element_by_tag_name('a').text for x in li]

        if 'AutotestVSName' in vs_names:
            cnt += 1
            print u'Ошибка при удалении ВС'
            self.driver.get_screenshot_as_file('vsRemoveError.png')
            print u'Скриншот:\n' + self.ARTSOURCE + 'vsRemoveError.png'
            print

        assert cnt == 0, (u'Errors: %d' % cnt)
