from bs4 import BeautifulSoup
import pandas as pd
import selenium  # automatiza a busca no site
from selenium import webdriver
# para criar scripts de testes automatizados
from selenium.common.exceptions import NoSuchElementException
# módulo options para  definir recursos para o Navegador
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import json

cards = []
# url de busca
for i in range(60):
    url = f'https://www.amazon.com.br/s?k=fic%C3%A7%C3%A3o&i=stripbooks&s=most_sell&page={i}&__mk_pt_BR=%C3%85M%C3%85%C5%BD%C3%95%C3%91&crid=1X91OL2CGG1W6&qid=1634255662&sprefix=fic%2Cstripbooks%2C249&ref=sr_pg_{i}'

    # chamar o navegador
    option = Options()
    option.headless = False
    # controlando o navegador --implementando com a solução ChromeDriverManager().install()
    navegador = webdriver.Chrome(ChromeDriverManager().install())
    navegador.get(url)

    # pegando o grid de produtos da busca --usar full x path
    div_grid = navegador.find_element_by_xpath(
        "/html/body/div[1]/div[2]/div[1]")
    print(div_grid)
    # navegador.quit()
    html_content = div_grid.get_attribute('outerHTML')
    soup = BeautifulSoup(html_content, 'html.parser')
    # print(soup.prettify())
    # src__Wrapper-sc-1k0ejj6-3 eflURh
    lista_de_produtos = soup.find_all(
        'div', class_='s-result-item s-asin sg-col-0-of-12 sg-col-16-of-20 sg-col s-widget-spacing-small sg-col-12-of-16')
    htmlcontent = div_grid.get_attribute('outerHTML')
    soup = BeautifulSoup(htmlcontent, 'html.parser')
    lista_de_produtos = soup.find_all(
        'div', class_='s-result-item s-asin sg-col-0-of-12 sg-col-16-of-20 sg-col s-widget-spacing-small sg-col-12-of-16')
    for produto in lista_de_produtos:
        card = {}

        # nome do livro
        nome_produto = produto.select('div span')
        print('Nome do produto--> ' + produto.find('span',
                                                   class_='a-size-medium a-color-base a-text-normal').get_text())
        nome_produto = produto.find(
            'span', class_='a-size-medium a-color-base a-text-normal').get_text()

        try:
            card['Livro'] = nome_produto
        except IndexError:
            card['Livro'] = '0'

        # preco do livro
        try:
            preco_anterior = produto.find(
                'span', class_='a-price a-text-price').get_text()
            preco_anterior = preco_anterior[1:]
            index = preco_anterior.find('R$')
            card['preco_anterior'] = preco_anterior[index:]
            print(card['preco_anterior'])
        except AttributeError:
            card['preco_anterior'] = 0

        # capturando o preco parcelaado
        try:
            preco_atual = produto.find('span', class_='a-price').get_text()
            preco_atual = preco_atual[1:]
            index2 = preco_atual.find('R$')
            card['preco_atual'] = preco_atual[index2:]
            print(card['preco_atual'])
        except:
            card['preco_atual'] = 0
        # Adicionando resultado a lista cards
        cards.append(card)

# Criando um dataframe com os resultados
dataset = pd.DataFrame(cards)
dataset.to_csv('./livros_amazon.csv', sep=';',
               index=False, encoding='utf-8-sig')
dataset
