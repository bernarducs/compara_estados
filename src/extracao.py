import time
from itertools import product

import pandas as pd
import requests

from .utils import UF, gera_url, salva_dataset


def extrai_relatorio(relatorios, no_anexos, anos, periodos, cods_uf=None):
    """Faz chamadas a diversas funções para extração de dados do STN.
       Atualmente apenas para estados.

    Args:
        relatorios (list[str]): Lista de relatórios orçamentários.
        no_anexos (list[int]): Lista com os números dos anexos.
        anos (list[int]): Lista comos números dos anexos.
        periodos (list[int]): Lista com os números dos períodos.
        cods_uf (lis[int]): Lista com os códigos dos estados.
    """
    
    if cods_uf is None:
        cods_uf = UF

    for relatorio, no_anexo, ano, periodo, cod_uf in product(
        relatorios, no_anexos, anos, periodos, cods_uf
    ):
        uf_nome = UF[str(cod_uf)]

        print(
            f'Extraindo {relatorio} anexo {no_anexo} de {uf_nome}, ano de {ano}...'
        )
        url = gera_url(relatorio, no_anexo, ano, periodo, cod_uf)

        try:
            base = busca_dados(url)
        except RuntimeError:
            print(
                f'Timeout: Não foi possível recuperar os dados para {uf_nome}.'
            )
            continue

        if base['items']:
            df = pd.DataFrame(base['items'])
            nome_df = f'{relatorio}{no_anexo}_{cod_uf}_{ano}{periodo}.csv'
            salva_dataset(relatorio, df, nome_df)

        time.sleep(2)


def busca_dados(url, tentativas=3):
    """Executa requisições à API do STN.

    Args:
        url (str): URL para requisição.
        tentativas (int, optional): Total de tentivas para cada URL. Padrão é 3.

    Raises:
        RuntimeError: Caso o total tentativas tenha ultrapassado o limite.

    Returns:
        dict: Objeto JSON com os dados de determinado relatório.
    """

    for tentativa in range(tentativas):
        try:
            r = requests.get(url)
            r.raise_for_status()   # gera HTTPError se status não é 200
            return r.json()
        except requests.exceptions.HTTPError as err:
            print(
                f'Tentativa {tentativa + 1} falhou com status {r.status_code}. \nRepetindo...'
            )
            time.sleep(20)
        except requests.exceptions.RequestException as err:
            print(
                f'Tentativa {tentativa + 1} falhou com erro: {err}. \nRepetindo...'
            )
            time.sleep(20)
    raise RuntimeError('Máximo de tentativas realizadas. Saindo...')
