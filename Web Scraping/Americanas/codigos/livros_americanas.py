import os
import requests
from bs4 import BeautifulSoup

cards = []
# url de busca
for i in range(1):
    url = f'https://www.americanas.com.br/busca/livros-ficcao?rc=livros%20fic%C3%A7%C3%A3o&sortBy=topSelling&limit=24&offset={i}'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36'}
    site = requests.get(url, headers=headers)
    soup = BeautifulSoup(site.content, 'html.parser')
    lista_de_produtos = soup.find_all(
        'div', class_='igrid__StyledGrid-sc-1man2hx-0 iFeuoP')
    for produto in lista_de_produtos:
        card = {}

        # nome do livro
        nome_produto = produto.select('div span')
        print('Nome do produto--> ' + produto.find('h3',
                                                   class_='product-name__Name-sc-1shovj0-0 gUjFDF').get_text())
        nome_produto = produto.find(
            'h3', class_='product-name__Name-sc-1shovj0-0 gUjFDF').get_text().strip()

        try:
            card['Livro'] = nome_produto
        except IndexError:
            card['Livro'] = '0'

        # preco do livro
        try:
            preco_a_vista = produto.find('span',
                                         class_='src__Text-sc-154pg0p-0 price__PromotionalPrice-h6xgft-1 ijXFcq price-info__ListPriceWithMargin-sc-1xm1xzb-2 liXDNM').get_text().strip()
            index = preco_a_vista[10:]
            card['preco_a_vista'] = index
        except AttributeError:
            card['preco_a_vista'] = 0

        # capturando o preco parcelaado
        try:
            preco_parcelado = produto.find('span',
                                           class_='installment__InstallmentUI-sc-1g296bd-0 fNXtFB').get_text().strip()
            index2 = preco_parcelado[3:-7]
            #index3 = index2.find('$')
            card['preco_parcelado'] = index2
        except:
            card['preco_parcelado'] = 0
        # Adicionando resultado a lista cards
        cards.append(card)

# Criando um dataframe com os resultados
dataset = card.DataFrame(cards)
dataset.to_csv('./livros_americanast.csv', sep=';',
               index=False, encoding='utf-8-sig')
dataset
