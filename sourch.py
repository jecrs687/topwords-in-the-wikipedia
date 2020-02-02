import requests
#import googletrans
from bs4 import BeautifulSoup
import time
import random
linkNumber = 5
numMinimoRepeticoes = 5

LANGUAGES = {
    'af': 'afrikaans',
    'sq': 'albanian',
    'am': 'amharic',
    'ar': 'arabic',
    'hy': 'armenian',
    'az': 'azerbaijani',
    'eu': 'basque',
    'be': 'belarusian',
    'bn': 'bengali',
    'bs': 'bosnian',
    'bg': 'bulgarian',
    'ca': 'catalan',
    'ceb': 'cebuano',
    'ny': 'chichewa',
    'zh-cn': 'chinese (simplified)',
    'zh-tw': 'chinese (traditional)',
    'co': 'corsican',
    'hr': 'croatian',
    'cs': 'czech',
    'da': 'danish',
    'nl': 'dutch',
    'en': 'english',
    'eo': 'esperanto',
    'et': 'estonian',
    'tl': 'filipino',
    'fi': 'finnish',
    'fr': 'french',
    'fy': 'frisian',
    'gl': 'galician',
    'ka': 'georgian',
    'de': 'german',
    'el': 'greek',
    'gu': 'gujarati',
    'ht': 'haitian creole',
    'ha': 'hausa',
    'haw': 'hawaiian',
    'iw': 'hebrew',
    'hi': 'hindi',
    'hmn': 'hmong',
    'hu': 'hungarian',
    'is': 'icelandic',
    'ig': 'igbo',
    'id': 'indonesian',
    'ga': 'irish',
    'it': 'italian',
    'ja': 'japanese',
    'jw': 'javanese',
    'kn': 'kannada',
    'kk': 'kazakh',
    'km': 'khmer',
    'ko': 'korean',
    'ku': 'kurdish (kurmanji)',
    'ky': 'kyrgyz',
    'lo': 'lao',
    'la': 'latin',
    'lv': 'latvian',
    'lt': 'lithuanian',
    'lb': 'luxembourgish',
    'mk': 'macedonian',
    'mg': 'malagasy',
    'ms': 'malay',
    'ml': 'malayalam',
    'mt': 'maltese',
    'mi': 'maori',
    'mr': 'marathi',
    'mn': 'mongolian',
    'my': 'myanmar (burmese)',
    'ne': 'nepali',
    'no': 'norwegian',
    'ps': 'pashto',
    'fa': 'persian',
    'pl': 'polish',
    'pt': 'portuguese',
    'pa': 'punjabi',
    'ro': 'romanian',
    'ru': 'russian',
    'sm': 'samoan',
    'gd': 'scots gaelic',
    'sr': 'serbian',
    'st': 'sesotho',
    'sn': 'shona',
    'sd': 'sindhi',
    'si': 'sinhala',
    'sk': 'slovak',
    'sl': 'slovenian',
    'so': 'somali',
    'es': 'spanish',
    'su': 'sundanese',
    'sw': 'swahili',
    'sv': 'swedish',
    'tg': 'tajik',
    'ta': 'tamil',
    'te': 'telugu',
    'th': 'thai',
    'tr': 'turkish',
    'uk': 'ukrainian',
    'ur': 'urdu',
    'uz': 'uzbek',
    'vi': 'vietnamese',
    'cy': 'welsh',
    'xh': 'xhosa',
    'yi': 'yiddish',
    'yo': 'yoruba',
    'zu': 'zulu',
    'fil': 'Filipino',
    'he': 'Hebrew'
}

LANGCODES = dict(map(reversed, LANGUAGES.items()))


def obter_conteudo(link,prefixo):
    """get all content in one page of wikipedia"""
    conteudo = ''
    site = requests.get( 'https:'+prefixo+link)
    soup = BeautifulSoup(site.content, 'html.parser')
    for x in range(0, len(soup.find_all('p'))):
        conteudo = conteudo + soup.find_all('p')[x].get_text()
    conteudo.encode(encoding='UTF-8',errors='ignore')
    return conteudo.lower()

