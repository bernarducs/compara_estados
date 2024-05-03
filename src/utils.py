import os

UF = {
    '15': 'Pará',
    '50': 'Mato Grosso do Sul',
    '11': 'Rondônia',
    '31': 'Minas Gerais',
    '17': 'Tocantins',
    '14': 'Roraima',
    '41': 'Paraná',
    '35': 'São Paulo',
    '16': 'Amapá',
    '12': 'Acre',
    '21': 'Maranhão',
    '13': 'Amazonas',
    '53': 'Distrito Federal',
    '33': 'Rio de Janeiro',
    '27': 'Alagoas',
    '26': 'Pernambuco',
    '29': 'Bahia',
    '51': 'Mato Grosso',
    '24': 'Rio Grande do Norte',
    '43': 'Rio Grande do Sul',
    '28': 'Sergipe',
    '42': 'Santa Catarina',
    '23': 'Ceará',
    '22': 'Piauí',
    '25': 'Paraíba',
    '52': 'Goiás',
    '32': 'Espírito Santo',
}


def gera_url(relatorio, no_anexo, ano, periodo, id_ente):
    prefix = 'http://apidatalake.tesouro.gov.br/ords/siconfi/tt/'
    params = 'an_exercicio={0}&' 'nr_periodo={1}&' 'id_ente={2}'
    try:

        if relatorio == 'rreo':
            query = (
                prefix
                + 'rreo?'
                + params
                + '&co_tipo_demonstrativo=RREO&'
                + 'no_anexo=RREO-Anexo%200{3}'
            )

        if relatorio == 'rgf':
            query = (
                prefix
                + 'rgf?'
                + params
                + '&co_poder=E&in_periodicidade=Q&co_tipo_demonstrativo=RGF&'
                + 'no_anexo=RGF-Anexo%200{3}'
            )

        return query.format(ano, periodo, id_ente, no_anexo)
    except UnboundLocalError:
        print('Param "relatorio", aceita apenas "rreo" ou "rgf".')
        return False


def salva_dataset(relatorio, df, nome_df):

    diretorio = os.path.join(os.getcwd(), 'datasets', relatorio)
    if not os.path.exists(diretorio):
        os.makedirs(diretorio)

    arquivo = os.path.join(diretorio, nome_df)
    df.to_csv(arquivo, sep=';', decimal=',', index=False, encoding='utf-8')
    print(f'{nome_df} salvo em {diretorio}')

def contagem_por_relatorio(diretorio, relatorio, anexo, ano):
    arquivos = os.listdir(diretorio)
    return len(
        [
            arquivo for arquivo in arquivos 
            if arquivo.startswith(f'{relatorio}{anexo}') and ano in arquivo
        ]
    )

def ufs_faltantes(diretorio, relatorio, anexo, ano):
    arquivos = os.listdir(diretorio)
    cods_uf = [
            arquivo.split('_')[1] for arquivo in arquivos 
            if arquivo.startswith(f'{relatorio}{anexo}') and ano in arquivo
        ]
    
    diff = list( set(UF.keys()) - set(cods_uf))
    return diff
