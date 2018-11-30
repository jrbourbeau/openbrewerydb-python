
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


def format_state(state):
    if state.lower() not in valid_states:
        raise ValueError(f'Invalid state entered, \'{state}\'')
    return f'by_state={state}'


def format_city(city):
    return f'by_city={city}'


def format_brewery_type(brewery_type):
    valid_types = {'micro',
                   'regional',
                   'brewpub',
                   'large',
                   'planning',
                   'bar',
                   'contract',
                   'proprietor',
                   }
    if brewery_type not in valid_types:
        raise ValueError(f'Invalid brewery_type entered. Must be in '
                         '{valid_types}, but got \'{brewery_type}\'.')
    return f'by_type={brewery_type}'


def _construct_query(state=None, city=None, brewery_type=None):
    base_url = 'https://api.openbrewerydb.org/breweries'
    selectors = []
    if state is not None:
        selectors.append(format_state(state))
    if city is not None:
        selectors.append(format_city(city))
    if brewery_type is not None:
        selectors.append(format_brewery_type(brewery_type))

    if selectors:
        url = base_url + '?' + '&'.join(selectors)

    return url


def _gen_data(state=None, city=None, brewery_type=None):

    url = _construct_query(state=state,
                           city=city,
                           brewery_type=brewery_type)
    for page in count(start=1):
        query_url = url + f'&page={page}&per_page=50'
        df = _execute_request(query_url)
        if df.empty:
            return
        else:
            yield df


def load(state=None, city=None, brewery_type=None):
    """ Query the Open Brewery DB

    Parameters
    ----------
    state : str, optional
        State name (case-insensitive) to select (default is ``None``, all
        states will be included). Note that `'district of columbia'` is a
        valid ``state``.
    city : str, optional
        City name (case-insensitive) to select (default is ``None``, all
        cities will be included).
    brewery_type : {None, 'micro', 'regional', 'brewpub', 'large', 'planning', 'bar', 'contract', 'proprietor'}
        Brewery type to select (default is ``None``, all brewery types will be
        included).

    Returns
    -------
    data : pandas.DataFrame
        DataFrame with query results

    Examples
    --------
    Get information about all micro breweries in Wisconsin

    >>> import openbrewerydb
    >>> data = openbrewerydb.load(state='wisconsin',
    ...                           brewery_type='micro')
    """
    data_generator = _gen_data(state=state,
                               city=city,
                               brewery_type=brewery_type)
    data = [d for d in data_generator]
    if not data:
        raise ValueError('No data found for this query')
    df = pd.concat(data, ignore_index=True)

    return df
