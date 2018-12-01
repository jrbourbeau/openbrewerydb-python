
import types
import pandas as pd
import pytest
from unittest import mock

from openbrewerydb.constants import base_url, dtypes
from openbrewerydb.core import (format_state, format_city, format_brewery_type,
                                _construct_query, _execute_request, load,
                                _gen_data)

from example_data import test_json_data


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
    (None, None, None, base_url),
])
def test__construct_query(city, state, brewery_type, expected):
    result = _construct_query(state=state,
                              city=city,
                              brewery_type=brewery_type)
    assert result == expected


@pytest.mark.remote_data
def test_load():
    df = load(city='dallas',
              state='texas',
              brewery_type='micro')
    assert isinstance(df, pd.DataFrame)
    assert (df['city'] == 'Dallas').all()
    assert (df['state'] == 'Texas').all()
    assert (df['brewery_type'] == 'micro').all()


@mock.patch('openbrewerydb.core._gen_data')
def test_load_is_concat(mock_gen_data):
    test_data = [pd.DataFrame([1, 4, 5]),
                 pd.DataFrame([7, 2]),
                 pd.DataFrame([4.2, 4]),
                 pd.DataFrame(),
                 ]

    mock_gen_data.return_value = iter(test_data)
    result = load()
    expected = pd.concat(test_data, ignore_index=True)
    pd.testing.assert_frame_equal(result, expected)


@mock.patch('openbrewerydb.core._gen_data')
def test_load_no_data(mock_gen_data):
    with pytest.raises(ValueError) as err:
        mock_gen_data.return_value = []
        load()
    assert 'No data found for this query' in str(err.value)


@mock.patch('openbrewerydb.core._execute_request')
def test__gen_data(mock_execute_request):
    mock_execute_request.side_effect = [pd.DataFrame([1]),
                                        pd.DataFrame([6]),
                                        pd.DataFrame([7]),
                                        pd.DataFrame(),
                                        ]
    data_generator = _gen_data()
    assert isinstance(data_generator, types.GeneratorType)
    assert len(list(data_generator)) == 3


@mock.patch('openbrewerydb.core._execute_request')
def test__gen_data_no_data(mock_execute_request):
    mock_execute_request.return_value = pd.DataFrame()
    data_generator = _gen_data()
    assert isinstance(data_generator, types.GeneratorType)
    generated_data = [i for i in data_generator]
    assert isinstance(generated_data, list)
    assert len(generated_data) == 0


@pytest.mark.parametrize('return_value, expected', [
    (test_json_data, pd.DataFrame(test_json_data).astype(dtypes)),
    ((), pd.DataFrame()),
])
@mock.patch('openbrewerydb.core.requests.get')
def test__execute_request(mock_get, return_value, expected):
    mock_get.return_value = mock.Mock()
    mock_get.return_value.json.return_value = return_value

    result = _execute_request('someurl.com')

    pd.testing.assert_frame_equal(result, expected)
