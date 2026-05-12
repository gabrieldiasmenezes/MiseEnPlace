# MiseEnPlace

## Visão Geral

Projeto de análise de dados e inteligência de mercado para restaurantes do Guia Michelin. O objetivo é transformar dados brutos em indicadores acionáveis, gerar uma base de dados limpa para dashboard e comunicar insights relevantes para investidores.

Os dados foram coletados a partir do arquivo `data/raw/michelin_my_maps.csv` e tratam informações sobre restaurantes, localização, premiações, níveis de preço e serviços disponíveis.

## Objetivo do Projeto

- Realizar diagnóstico de qualidade dos dados brutos.
- Limpar e transformar o dataset para análise.
- Gerar métricas e KPIs focados em desempenho de restaurantes Michelin.
- Produzir datasets consolidados para uso em visualizações e dashboard Power BI.
- Criar um fluxo de ETL reprodutível que possa ser executado como pipeline.

## Estrutura do Repositório

- `data/raw/`
  - `michelin_my_maps.csv` — dados brutos originais.
- `data/processed/`
  - `michelin_cleaned.csv` — dataset limpo para análise.
  - `michelin_facilities_exploded.csv` — base de serviços e facilidades explodida para análise de frequência.
- `data/final/`
  - `michelin_dashboard.csv` — arquivo consolidado para dashboard.
  - `michelin_facilities_dashboard.csv` — arquivo consolidado de facilidades para dashboard.
- `notebooks/`
  - `01_data_collection.ipynb` — diagnóstico inicial de dados e definição de colunas relevantes.
  - `02_cleaning_eda.ipynb` — limpeza de dados, tratamento de localização, normalização de preço e geração de bases processadas.
  - `03_metrics_kpis.ipynb` — análise de KPIs, insights por categoria de premiação e validação de hipóteses.
- `scripts/`
  - `pipiline.py` — pipeline de ETL que executa a limpeza automatizada e gera os arquivos processados.
  - `utils.py` — funções de transformação reutilizáveis para o pipeline.
- `dashboard/`
  - `dashboard.pbix` — arquivo Power BI do dashboard.

## Metodologia e Transformações Realizadas

### 1. Seleção de colunas relevantes
Foram removidas colunas que não agregam valor analítico para a proposta do projeto, tais como:
- `Address`
- `Cuisine`
- `Url`
- `WebsiteUrl`
- `GreenStar`
- `Description`
- `PhoneNumber`

### 2. Tratamento de localização
A coluna `Location` foi ajustada para garantir país e cidade. Em casos onde só havia cidade ou estado, foi aplicada a correção manual em entradas como:
- `Singapore` → `Singapore, Singapore`
- `Macau` → `Macau, China`
- `Luxembourg` → `Luxembourg, Luxembourg`
- `Abu Dhabi` → `Abu Dhabi, United Arab Emirates`
- `Dubai` → `Dubai, United Arab Emirates`

Depois disso, a coluna `Location` foi dividida em duas colunas:
- `City`
- `Country`

### 3. Normalização de preço
A coluna `Price` foi convertida para um novo indicador numérico chamado `PriceLevel`.

A estratégia foi simples e eficaz: contar o número de símbolos de moeda por registro e limitar o valor a um máximo de 4. Assim, diferentes moedas foram transformadas em um mesmo nível de preço entre 1 e 4.

### 4. Tratamento de facilidades
A coluna `FacilitiesAndServices` foi explodida em uma tabela separada para permitir análise de frequência item a item. Isso permite identificar quais serviços mais aparecem em restaurantes 3 estrelas e como eles se distribuem nas demais categorias.

## Insights Identificados

Os notebooks do projeto trazem as principais conclusões obtidas durante a análise:
- 100% dos restaurantes 3 estrelas possuem registro de facilidades e serviços.
- A presença de serviços como `Air conditioning`, `Interesting wine list`, `Wheelchair access` e `Car park` é muito mais comum nas categorias superiores.
- `Interesting wine list` se destaca como um diferencial de infraestrutura entre restaurantes 3 estrelas e outras categorias.
- A relação entre número médio de facilidades e nível de premiação indica que a qualidade das facilidades importa mais do que a quantidade isolada.

## Como Executar o Projeto

### Requisitos
- Python 3.8+ instalado
- Recomenda-se criar um ambiente virtual
- Dependências listadas em `requirements.txt`

### Passos

