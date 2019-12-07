import requests
import json
import pandas #import pandas para poder trabalhar com esta biblioteca

def converter_data(dia): #Toda função vai ser atribuida pelo DEF
    dia = dia[8:]+"/"+dia[5:7]+"/"+dia[0:4] 
    print("Ultima atualização dos dados:", dia)
    return dia

# verificando se o usuário possui uma chave de acesso para #acesso pessoal
def chave_acesso(chave="a88e5172c7cc3ff6d8322073432c233d"): 
    return "http://data.fixer.io/api/latest?access_key="+chave

#  convertendo as taxas em reais
def converter_em_reais(valor_real, valor_estrangeiro):
    return round(valor_real/valor_estrangeiro,2)

def exportar_tabela(lista_titulos, lista_valores, nome_arquivo, lista_dia):
    celulas = pandas.DataFrame({'Moedas':lista_titulos, 'Valores':lista_valores, 'Acessado em':lista_dia}) #importando os dados da API para um dataframe
    #A chave do dicionario é o titulo da coluna e o valor da lista sera o conteudo da coluna
    celulas.to_csv(nome_arquivo+".csv",index=False, sep=";") #exportando o resultado e formatando para sair como celulas separas
    print("Tabela exportada com sucesso!")

def main(): # main será a função princial
    '''
    Utilizamos a função get do requests para acessar as informações da API onde se encontra as informações das moedas.
    Ao acessar o servidor, a variável status_cod do requests, é preenchida com a respota HTTP do servidor e variavel content também do requests, é preenchida com o conteúdo da API (JSON)
    '''
    chave = input("Informe a sua chave de acesso do Fixer.io, se não houver, pressione ENTER: ")
    url = chave_acesso(chave) if len(chave) > 0 else chave_acesso()
    print("Acessando base de dados... ")

    resposta = requests.get(url)
    if resposta.status_code == 200:
        print("Conexão com a base de dados estabelecida com sucesso... ")
        dados = resposta.json()
        # A função converter_data irá receber o valor da variáel dados['date'] e irá retornar a data convertida  no padrão #Brasil, será atribuida a variável dia_convertido
        dia_convertido = converter_data(dados['date'])
        # a opção round, arredonda o valor encontrado para até duas casas decimais.
        euro_em_reais = converter_em_reais(dados['rates']['BRL'], dados['rates']['EUR'])   
        bitcoin_em_reais = converter_em_reais(dados['rates']['BRL'], dados['rates']['BTC'])
        dollar_em_reais = converter_em_reais(dados['rates']['BRL'], dados['rates']['USD'])
        escolha = input("Digite:\nB - Bitcoin\nD - Dollar\nE - Euro\nA - Todas\n").upper()
        if (escolha == 'B'):
            exportar_tabela(['Bitcoin'], [bitcoin_em_reais], 'bitcoin',[dia_convertido])
        elif (escolha == 'D'):
            exportar_tabela(['Dollar'], [dollar_em_reais], 'dollar',[dia_convertido])
        elif (escolha == 'E'):
            exportar_tabela(['Euro'], [euro_em_reais], 'euro',[dia_convertido])
        elif (escolha == 'A'):
            exportar_tabela(['Bitcoin', 'Dollar', 'Euro'], [bitcoin_em_reais, dollar_em_reais, euro_em_reais], 'moedas',[dia_convertido,'',''])
        else:
            print("Você não escolheu nenhuma das opções. Sua tabela não será exportada! ")
    else:
        print("Erro ao acessar a base de dados")

if __name__=="__main__":
    main()