def contar_conteudo_e_remover_excesso(conteudo):
    """This function get the words and convert her in one array [[word, weight], ....[word,weight]]"""
    palavras = []
    e=0
    boost =conteudo[0:int(len(conteudo)/50)]
    x=0
    while(x<len(boost)):
        y=x+1
        d=0
        while(y<len(boost)):
            if(boost[x]==boost[y]):
                del(boost[y])
                d=d+1
            y=y+1
        boost[x]=[boost[x],d]
        x=x+1
    boost.sort(key=lambda x: x[1], reverse=True)
    for x in boost:
        conteudo[boost.index(x)]=x[0]
    for x in range(0,len(conteudo)):
        d = 0
        for y in range(x+1, len(conteudo)):
            if(conteudo[x]==conteudo[y-d]):
                del(conteudo[y-d])
                d+=1
        if(len(conteudo)>x):
            if(d>=numMinimoRepeticoes):
                palavras.append((conteudo[x], d+1))
    return palavras

def filtrar_conteudo(conteudo):
    """this function is the filter of words, 
    this function get the words and filter her"""
    conteudo = conteudo.split()
    d=0
    for x in range(0, len(conteudo)):
        if(conteudo[x-d].isalpha()==0):
            del(conteudo[x-d])
            d=d+1
            continue
        if(conteudo[x-d].isalnum()==0):
            del(conteudo[x-d])
            d=d+1
            continue
        if (conteudo[x-d].count('wiki') > 0):
            del (conteudo[x-d])
            d = d + 1
            continue
    tamanho = len(conteudo)
    return conteudo,tamanho

def ordenar_conteudo(conteudo):
    """this function only realize one sort of the words basead in the weight"""
    conteudo.sort(key=lambda x: x[1], reverse=True)
    return conteudo

def obter_paginas(link,prefixo):
    """get the pages of wikipedia"""
    y = len(link)
    if (y == 0):
        y = y + 1
    for z in range(0, y):
        site = requests.get('https:'+prefixo+link[z])
        soup = BeautifulSoup(site.content, 'html.parser')
        pagina = soup.find_all('a', href=True)
        for x in range(0,len(pagina)):
            if(pagina[x]['href'].count('/wiki/')>0):
                if(not(pagina[x]['href'].count('.')>0)):
                     link.append(pagina[x]['href'])
    return link

def remover_links(link, prefixo):
    """remove duplicate links"""
    x=0
    print(len(link))
    boost = link[0:int(len(link)/10)]
    while(x<len(boost)):
        y=x+1
        d=0
        while(y<len(boost)):
            if(boost[x]==boost[y]):
                del(boost[y])
                d=d+1
            y=y+1
        boost[x]=[boost[x],d]
        x=x+1
    boost.sort(key=lambda x: x[1], reverse=True)
    for x in boost:
        link[boost.index(x)]=x[0]
    x=0
    while(x<len(link)):
        y=x+1
        while(y<len(link)):
            if(link[x]==link[y]):
                del(link[y])
                d=d+1
            y=y+1
        x=x+1
    print(len(link))
    # não lembro o q essa parada abaixo faz, talvez tenha sido alguma noia ksks
    # for z in range (0, len(link)):
    #     site = requests.get('https:'+prefixo+link[z])
    #     soup = BeautifulSoup(site.content, 'html.parser')
    #     pagina_excluir = soup.find_all('div', id=True)
    #     paginas_excluir = []
    #     d=0
    #     for x in range (0, len(pagina_excluir)):
    #         pagina_excluir = soup.find_all('div', id=True)
    #         if(pagina_excluir[x]['id']=='mw-panel' or pagina_excluir[x]['id']=='lang' or pagina_excluir[x]['id']=='mp-sister-content'):
    #             pagina_excluir = pagina_excluir[x].find_all('a', href=True)
    #             for y in range(0,len(pagina_excluir)):
    #                 if(not(pagina_excluir[y]['href']==None)):
    #                     if(not(pagina_excluir[y]['href'].count('.')>0)):
    #                         paginas_excluir.append(pagina_excluir[y]['href'])
    #                         d = d+1

    #             if (d==3):
    #                 break
    #     break
    return link