1. Abra o terminal na raiz do projeto.
2. Crie e ative um ambiente virtual:

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

3. Instale as dependências:

```powershell
pip install -r requirements.txt
```

4. Baixe o dataset do Kaggle no link: https://www.kaggle.com/datasets/ngshiheng/michelin-guide-restaurants-2021 e coloque o arquivo CSV na pasta `data/raw/`.

5. Execute o pipeline de ETL para gerar os arquivos processados:

```powershell
cd scripts
python pipiline.py
```

> Observação: o script `scripts/pipiline.py` utiliza caminhos relativos a partir da pasta `scripts`. Por isso, recomendamos executá-lo dentro desse diretório. O script funcionará automaticamente após o download do dataset.

6. Os arquivos gerados ficarão em:
- `data/processed/michelin_cleaned.csv`
- `data/processed/michelin_facilities_exploded.csv`
- `data/final/michelin_dashboard.csv`
- `data/final/michelin_facilities_dashboard.csv`

7. Para visualizar o dashboard, abra o arquivo `dashboard/dashboard.pbix` no seu próprio Power BI (isso deve ser feito manualmente pelo usuário).

### Reproduzindo os notebooks

Para análise passo a passo e validação dos resultados, abra os notebooks em `notebooks/` na ordem:
1. `01_data_collection.ipynb`
2. `02_cleaning_eda.ipynb`
3. `03_metrics_kpis.ipynb`

Eles contêm explicações das decisões, validações e gráficos que suportam os insights.

## Dashboard Power BI

O arquivo Power BI está disponível em `dashboard/dashboard.pbix` e contém três páginas principais criadas para suporte à decisão de investimentos.

### Páginas do dashboard

- `Executive Summary`
  - Visão geral dos resultados do projeto.
  - Mostra o total de restaurantes analisados, número de restaurantes 3 estrelas e países cobertos.
  - Inclui distribuição de prêmios Michelin por categoria (`Selected Restaurants`, `Bib Gourmand`, `1 Star`, `2 Stars`, `3 Stars`).

- `Investment Blueprint`
  - Analisa os principais elementos que definem um restaurante 3 estrelas.
  - Exibe a penetração das facilidades mais relevantes entre restaurantes 3 estrelas, com destaque para `Air conditioning`, `Interesting wine list`, `Wheelchair access`, `Car park` e `Valet parking`.
  - Apresenta a distribuição do `PriceLevel` por categoria de prêmios, mostrando que a maior parte dos restaurantes 3 estrelas opera no nível de preço 4.

- `Target Markers`
  - Foco geográfico para identificar os mercados com maior concentração de excelência.
  - Inclui um mapa mundial de restaurantes Michelin exibindo clusters de destaque.
  - Mostra países com maiores contagens de restaurantes 3 estrelas, com liderança de Coreia do Sul, Japão, Espanha, Itália e Reino Unido.
  - Traz uma tabela de cidades-chave como `Tokyo`, `Paris`, `Hong Kong`, `London`, `Kyoto` e `New York`.

### Valor do dashboard

O relatório Power BI foi desenhado para apoiar decisões de investimento em gastronomia ao combinar três perspectivas:
- visão macro do universo analisado;
- blueprint de diferenciais operacionais e de infraestrutura exigidos por restaurantes de elite;
- direção geográfica para encontrar mercados e cidades com maior potencial.

> Nota: o conteúdo das páginas foi descrito a partir das imagens fornecidas. Se houver mais detalhes ou textos específicos do dashboard que você deseja incluir, posso adaptar o README com base nas informações adicionais.

## Observações Técnicas

- O pipeline foi projetado para ser reprodutível e modular.
- A limpeza preserva a consistência dos dados e gera artefatos específicos para análise de serviços e de localização.
- O projeto segue uma arquitetura simples: dados brutos → transformação → exports para visualização.

## Contribuições

Se quiser estender o projeto, algumas melhorias possíveis são:
- adicionar validação de integridade dos dados (`schema validation`);
- automatizar a execução pela raiz do projeto usando caminhos relativos fixos;
- criar dashboard interativo adicional em Power BI ou outra ferramenta de BI;
- incluir análise de `Cuisine` depois de normalizar e categorizar os tipos culinários.

## Autor
- Projeto desenvolvido como parte do fluxo `MiseEnPlace`.
- Para complementos e ajustes, posso ajudar a documentar casos de uso específicos ou melhorar o dashboard Power BI.
