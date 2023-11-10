import os
import geopandas as gpd
from sqlalchemy import create_engine

HOST = '***.**.*.***'
USER = '******'
PASSWORD = '*****'
DATABASE = '******'
PORT = '****'
FILE_NAME = 'NomedoArquivo'

# Conexão com o banco de dados PostgreSQL
engine = create_engine(f'postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}')

# Consulta SQL para selecionar os dados da tabela
sql_query = "SELECT * FROM public.script_python WHERE codigo_arquivo_name = %s"

# Substitua 'nome_da_coluna_geom' pela coluna de geometria correta da sua tabela
geom_col = 'valor'

# Lê os dados do banco de dados e cria um GeoDataFrame
gdf = gpd.read_postgis(sql_query, con=engine, params=(FILE_NAME,), geom_col=geom_col)

# Especifique o caminho da pasta onde você deseja salvar o arquivo Shapefile
pasta_saida = f'C:\\Users\\marcus.mello\\Desktop\\save_shape\\{FILE_NAME}'

# Verifica se a pasta de saída existe, caso contrário, cria-a
if not os.path.exists(pasta_saida):
    os.makedirs(pasta_saida)

# Separa os dados em camadas de MultiPolygon e Point
gdf_multipolygon = gdf[gdf['valor'].geom_type == 'MultiPolygon']
gdf_point = gdf[gdf['valor'].geom_type == 'Point']

# Define o caminho completo dos arquivos Shapefile
caminho_saida_multipolygon = os.path.join(pasta_saida, f'{FILE_NAME}_multipolygon.shp')
caminho_saida_point = os.path.join(pasta_saida, f'{FILE_NAME}_point.shp')

# Exporta os dados para Shapefiles separados
gdf_multipolygon.to_file(caminho_saida_multipolygon)
gdf_point.to_file(caminho_saida_point)

# Feche a conexão com o banco de dados
engine.dispose()