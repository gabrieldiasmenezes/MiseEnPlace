# ============================================================
# MiseEnPlace | pipeline.py
# Purpose: Automate the full ETL process from raw to processed
# Author: [seu nome]
# Usage: python scripts/pipeline.py
# ============================================================
from utils import *
import os
os.system('cls')

# Paths 
RAW_PATH = '../data/raw/michelin_my_maps.csv'
CLEANED_PATH = '../data/processed/michelin_cleaned.csv'
FACILITIES_PATH = '../data/processed/michelin_facilities_exploded.csv'
FINAL_PATH = '../data/final/'

IRRELEVANT_COLUMNS = [
    'Address', 'Cuisine', 'Url', 'WebsiteUrl',
    'GreenStar', 'Description', 'PhoneNumber'
]

def run_pipeline():
    print("MiseEnPlace Pipeline — Starting...\n")
    df = load_data(RAW_PATH)
    df = drop_irrelevant_columns(df, IRRELEVANT_COLUMNS)
    df = fix_locations(df)
    df = extract_city_country(df)
    df = normalize_price(df)
    df, df_facilities = explode_facilities(df)  # dois valores de retorno
    df = reorder_columns(df)
    export_data(df, df_facilities, CLEANED_PATH, FACILITIES_PATH)
    export_final(df, df_facilities, FINAL_PATH)
    print("\nPipeline completed successfully.")

if __name__ == "__main__":
    run_pipeline()
