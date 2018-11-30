
import pandas as pd
import pytest

from openbrewerydb.core import (format_state, format_city, format_brewery_type,
                                _construct_query, _execute_request, load)

base_url = 'https://api.openbrewerydb.org/breweries'


@pytest.mark.parametrize('state', [
    'texas',
    'Wisconsin',
])
def test_format_state(state):
    result = format_state(state)
    expected = f'by_state={state}'
    assert result == expected


def test_format_state_raises():
    with pytest.raises(ValueError) as err:
        format_state(state='tejas')
    assert 'Invalid state entered' in str(err.value)


@pytest.mark.parametrize('brewery_type', [
    'micro',
    'regional',
    'brewpub',
    'large',
    'planning',
    'bar',
    'contract',
    'proprietor',
])
def test_format_brewery_type(brewery_type):
    result = format_brewery_type(brewery_type)
    expected = f'by_type={brewery_type}'
    assert result == expected


@pytest.mark.parametrize('brewery_type', [
    'invalid',
    'Micro',
])
def test_format_brewery_type_raises(brewery_type):
    with pytest.raises(ValueError) as err:
        format_brewery_type(brewery_type=brewery_type)
    assert 'Invalid brewery_type entered' in str(err.value)


@pytest.mark.parametrize('city', [
    'Alameda',
    'new york',
])
def test_format_city(city):
    result = format_city(city)
    expected = f'by_city={city}'
    assert result == expected


@pytest.mark.parametrize('city, state, brewery_type, expected', [
    ('madison', 'wisconsin', 'micro', f'{base_url}?by_state=wisconsin&by_city=madison&by_type=micro'),
    (None, 'wisconsin', 'micro', f'{base_url}?by_state=wisconsin&by_type=micro'),
    ('madison', None, 'micro', f'{base_url}?by_city=madison&by_type=micro'),
    ('madison', 'wisconsin', None, f'{base_url}?by_state=wisconsin&by_city=madison'),
])
def test__construct_query(city, state, brewery_type, expected):
    assert _construct_query(state=state, city=city, brewery_type=brewery_type) == expected


@pytest.mark.remote_data
def test__execute_request():
    url = _construct_query(city='dallas',
                           state='texas',
                           brewery_type='micro')
    df = _execute_request(url)
    assert (df['city'] == 'Dallas').all()
    assert (df['state'] == 'Texas').all()
    assert (df['brewery_type'] == 'micro').all()


@pytest.mark.remote_data
def test_load():
    df = load(city='dallas',
              state='texas',
              brewery_type='micro')
    assert isinstance(df, pd.DataFrame)
    assert (df['city'] == 'Dallas').all()
    assert (df['state'] == 'Texas').all()
    assert (df['brewery_type'] == 'micro').all()


@pytest.mark.remote_data
def test_load_no_data():
    with pytest.raises(ValueError) as err:
        load(city='invalid_city',
             state='maine')
    assert 'No data found for this query' in str(err.value)
