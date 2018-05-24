# To usando um teclado sem acento, entao as coisas vao ficar assim mesmo
#from IPython.display import display, HTML

import numpy as np
import re
import os

from matplotlib import pyplot as plt

import codecs
from collections import defaultdict


import pandas as pd
import seaborn as sns
#encoding: utf-8

nomeArquivo = input("Digite o nome do arquivo a ser analisado: ")

df1 = pd.read_csv(nomeArquivo)  # dataframe 1, lendo a tabela principal da avaliacao interna

dicte = df1.to_dict('dict')
dict2 = dict()

#print(dict2)
#input("k")

r1 = re.compile("(.*?)\s*\[")
for key in dicte:
    if '[' in key:  # Porque tem umas colunas sem sentido na tabela que eu nao quero pegar

        nomePetauro = (re.search(r"(?<=\[).+?(?=\])", key)).group()  # Nome do petauro entre os colchetes
        if not os.path.exists(nomePetauro): #cria um diretório com o nome do petiano se já não existir
            os.makedirs(nomePetauro)
        categoria = r1.match(key)  # Categoria (o que vem antes dos colchetes, ex: Assiduidade na sala, proatividade...)
#        print(categoria)
#        input("K")
        categoria = categoria.group(1)

        """
        tamCat = 0
        trocaEspaco = 0
        for i in range(len(categoria)):
            tamCat+=1
            if tamCat >= 10:
                trocaEspaco = 1
            if categoria[i] == ' ' and trocaEspaco == 1:
                temp = list(categoria)
                temp[i] = '\n'
                print(temp)
                categoria = ''.join(temp)
                trocaEspaco = 0
                tamCat = 0
        """

#        print(categoria)
#        input("k")
        if not (nomePetauro in dict2):  # Se a key  dict2[nome] nao existe, eh criada
            dict2[nomePetauro] = {}
        if not (categoria in dict2[nomePetauro]):  # se a key dict2[nome][categoria] nao existe, eh criada
            dict2[nomePetauro][categoria] = {}

        for x in dicte[key]:
            if isinstance(dicte[key][x], str):
                if dicte[key][x] in dict2[nomePetauro][categoria]:     # Se a ja existe a key daquele voto, adiciona mais 1
                    dict2[nomePetauro][categoria][dicte[key][x]] += 1  # dicte[key][x] pode ser "Bem organizado", por exemplo,
                    # entao ficaria dict2[nome][categoria]['Bem organizado'] += 1
                else:
                    dict2[nomePetauro][categoria][dicte[key][x]] = 1  # Se a key nao existe, ela eh criada e inicializada


        #transforma em série
        serieData = pd.Series(dict2[nomePetauro][categoria], name='Total')
        serieData.index.name = ' '

        '''
               Voto         Total
        0   Nunca Vejo        2
        1   Vejo Pouco        5
        2   ...................
        3   ...................
        4   ...................

        '''

        # carrega a série com os índices corretos para o data frame
        dictDf = pd.DataFrame(serieData.reset_index())


        # printa situação
        print('Salvando: ' + nomePetauro + ' - ' + categoria)

        ax = plt.subplots()

        grafico = sns.barplot(x=" ", y="Total", hue=' ',  data=dictDf) # plota o gráfico

        nBar = len(ax)
        for patch in grafico.patches:
            cw = patch.get_width()
            print(cw)

            diff = cw - nBar*.1

            patch.set_width(nBar*.1)
            print(nBar*.1)
            patch.set_x(patch.get_x() + diff * .5)

        grafico.set_title(categoria) # adiciona título ao gráfico
        plt.tight_layout()

        imagem = grafico.get_figure()
        imagem.set_size_inches(15, 8) # tamanho da janela para não amontoar as letras de cada voto



        imagem.savefig(nomePetauro + '/' + categoria + '.png') # salva no diretório apropriado



# print(dict2['Bernardo']['Assiduidade na sala']['Vejo pouco'])
# Formato exemplo do dict2


# Sinceramente, eu nao acredito que isso aqui seja o ideal, mas vamo dalhe
for nome in dict2:  # Itera por todos os nomes no dicionario
    f = codecs.open(nome + "/" + "relatorio" + nome + ".csv", "w", "utf-8")  # codecs.open para poder botar o atributo de utf-8, abre/cria o arquivo
    for cat in dict2[nome]:  # Itera pela categoria
        f.write(cat + ',Votos,')  # Cria o "header" Organizacao | Votos ::::::: Nao esquecer de separar com virgulas
        for votos in dict2[nome][cat]:  # Votos eh "Bem organizado" ou qualquer coisa do tipo
            f.write('\n')  # Eh realmente uma quebra de linha na tabela
            f.write(votos + ',' + str(dict2[nome][cat][votos]) + ',')  # Formato disso: Bem organizado | 12
        f.write('\n,\n')  # Quebra a linha duas vezes por clareza

f.close()

print('Concluido')
