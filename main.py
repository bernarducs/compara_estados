from src.extracao import extrai_relatorio
from src.utils import ufs_faltantes


# rreo, ultimo do ano, anexos 1 e 3
# extrai_relatorio(['rreo'], [3], [2020, 2021], [6])

# rgf, ultimos 5 anos, anexos 6
# extrai_relatorio(['rgf'], [6], [2023], [3])

for ano in [2018, 2019]:
    relatorio = 'rgf'
    anexo = 6
    cods_ufs = ufs_faltantes(f'./datasets/{relatorio}', relatorio, anexo, str(ano))
    extrai_relatorio([relatorio], [anexo], [ano], [3], cods_ufs)
