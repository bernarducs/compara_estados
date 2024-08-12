## Extração Compara Estados

Script que extrai dados da [API](https://apidatalake.tesouro.gov.br/docs/siconfi) do STN, retornando arquivos CSVs para o BI "Compara Estados" do Governo de Pernambuco.

### Preparando o ambiente

```bash
# após clonar o repositório...
$ cd compara_estados
$ python -m venv .ve
$ source .ve/bin/activate
(.ve) $ pip install -r requirements.txt
```

### Como usar

Digamos que queremos extrair dados do anexo 3 do RREO, ano de 2023, segundo bimestre:

```bash
(.ve) $ python comandos.py extrai_relatorio --relatorios=['rreo'] --no_anexos=[3] --anos=[2023] --periodos=[2]
```

Todas as UFs serão extraídas. Caso precise apenas de alguns estados:

```bash
(.ve) $ python comandos.py extrai_relatorio --relatorios=['rreo'] --no_anexos=[3] --anos=[2023] --periodos=[2]  --cods_uf=[26,27]
``` 

Lembre-se, não use espaços nas listas, bash interpretará o comando de forma errada:

```bash
(.ve) $ python comandos.py extrai_relatorio --relatorios=['rreo'] --no_anexos=[1, 3] --anos=[2022, 2023, 2024] --periodos=[2]  --cods_uf=[26, 27] # ERRADO
``` 

### Falta
- testes
