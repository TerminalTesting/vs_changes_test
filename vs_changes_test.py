#! /usr/bin/python
# -*- coding: utf-8 -*-
import unittest
import sys
import os, time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#from sqlalchemy import create_engine, MetaData



class VSChangesTest(unittest.TestCase):

    def setUp(self):
        #delete old screenshot artifacts
        os.system('find -iname \*.png -delete')
    
        self.SITE = 'http://nsk.%s/' % os.getenv('SITE')
        self.ARTSOURCE = '%sartifact/' % os.getenv('BUILD_URL')
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(5)


    def tearDown(self):
        """Удаление переменных для всех тестов. Остановка приложения"""
        
        self.driver.get('%slogout' % self.SITE)
        self.driver.close()
        if sys.exc_info()[0]:   
            print sys.exc_info()[0]

    def is_element_present(self, how, what, timeout=10):
        """ Поиск элемента по локатору

            По умолчанию таймаут 10 секунд, не влияет на скорость выполнения теста
            если элемент найден, если нет - ждет его появления 10 сек
            
            Параметры:
               how - метод поиска
               what - локатор
            Методы - атрибуты класса By:
             |  CLASS_NAME = 'class name'
             |  
             |  CSS_SELECTOR = 'css selector'
             |  
             |  ID = 'id'
             |  
             |  LINK_TEXT = 'link text'
             |  
             |  NAME = 'name'
             |  
             |  PARTIAL_LINK_TEXT = 'partial link text'
             |  
             |  TAG_NAME = 'tag name'
             |  
             |  XPATH = 'xpath'
                                             """
	try:
            return WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located((how, what)))
	except:
            print u'Элемент не найден'
	    print 'URL: ', self.driver.current_url
	    print u'Метод поиска: ', how
	    print u'Локатор: ', what
	    screen_name = '%d.png' % int(time.time())
	    self.driver.get_screenshot_as_file(screen_name)
	    print u'Скриншот страницы: ', self.ARTSOURCE + screen_name
	    raise Exception('ElementNotPresent')

    def test_vs(self):

        driver = self.driver
        element = self.is_element_present
        
        driver.get('%slogin' % self.SITE)
        element(By.ID, 'username').send_keys(os.getenv('AUTH'))
        element(By.ID, 'password').send_keys(os.getenv('AUTHPASS'))
        element(By.CLASS_NAME, 'btn-primary').click()
        time.sleep(7)
        driver.get('%sterminal/admin/' % self.SITE)
        element(By.PARTIAL_LINK_TEXT, u'тестовый режим').click()
        driver.get('%sterminal/admin/site/terminal/tcategory/list' % self.SITE)

        """ Добавление новой ВС """
        cnt = 0
        element(By.CLASS_NAME, 'add').click()
        name_input = element(By.CLASS_NAME, 'input-tree-node')
        name_input.clear()
        name_input.send_keys('AutotestVS')
        self.driver.find_elements_by_class_name('save')[1].click()
        driver.refresh()
        li = element(By.CLASS_NAME, 'dynatree-container').find_elements_by_tag_name('li')
        vs_names = [x.find_element_by_tag_name('a').text for x in li]

        if 'AutotestVS' not in vs_names:
            cnt += 1
            print u'Ошибка при добавлении ВС'
            self.driver.get_screenshot_as_file('vsAddError.png')
            print u'Скриншот:\n' + self.ARTSOURCE + 'vsAddError.png'
            print

        """ Перемещение ВС """
        time.sleep(5)
        element(By.LINK_TEXT, 'AutotestVS').click()
        element(By.LINK_TEXT, u'Общие настройки').click()
        #self.driver.find_element_by_class_name('sonata-ba-collapsed').click()
        element(By.ID, 'categoryform_parent').click()
        element(By.ID, 'categoryform_parent').find_elements_by_tag_name('option')[2].click()
        element(By.CLASS_NAME, 'btn-primary').click()
        element(By.LINK_TEXT, u'Общие настройки').click()
        option = element(By.ID, 'categoryform_parent').find_elements_by_tag_name('option')[2]

        if not option.is_selected():
            cnt += 1
            print u'Ошибка при изменении уровня вложенности ВС'
            driver.get_screenshot_as_file('vsNestingLevelChangingError.png')
            print u'Скриншот:\n' + self.ARTSOURCE + 'vsNestingLevelChangingError.png'
            print

        """ Перемещение ВС обратно """
        time.sleep(5)
        element(By.ID, 'categoryform_parent').click()
        element(By.ID, 'categoryform_parent').find_elements_by_tag_name('option')[0].click()
        element(By.CLASS_NAME, 'btn-primary').click()
        element(By.LINK_TEXT, u'Общие настройки').click()
        option = element(By.ID, 'categoryform_parent').find_elements_by_tag_name('option')[0]

        if not option.is_selected():
            cnt += 1
            print u'Ошибка при изменении уровня вложенности ВС, возврат к прежним настройкам'
            driver.get_screenshot_as_file('vsNestingLevelChangingError.png')
            print u'Скриншот:\n' + self.ARTSOURCE + 'vsNestingLevelChangingError.png'
            print

        """ Добавление РС """
        
        time.sleep(5)
        element(By.CLASS_NAME, 'addRsIb').click()
        time.sleep(10)
        #self.driver.execute_script("""$( '.input-collection' ).append( '<input style="display:none" checked="" name="ib[]" value="8d954cfc-0131-11e0-a3a6-0026188b0a94" type="checkbox">' )""")
        driver.find_elements_by_class_name('dynatree-checkbox')[2].click()
        time.sleep(5)
        element(By.CLASS_NAME, 'ui-dialog-buttonset').find_elements_by_tag_name('button')[0].click()
        time.sleep(15)
        element(By.CLASS_NAME, 'btn-primary').click()
        time.sleep(10)
        try:
            element(By.CLASS_NAME, 'adminVsNoChanged')
        except:
            cnt += 1
            print u'Ошибка при добавлении РС'
            driver.get_screenshot_as_file('vsRsAddError.png')
            print u'Скриншот:\n' + self.ARTSOURCE + 'vsRsAddError.png'
            print

        """ Изменение данных ВС """
        #Общие настройки
        element(By.LINK_TEXT, u'Общие настройки').click()
        element(By.ID, 'categoryform_active').click()
        element(By.ID, 'categoryform_name').clear()
        element(By.ID, 'categoryform_name').send_keys('AutotestVSName')
        element(By.ID, 'categoryform_alias').clear()
        element(By.ID, 'categoryform_alias').send_keys('AutotestVSAlias')
        element(By.ID, 'categoryform_menuColumnNumber').click()
        element(By.ID, 'categoryform_menuColumnNumber').find_elements_by_tag_name('option')[1].click()
        driver.execute_script("""$( '#categoryform_sort' ).attr('value', 777 )""")
        element(By.ID, 'categoryform_description').send_keys('AutotestVSDescription')
        element(By.ID, 'categoryform_picture').send_keys('AutotestVSPicture')
        
        element(By.ID, 'categoryform_flagBrand').click()
        element(By.ID, 'categoryform_flagNew').click()
        element(By.ID, 'categoryform_flagBrandLevel').click()
        element(By.ID, 'categoryform_flagHideBrandLevel').click()
        element(By.ID, 'categoryform_flagTermShow').click()
        element(By.ID, 'categoryform_flagSetGroup').click()
        element(By.ID, 'categoryform_showPromoBlock').click()
        
        element(By.ID, 'categoryform_externalLink').send_keys('AutotestVSLink')

        #Служебные настройки
        element(By.LINK_TEXT, u'Служебные настройки').click()
        #self.driver.find_element_by_id('categoryform_oldId').send_keys('AutotestVSoldId')
        #self.driver.find_element_by_id('categoryform_oldAlias').send_keys('AutotestVSoldAlias')

        #SEO - настройки
        element(By.LINK_TEXT, u'SEO - настройки').click()
        element(By.ID, 'categoryform_metaTitle').send_keys('AutotestVSmetaTitle')
        element(By.ID, 'categoryform_metaKeywords').send_keys('AutotestVSmetaKeywords')
        element(By.ID, 'categoryform_metaDescription').send_keys('AutotestVSmetaDescription')
        element(By.ID, 'categoryform_metaH1').send_keys('AutotestVSmetaH1')
        element(By.ID, 'categoryform_singularName').send_keys('AutotestVSsingularName')
        element(By.ID, 'categoryform_translitName').send_keys('AutotestVStranslitName')
        
        element(By.CLASS_NAME, 'btn-primary').click()#save changes

        #Общие настройки
        element(By.LINK_TEXT, u'Общие настройки').click()
        if element(By.ID, 'categoryform_active').is_selected():
            cnt += 1
            print 'Флаг активности не снялся'
            print
        if element(By.ID, 'categoryform_name').get_attribute('value') != 'AutotestVSName':
            cnt += 1
            print 'Текст поля "Название" не изменился - ', element(By.ID, 'categoryform_name').get_attribute('value')
            print
        if element(By.ID, 'categoryform_alias').get_attribute('value') != 'AutotestVSAlias':
            cnt += 1
            print 'Текст поля "Alias секции" не изменился - ', element(By.ID, 'categoryform_alias').get_attribute('value')
            print
        element(By.ID, 'categoryform_menuColumnNumber').click()
        if element(By.ID, 'categoryform_menuColumnNumber').find_elements_by_tag_name('option')[1].get_attribute('selected') != 'true':
            cnt += 1
            print 'Значение в поле "Столбец в top меню" не изменилось - ', element(By.ID, 'categoryform_menuColumnNumber').find_elements_by_tag_name('option')[1].get_attribute('selected')
            print
        if element(By.ID, 'categoryform_sort').get_attribute('value') != '777':
            cnt += 1
            print 'Значение в поле "Сортировка" не изменилось - ', element(By.ID, 'categoryform_sort').get_attribute('value')
            print
        if element(By.ID, 'categoryform_description').get_attribute('value') != 'AutotestVSDescription':
            cnt += 1
            print 'Текст поля "Описание" не изменился - ', element(By.ID, 'categoryform_description').get_attribute('value')
            print
        if element(By.ID, 'categoryform_picture').get_attribute('value') != 'AutotestVSPicture':
            cnt += 1
            print 'Текст поля "Изображение в меню" не изменился - ', element(By.ID, 'categoryform_picture').get_attribute('value')
            print
        
        if not element(By.ID, 'categoryform_flagBrand').is_selected():
            cnt += 1
            print 'Флаг "Наличие подбора по параметрам" не установился'
            print
        if not element(By.ID, 'categoryform_flagNew').is_selected():
            cnt += 1
            print 'Флаг "ВС-новинка" не установился'
            print
        if not element(By.ID, 'categoryform_flagBrandLevel').is_selected():
            cnt += 1
            print 'Флаг "Брендовая категория" не установился'
            print
        if not element(By.ID, 'categoryform_flagHideBrandLevel').is_selected():
            cnt += 1
            print 'Флаг "Скрыть брендовый уровень в топ-меню" не установился'
            print
        if element(By.ID, 'categoryform_flagTermShow').is_selected():
            cnt += 1
            print 'Флаг "Показывать для терминалов" не снялся'
            print
        if not element(By.ID, 'categoryform_flagSetGroup').is_selected():
            cnt += 1
            print 'Флаг "Группировать по данной ВС наборы" не установился'
            print
        if not element(By.ID, 'categoryform_showPromoBlock').is_selected():
            cnt += 1
            print 'Флаг "Показывать товары в промо-блоке" не установился'
            print
        
        if element(By.ID, 'categoryform_externalLink').get_attribute('value') != 'AutotestVSLink':
            cnt += 1
            print 'Текст поля "Ссылка для перехода" не изменился - ', element(By.ID, 'categoryform_externalLink').get_attribute('value')
            print

        #Служебные настройки
        element(By.LINK_TEXT, u'Служебные настройки').click()
        #if self.driver.find_element_by_id('categoryform_oldId').get_attribute('value') != 'AutotestVSoldId':
        #    cnt += 1
        #    print 'Текст categoryform_oldId не изменился - ', self.driver.find_element_by_id('categoryform_oldId').get_attribute('value')
        #    print
        #if self.driver.find_element_by_id('categoryform_oldAlias').get_attribute('value') != 'AutotestVSoldAlias':
        #    cnt += 1
        #    print 'Текст categoryform_oldAlias не изменился - ', self.driver.find_element_by_id('categoryform_oldAlias').get_attribute('value')
        #    print

        #SEO - настройки
        element(By.LINK_TEXT, u'SEO - настройки').click()
        if element(By.ID, 'categoryform_metaTitle').get_attribute('value') != 'AutotestVSmetaTitle':
            cnt += 1
            print 'Текст поля "Мета-тег. Title" не изменился - ', element(By.ID, 'categoryform_metaTitle').get_attribute('value')
            print
        if element(By.ID, 'categoryform_metaKeywords').get_attribute('value') != 'AutotestVSmetaKeywords':
            cnt += 1
            print 'Текст поля "Мета-тег. Keywords" не изменился - ', element(By.ID, 'categoryform_metaKeywords').get_attribute('value')
            print
        if element(By.ID, 'categoryform_metaDescription').get_attribute('value') != 'AutotestVSmetaDescription':
            cnt += 1
            print 'Текст поля "Мета-тег. Description" не изменился - ', element(By.ID, 'categoryform_metaDescription').get_attribute('value')
            print
        if element(By.ID, 'categoryform_metaH1').get_attribute('value') != 'AutotestVSmetaH1':
            cnt += 1
            print 'Текст поля "H1" не изменился - ', element(By.ID, 'categoryform_metaH1').get_attribute('value')
            print
        if element(By.ID, 'categoryform_singularName').get_attribute('value') != 'AutotestVSsingularName':
            cnt += 1
            print 'Текст поля "Название ВС в единственном числе" не изменился - ', element(By.ID, 'categoryform_singularName').get_attribute('value')
            print
        if element(By.ID, 'categoryform_translitName').get_attribute('value') != 'AutotestVStranslitName':
            cnt += 1
            print 'Текст поля "Название ВС в транслите (для брендов - в русскоязычном формате)" не изменился - ', element(By.ID, 'categoryform_translitName').get_attribute('value')
            print

        

        """ Удаление ВС """
        element(By.LINK_TEXT, 'AutotestVSName').click()
        element(By.CLASS_NAME, 'delete').click()
        driver.switch_to_alert().accept()
        time.sleep(10)
        li = element(By.CLASS_NAME, 'dynatree-container').find_elements_by_tag_name('li')
        vs_names = [x.find_element_by_tag_name('a').text for x in li]

        if 'AutotestVSName' in vs_names:
            cnt += 1
            print u'Ошибка при удалении ВС'
            self.driver.get_screenshot_as_file('vsRemoveError.png')
            print u'Скриншот:\n' + self.ARTSOURCE + 'vsRemoveError.png'
            print

        assert cnt == 0, (u'Errors: %d' % cnt)
