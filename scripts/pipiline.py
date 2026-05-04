# ============================================================
# MiseEnPlace | pipeline.py
# Purpose: Automate the full ETL process from raw to processed
# Author: [seu nome]
# Usage: python scripts/pipeline.py
# ============================================================
import pandas as pd
import os
os.system('cls')

# Paths

RAW_PATH = '../data/raw/michelin_my_maps.csv'
PROCESSED_PATH= '../data/processed/'

print("MiseEnPlace Pipeline — Starting...")