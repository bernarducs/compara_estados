import time
from itertools import product

import pandas as pd
import requests

from .utils import UF, gera_url, salva_dataset


def extrai_relatorio(relatorios, no_anexos, anos, periodos, cods_uf):
    
    if cods_uf is None:
        cods_uf = UF

    for relatorio, no_anexo, ano, periodo, cod_uf in product(
        relatorios, no_anexos, anos, periodos, cods_uf
    ):
        print(
            f'Extraindo {relatorio} anexo {no_anexo} de {UF[cod_uf]}, ano de {ano}...'
        )
        url = gera_url(relatorio, no_anexo, ano, periodo, cod_uf)

        try:
            base = busca_dados(url)
        except RuntimeError:
            print(
                f'Timeout: Não foi possível recuperar os dados para {UF[cod_uf]}.'
            )
            continue

        if base['items']:
            df = pd.DataFrame(base['items'])
            nome_df = f'{relatorio}{no_anexo}_{cod_uf}_{ano}{periodo}.csv'
            salva_dataset(relatorio, df, nome_df)

        time.sleep(2)


def busca_dados(url, tentativas=3):
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