def obter_prefixo(link):
    """get the prefix of links"""
    d=0
    prefixo = []
    site = requests.get(link)
    soup = BeautifulSoup(site.content, 'html.parser')
    pagina = soup.find_all('a', title=True, href=True)
    for x in range(0, len(pagina)):
        for y in range(x+1, len(pagina)):
            if(pagina[x-d]['title']==pagina[y]['title']):
                del(pagina[x-d])
                d = d + 1
        if(x<len(pagina)):
            if(pagina[x-d]['title'].count("—") > 0):
                pagina[x-d]['title'] = pagina[x-d]['title'].replace(pagina[x-d]['title'][pagina[x-d]['title'].find(" "):len(pagina[x-d]['title'])],'')

    for x in pagina:
        prefixo.append((x['title'],x['href']))
    return prefixo

def arquivar(conteudo, lingua1, tamanho):
    """archive the words in a file txt using a structure json"""
    with open(lingua1+'-pt.txt','w+', encoding="utf-8") as arq:
        arq.write('{'+'"tamanho":{},'.format(tamanho)+'"palavras":[')
        arq.write("\n")
        arq.write("\n")
        for z in range(0, len(conteudo)):
            arq.write('{"word":"'+conteudo[z][0]+'",repeted":{}'.format(conteudo[z][1])+',"porcent":{}'.format((conteudo[z][1]/tamanho)*100)+'},')
            arq.write("\n")
        arq.write('],}')
        print('arquivo salvo como {}-pt.txt'.format(lingua1))

def enxutar(conteudo, lingua):
    """decrapeted"""
    tradutor = googletrans.Translator()
    palavras=""
    traduzido = []
    d=0
    lingua=lingua.lower()
    for y in range(0,len(conteudo)):
        time.sleep(random.randint(1,5))
        e=0
        palavras = conteudo[y-d][0]
        print(palavras)
        nativa = tradutor.detect(palavras).lang
        for x in range(0, len(nativa),2):
            print(LANGUAGES[nativa[x:x+2]], nativa[x:x+2], lingua)
            lingua2 = tradutor.translate(LANGUAGES[nativa[x:x+2]], dest=nativa[x:x+2]).text
            lingua2 = lingua2.lower()
            print(LANGUAGES[nativa[x:x+2]], nativa[x:x+2], lingua, lingua2)
            if(lingua==lingua2):
                print(palavras)
                traduzido.append(tradutor.translate(palavras, dest="pt",src=nativa[x:x+2]).text)
                e=1
        if(e==0):
            del(conteudo[y-d])
            d+=1
    return conteudo,traduzido

def processar_conteudo(prefixo):
    """get and process words embased the prefix"""
    print("obtendo paginas")
    link = obter_paginas([''],prefixo[1])
    print("removendo links excessivos ou identicos")
    link = remover_links(link, prefixo[1])
    while(len(link)<linkNumber):
        print("-----existem:{} links".format(len(link)))
        print("obtendo mais paginas")
        link = obter_paginas(link, prefixo[1])
        print("-----existem:{} links".format(len(link)))
        print("removendo links excessivos ou identicos")
        link = remover_links(link, prefixo[1])
        print("-----existem:{} links".format(len(link)))
    print("obtendo condeudo")
    conteudo = obter_conteudo(link[0],prefixo[1])
    for x in range(1, linkNumber):
        print("pegando conteudo: {}/{}".format(x, linkNumber))
        conteudo = conteudo + obter_conteudo(link[x], prefixo[1])
    print("filtrando conteudo")
    conteudo,tamanho = filtrar_conteudo(conteudo)
    print("contando conteudo e removendo excesso")
    conteudo = contar_conteudo_e_remover_excesso(conteudo)
    print("ordenando conteudo")
    conteudo = ordenar_conteudo(conteudo)
    #print("enxutar e traduzindo")
    #conteudo,traduzido = enxutar(conteudo, prefixo[0])
    print("arquivando")
    arquivar(conteudo, prefixo[0], tamanho)
    print("\n\n\n\n")
    return conteudo





prefixo = obter_prefixo('https://www.wikipedia.org/')

for y in range(0, len(prefixo)):
    if (prefixo[y][0].isalpha() == 1 and not(prefixo[y][0]=="Deutsch")and not(prefixo[y][0]=="Nihongo")):
        print(prefixo[y][0])
        processar_conteudo(prefixo[y])




