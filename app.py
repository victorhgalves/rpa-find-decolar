import sys
sys.path.append('venv/Lib/site-packages')

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, UnexpectedAlertPresentException,TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from flask import Flask,request
from time import sleep
import config as cfg
import pandas as pd
import re
import requests
import json


app = Flask(__name__)

def runBrowser(url): 
    chrome_options = webdriver.ChromeOptions()
    prefs = {"profile.default_content_setting_values.notifications" : 2}
    chrome_options.add_experimental_option("prefs",prefs)
    browser = webdriver.Chrome(executable_path='chromedriver.exe',chrome_options=chrome_options)
    browser.maximize_window()
    browser.get(url)
    return browser

def executaBusca(browser):
    try:
        _cluster = getCluster(browser)
        _info = getInformacoes(_cluster)
        _dicionarios = formataInformacoes(_info)
        return _dicionarios
    except NoSuchElementException:
        pass
    except Exception as ex:
        return False

def formataInformacoes(info):
    try:
        lista_informacoes  = []
        for x in info:
            informacoes = {}
            informacoes['Companhia'] = x.find_element_by_class_name('name').text
            informacoes['ValorTotal'] = x.find_element_by_class_name('price-wrapper').text
            informacoes['HoraPartidaIda'] = x.find_element_by_class_name('sub-cluster').text.split('\n')[8]
            informacoes['QuantidadeParadasIda'] = x.find_element_by_class_name('sub-cluster').text.split('\n')[9]
            informacoes['HoraChegadaIda'] = x.find_element_by_class_name('sub-cluster').text.split('\n')[10]
            informacoes['HoraPartidaVolta'] = x.find_element_by_class_name('sub-cluster.last').text.split('\n')[8]
            informacoes['QuantidadeParadasVolta'] = x.find_element_by_class_name('sub-cluster.last').text.split('\n')[9]
            informacoes['HoraChegadaVolta'] = x.find_element_by_class_name('sub-cluster.last').text.split('\n')[10]
            lista_informacoes.append(informacoes)
        return lista_informacoes
    except Exception as ex:
        pass


def getInformacoes(cluster):
    try:
        _valores = []
        for i in cluster:
            _valores.append(i)
        return _valores
    except NoSuchElementException:
        pass
    except Exception as ex:
        return False


def getCluster(browser):
    try:
        sleep(5)
        scroll = 0
        for x in range(0,100):
            scroll += 10
            browser.execute_script('window.scrollTo(0, {});'.format(scroll))
        clusters = WebDriverWait(browser, 2).until(EC.visibility_of_all_elements_located((By.CLASS_NAME, 'cluster-container.COMMON')))
        return clusters
    except NoSuchElementException:
        pass
    except Exception as ex:
        return False

@app.route('/api/buscar', methods=['POST', 'GET'])
def executeProcess():
    try:
        content = request.get_json()
        origem = content['origem']
        destino = content['destino']
        data_ida = content['data_ida']
        data_volta = content['data_volta']
        url = 'https://www.decolar.com/shop/flights/search/roundtrip/{}/{}/{}/{}/1/0/0/NA/NA/NA/NA/NA/?from=SB&di=1-0'.format(origem,destino,data_ida,data_volta)
        browser = runBrowser(url)
        dados = executaBusca(browser)
        browser.close()
        return json.dumps({'Sucesso':True,'Retorno':dados})
    except Exception as ex:
        pass
    
      


if __name__ == '__main__':
    app.run(host='AXH19030', debug=True,
	threaded=True, use_reloader=False)
    