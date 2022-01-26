import os
import requests
from bs4 import BeautifulSoup
import pandas as pd


cards = []
# url de busca

n = list(range(51))
for posicao in n:
    n[posicao] = 24 * n[posicao]
print(n)
for i in [0, 24, 48, 72, 96, 120, 144, 168, 192, 216, 240, 264, 288, 312, 336, 360, 384, 408, 432, 456, 480, 504, 528, 552, 576, 600, 624, 648, 672, 696, 720, 744, 768, 792, 816, 840, 864, 888, 912, 936, 960, 984, 1008, 1032, 1056, 1080, 1104, 1128, 1152, 1176, 1200]:
    url_site = f'https://www.americanas.com.br/busca/notebook-gamer?limit=24&offset={i}'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36'}
    site = requests.get(url_site, headers=headers)
    soup = BeautifulSoup(site.content, 'html.parser')
    lista_de_produtos = soup.find_all(
        'div', class_='col__StyledCol-sc-1snw5v3-0 epVkvq src__ColGridItem-sc-122lblh-0 bvfSKS')
    print(lista_de_produtos)
    for produto in lista_de_produtos:
        card = {}

        # nome do livro
        nome_produto = produto.select('div h3')
        print('Nome do produto--> ' + produto.find('h3',
                                                   class_='src__Name-sc-1k0ejj6-4 isrBEm').get_text())
        nome_produto = produto.find(
            'h3', class_='src__Name-sc-1k0ejj6-4 isrBEm').get_text()
        print(nome_produto)
        try:
            card['nome'] = nome_produto
            print(card['nome'])
        except IndexError:
            card['nome'] = '0'

        # preco do livro
        try:
            preco_a_vista = produto.find('span',
                                         class_='src__Text-sc-154pg0p-0 src__PromotionalPrice-sc-1k0ejj6-8 gxxqGt').get_text().strip()
            index = preco_a_vista.find(' ')
            card['preco_a_vista'] = preco_a_vista[index:]
            print(card['preco_a_vista'])
        except AttributeError:
            card['preco_a_vista'] = 0

        # capturando o preco parcelaado
        try:
            preco_parcelado = produto.find('span',
                                           class_='src__PaymentDetails-sc-1k0ejj6-5 src__Installment-sc-1k0ejj6-6 dHTHdJ').get_text().strip()
            index2 = preco_parcelado.find('x')
            index3 = preco_parcelado.find('$')
            index4 = preco_parcelado.find('sem')
            card['parcelas'] = preco_parcelado[:index2]
            card['preco_parcelado'] = preco_parcelado[index3:index4]
            print(card['preco_parcelado'])
            print(card['parcelas'])
        except:
            card['parcelas'] = 0
            card['preco_parcelado'] = 0

        # Adicionando resultado a lista cards
        cards.append(card)

# Criando um dataframe com os resultados
dataset = pd.DataFrame(cards)
dataset.to_csv('./notebook_gamer_americanas.csv', sep=';',
               index=False, encoding='utf-8-sig')
dataset
