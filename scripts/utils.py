# ============================================================
# MiseEnPlace | utils.py
# Purpose: Reusable transformation functions for the ETL pipeline
# Author: [seu nome]
# ============================================================

import pandas as pd


def verify_null(value) -> bool:
    """Check if a value is null."""
    return pd.isna(value)


def load_data(path: str) -> pd.DataFrame:
    """Load raw dataset from CSV file."""
    df = pd.read_csv(path)
    print(f"Data loaded: {df.shape[0]} rows x {df.shape[1]} columns")
    return df


def drop_irrelevant_columns(df: pd.DataFrame, irrelevant_columns: list) -> pd.DataFrame:
    """Drop columns with no analytical value."""
    df = df.drop(columns=irrelevant_columns)
    print(f"Dropped {len(irrelevant_columns)} columns. Remaining: {df.shape[1]}")
    return df


def fix_locations(df: pd.DataFrame) -> pd.DataFrame:
    """Fix city-state entries missing country in Location column."""
    city_state_mapping = {
        'Singapore': 'Singapore, Singapore',
        'Macau': 'Macau, China',
        'Luxembourg': 'Luxembourg, Luxembourg',
        'Abu Dhabi': 'Abu Dhabi, United Arab Emirates',
        'Dubai': 'Dubai, United Arab Emirates'
    }

    def apply_fix(location):
        if verify_null(location):
            return None
        if ',' not in location:
            return city_state_mapping.get(location.strip(), location)
        return location

    df['Location'] = df['Location'].apply(apply_fix)
    print("Location entries fixed.")
    return df


def extract_city_country(df: pd.DataFrame) -> pd.DataFrame:
    """Split Location column into City and Country."""
    def extract_location_part(location, part):
        if verify_null(location):
            return None
        return location.split(',')[part].strip()

    df['City'] = df['Location'].apply(lambda x: extract_location_part(x, 0))
    df['Country'] = df['Location'].apply(lambda x: extract_location_part(x, -1))
    df = df.drop(columns=['Location'])
    print("City and Country extracted.")
    return df


def normalize_price(df: pd.DataFrame) -> pd.DataFrame:
    """Normalize currency symbols to unified price scale (1-4)."""
    def get_price_category(price):
        if verify_null(price):
            return None
        return min(len(price.strip()), 4)

    df['PriceLevel'] = df['Price'].apply(get_price_category)
    df = df.drop(columns=['Price'])
    print("Price normalized to PriceLevel scale (1-4).")
    return df


def explode_facilities(df: pd.DataFrame) -> tuple:
    """Create exploded facilities dataset for frequency analysis."""
    df_facilities = df[['Name', 'Award', 'FacilitiesAndServices']].copy()
    df_facilities = df_facilities.dropna(subset=['FacilitiesAndServices'])
    df_facilities['FacilitiesAndServices'] = df_facilities['FacilitiesAndServices'].str.split(',')
    df_facilities = df_facilities.explode('FacilitiesAndServices')
    df_facilities['FacilitiesAndServices'] = df_facilities['FacilitiesAndServices'].str.strip()
    print(f"Facilities exploded: {df_facilities.shape[0]} rows.")
    return df, df_facilities


def reorder_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Reorder columns for final dataset structure."""
    column_order = [
        'Name', 'City', 'Country', 'Longitude',
        'Latitude', 'PriceLevel', 'Award', 'FacilitiesAndServices'
    ]
    df = df[column_order]
    print(f"Columns reordered: {df.columns.tolist()}")
    return df


def export_data(df: pd.DataFrame, df_facilities: pd.DataFrame,
                path_df: str, path_facilities: str) -> None:
    """Export cleaned datasets to processed folder."""
    df.to_csv(path_df, index=False)
    df_facilities.to_csv(path_facilities, index=False)
    print(f"Files exported successfully:")
    print(f"  - {path_df}")
    print(f"  - {path_facilities}")

def export_final(df: pd.DataFrame, df_facilities: pd.DataFrame,
                 path_final: str) -> None:
    """Export consolidated dataset for dashboard consumption."""
    df.to_csv(f"{path_final}michelin_dashboard.csv", index=False)
    df_facilities.to_csv(f"{path_final}michelin_facilities_dashboard.csv", index=False)
    print(f"Dashboard files exported to {path_final}")