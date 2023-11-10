import json
import psycopg2

# Carregue o JSON
with open("./NOME_DO_ARQUIVO.json", encoding='utf8') as meu_json:
    dados = meu_json.read()
    data = json.loads(dados)

# Configurar a conexão com o banco de dados
conn = psycopg2.connect(
    dbname='postgres',
    user='******',
    password='*****',
    host='000.00.0.000',
    port='5432'
)

# Criar um cursor
cur = conn.cursor()

# Truncar a tabela script_python para remover todos os registros existentes
# cur.execute("TRUNCATE TABLE script_python RESTART IDENTITY")

# Função para extrair valores geojson
def extract_geojson(tipo):
    for geo in data['geo']:
        if geo['tipo'] == tipo:
            return json.dumps(geo['geoJson'])  # Converta para uma string JSON válida
        
codigo_protocolo = data['origem']['codigoProtocolo'].replace('.', '')

# Extrair os valores desejados
valor_json = [
# ('nome_no_banco' , extract_geojson('valor_no_json')
('Territorio_geojson' , extract_geojson('area_territorio')),
('plantacao_geojson' , extract_geojson('area_plantacao')),
('rios_geojson' , extract_geojson('area_rios_proximos')),
]

valor_json_com_codigo = [(nome, valor, codigo_protocolo) for nome, valor in valor_json if valor is not None]

#Inserir os dados na tabela PostgreSQL
insert_query = "INSERT INTO script_python(nome, valor, codigo_car) VALUES (%s, %s, %s)"
cur.executemany(insert_query, valor_json_com_codigo)

# Commit das alterações
conn.commit()

# Fechar cursor e conexão
cur.close()
conn.close()