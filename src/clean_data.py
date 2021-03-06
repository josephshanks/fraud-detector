import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split


def load_data(filepath):
    """
    Load the data into a pandas dataframe.
    
    Parameters:
        filepath - file path to data file
    
    Returns:
        data - pandas dataframe of data
    """
    
    return pd.read_json(filepath)


def clean_data(d, predict=False):
    """
    Clean the data for use in model training.
    
    Parameters:
        d - dataframe of loaded data
        predict - boolean of whether the data is prediction data or not. default False
        
    Returns:
        data - cleaned dataframe
    """
    
    data = d.copy()
    
    if not predict:
        # create fraud binary classification
        data['fraud'] = data['acct_type'].apply(lambda x: 1 if 'fraud' in x else 0)
    
    # one-hot-encode
    data = pd.get_dummies(data, columns=['currency'], prefix='currency', prefix_sep=': ', dtype='int', drop_first=True)
    data = pd.get_dummies(data, columns=['channels'], prefix='channels', prefix_sep=': ', dtype='int', drop_first=True)
    data = pd.get_dummies(data, columns=['payout_type'], prefix='payout_type', prefix_sep=': ', dtype='int', drop_first=True)
    
    # extract max ticket price for event
    data['max_price'] = (data['ticket_types']
                     .apply(lambda x: max([ticket['cost'] for ticket in x]) if isinstance(x, list) and len(x) > 0 else 0))
    
    # extract number of previous events
    data['has_prev_payouts'] = data['previous_payouts'].apply(len)
    
    # convert nans to 0 for various features
    data[np.isnan(data['has_header'])] = 0
    data[np.isnan(data['delivery_method'])] = 0
    data[np.isnan(data['sale_duration'])] = 0
    data[np.isnan(data['org_facebook'])] = 0
    data[np.isnan(data['org_twitter'])] = 0
    
    #convert category to binary
    data['listed'] = data['listed'].apply(lambda x: 1 if x == 'y' else 0)
    
    #drop unecessary columns
    data.drop(columns=[
        'country',
        'email_domain',
        'event_created',
        'event_end',
        'event_published',
        'event_start',
        'object_id',
        'previous_payouts',
        'ticket_types',
        'user_created',
        'venue_address',
        'venue_country',
        'venue_latitude',
        'venue_longitude',
        'venue_name',
        'venue_state',
        'sale_duration2',
        'gts',
        'num_order',
        'num_payouts'
    ], inplace=True)
    
    # convert categories to binary
    data['org_facebook'] = data['org_facebook'].apply(lambda x: x if x==0 else 1)
    data['org_twitter'] = data['org_twitter'].apply(lambda x: x if x==0 else 1)
    data['delivery_method'] = data['delivery_method'].apply(lambda x: x if x==0 else 1)
    data['user_type'] = data['delivery_method'].apply(lambda x: x if x==1 else 0)
    
    if not predict:
        data.drop(columns=[
            'acct_type',
            'approx_payout_date'
        ], inplace=True)
    else:
        data.drop(columns=['sequence_number'], inplace=True)
    
    return data

def train_test_split_data(data, test_size=0.25):
    """
    Create train/test split of data.
    
    Parameters:
        data - data to split
        test_size - percentage to split to test
        
    Returns:
        X_train, X_test, y_train, y_test
    
    """
    
    y = data['fraud'].values
    X = data.drop(columns=['fraud','description','name','org_desc','org_name','payee_name']).values
    
    return train_test_split(X, y, test_size=test_size, stratify=y, shuffle=True)

def get_model_data(filepath):
    """
    Run all functions to load and clean data and return train/test data for the model.
    """
    
    data = load_data(filepath)
    data = clean_data(data)
    return train_test_split_data(data)
    
def clean_api_data(data):
    
    columns = ['body_length', 'delivery_method', 'fb_published', 'has_analytics', 'has_header', 'has_logo', 'listed', 'name_length', 'org_facebook', 'org_twitter', 'sale_duration', 'show_map', 'user_age', 'user_type', 'currency: CAD', 'currency: EUR', 'currency: GBP', 'currency: MXN', 'currency: NZD', 'currency: USD', 'channels: 4', 'channels: 5', 'channels: 6', 'channels: 7', 'channels: 8', 'channels: 9', 'channels: 10', 'channels: 11', 'channels: 12', 'channels: 13', 'payout_type: ACH', 'payout_type: CHECK', 'max_price', 'has_prev_payouts']
    
    data = pd.DataFrame([data])
    
    data.fillna(0, inplace=True)
    
    #convert category to binary
    data['listed'] = data['listed'].apply(lambda x: 1 if x == 'y' else 0)
    
    for column in columns:
        if not column in data.columns:
            data[column] = 0
    
    if f"currency: {data['currency'].values[0]}" in columns:
        data[f"currency: {data['currency'].values[0]}"] = 1
    if f"channels: {data['channels'].values[0]}" in columns:
        data[f"channels: {data['channels'].values[0]}"] = 1
    if f"payout_type: {data['payout_type'].values[0]}" in columns:
        data[f"payout_type: {data['payout_type'].values[0]}"] = 1
        
    # extract max ticket price for event
    data['max_price'] = (data['ticket_types']
                     .apply(lambda x: max([ticket['cost'] for ticket in x]) if isinstance(x, list) and len(x) > 0 else 0))
    
    # extract number of previous events
    data['has_prev_payouts'] = data['previous_payouts'].apply(len)
        
    #drop unecessary columns
    data.drop(columns=[
        'country',
        'email_domain',
        'event_created',
        'event_end',
        'event_published',
        'event_start',
        'object_id',
        'previous_payouts',
        'ticket_types',
        'user_created',
        'venue_address',
        'venue_country',
        'venue_latitude',
        'venue_longitude',
        'venue_name',
        'venue_state',
        'description',
        'name',
        'org_desc',
        'org_name',
        'payee_name',
        'sequence_number'
    ], inplace=True)
    
    # convert categories to binary
    data['org_facebook'] = data['org_facebook'].apply(lambda x: x if x==0 else 1)
    data['org_twitter'] = data['org_twitter'].apply(lambda x: x if x==0 else 1)
    data['delivery_method'] = data['delivery_method'].apply(lambda x: x if x==0 else 1)
    data['user_type'] = data['delivery_method'].apply(lambda x: x if x==1 else 0)
    
    data.drop(columns=[
        'currency','channels','payout_type'
    ], inplace=True)
    
    return data.values