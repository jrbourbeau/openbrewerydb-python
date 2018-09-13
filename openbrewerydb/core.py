
from itertools import count
import pandas as pd
import requests

from .states import states as valid_states


def _execute_request(url):
    r = requests.get(url)
    json = r.json()
    if json:
        dtypes = {
                  'id': int,
                  'brewery_type': 'category',
                  'state': 'category',
                  'country': 'category',
                  'latitude': float,
                  'longitude': float,
                  }
        df = pd.DataFrame(json).astype(dtypes)
    else:
        df = pd.DataFrame()
    return df


def _construct_query(state=None, city=None, brewery_type=None, sort=None,
                     ascending=True):
    url = 'https://api.openbrewerydb.org/breweries'
    selectors = []
    if state is not None:
        if state not in valid_states:
            raise ValueError(f'Invalid state entered, \'{state}\'')
        selectors.append(f'by_state={state}')
    if city is not None:
        selectors.append(f'by_city={city}')
    if brewery_type is not None:
        valid_types = {'micro', 'regional', 'brewpub', 'large', 'planning'}
        if brewery_type not in valid_types:
            raise ValueError(f'Invalid brewery_type entered. Must be in '
                             '{valid_types}, but got \'{brewery_type}\'.')
        selectors.append(f'by_type={brewery_type}')
    if sort is not None:
        order = '' if ascending else '-'
        selectors.append(f'sort={order}{sort}')

    if selectors:
        url += '?' + '&'.join(selectors)

    return url


def _gen_data(state=None, city=None, brewery_type=None, sort=None,
              ascending=True):

    url = _construct_query(state=state,
                           city=city,
                           brewery_type=brewery_type,
                           sort=sort,
                           ascending=ascending)
    for page in count():
        query_url = url + f'&page={page}&per_page=50'
        df = _execute_request(query_url)
        if df.empty:
            return
        else:
            yield df


def load(state=None, city=None, brewery_type=None, sort=None, ascending=True):
    """ Perform query against Open Brewery DB

    Parameters
    ----------
    state : str, optional
        State name to filter by (default is None, all states will be included).
    city : str, optional
        City name to filter by (default is None, all cities will be included).
    brewery_type : {None, 'micro', 'regional', 'brewpub', 'large', 'planning'}
        Brewery type to filter by (default is None, all brewery types will be
        included).
    sort : {None, 'state', 'city', 'type'}
        Value to sort data according to (default is None, no sorting will be
        done).
    ascending : boolean, optional
        Option to sort in ascending or descending order (default is True,
        so ascending order will be used). Only used if sort is not None.

    Returns
    -------
    data : pandas.DataFrame
        DataFrame

    Examples
    --------
    >>> import openbrewerydb
    >>> data = openbrewerydb.load(state='wisconsin')
    """
    data_generator = _gen_data(state=state,
                               city=city,
                               brewery_type=brewery_type,
                               sort=sort,
                               ascending=ascending)
    data = [d for d in data_generator]
    if not data:
        raise ValueError('No data found for this query')
    df = pd.concat(data, ignore_index=True)

    return df
