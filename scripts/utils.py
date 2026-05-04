import pandas as pd

def verify_null(content):
    return pd.isna(content)
    
def load_data(path):
    return pd.read_csv(path)

def drop_irrelevant_columns(df:pd.DataFrame,irrelevant_columns:list)-> pd.DataFrame:
    return df.drop(columns=irrelevant_columns)

def fix_locations(df: pd.DataFrame)-> pd.DataFrame:
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
    df['Location']=df['Location'].apply(apply_fix)
    return df


def extract_city_country(df: pd.DataFrame)-> pd.DataFrame:
    def extract_location_part(location,part):
        if pd.isna(location):
            return None
        return location.split(',')[part].strip()
    
    df['City']=df['Location'].apply(lambda x: extract_location_part(x,0))
    df['Country']=df['Location'].apply(lambda x: extract_location_part(x,-1))

    df=df.drop(columns=['Location'])

    return df


def normalize_price(df: pd.DataFrame)-> pd.DataFrame:
    def get_price_category(price):
        if pd.isna(price):
            return None
        return min(len(price.strip()),4)
    df['PriceLevel']=df['Price'].apply(get_price_category)
    df=df.drop(columns=['Price'])
    return df

def explode_facilities(df: pd.DataFrame)-> tuple:
    df_facilities = df[['Name', 'Award', 'FacilitiesAndServices']].copy()
    df_facilities = df_facilities.dropna(subset=['FacilitiesAndServices'])
    df_facilities['FacilitiesAndServices'] = df_facilities['FacilitiesAndServices'].str.split(',')
    df_facilities = df_facilities.explode('FacilitiesAndServices')
    df_facilities['FacilitiesAndServices'] = df_facilities['FacilitiesAndServices'].str.strip()

    return df,df_facilities


