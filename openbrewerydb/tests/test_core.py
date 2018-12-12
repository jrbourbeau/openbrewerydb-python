import re
import time
import pandas as pd
import pytest
from unittest import mock

from openbrewerydb.constants import dtypes
from openbrewerydb.core import (_validate_state, _validate_brewery_type,
                                _format_request_params, _get_data, load, timer)

from example_data import test_json_data


@pytest.mark.parametrize('state', [
    'texas',
    'Wisconsin',
])
def test__validate_state(state):
    result = _validate_state(state)
    assert result is None


def test__validate_state_raises():
    with pytest.raises(ValueError) as err:
        _validate_state('tejas')
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
    result = _validate_brewery_type(brewery_type)
    assert result is None


@pytest.mark.parametrize('brewery_type', [
    'invalid',
    'Micro',
])
def test__validate_brewery_type(brewery_type):
    with pytest.raises(ValueError) as err:
        _validate_brewery_type(brewery_type=brewery_type)
    assert 'Invalid brewery_type entered' in str(err.value)


@pytest.mark.parametrize('city, state, brewery_type, page', [
    ('portland', 'Maine', 'micro', None),
    ('portland', 'Maine', 'micro', 7),
    (None, 'Maine', 'micro', None),
    ('portland', None, 'micro', None),
    ('portland', 'Maine', None, None),
    (None, None, None, None),
])
def test__format_request_params(city, state, brewery_type, page):
    result = _format_request_params(city=city,
                                    state=state,
                                    brewery_type=brewery_type,
                                    page=page)
    expected = {'by_state': state,
                'by_city': city,
                'by_type': brewery_type,
                }
    if page is not None:
        expected['page'] = str(page)
        expected['per_page'] = '50'

    assert result == expected


@pytest.mark.parametrize('page', [None, 9])
def test__format_request_params_keys(page):
    result = _format_request_params(page=page)

    expected = {'by_state',
                'by_city',
                'by_type'}
    if page is not None:
        expected.update(['page', 'per_page'])

    assert set(result.keys()) == expected


@pytest.mark.parametrize('return_value, expected', [
    (test_json_data, pd.DataFrame(test_json_data).astype(dtypes)),
    ((), pd.DataFrame()),
])
@mock.patch('openbrewerydb.core._get_request')
def test__get_data(mock_get_request, return_value, expected):
    mock_get_request.return_value = mock.Mock()
    mock_get_request.return_value.json.return_value = return_value

    result = _get_data()
    pd.testing.assert_frame_equal(result, expected)


@mock.patch('openbrewerydb.core._get_data')
def test_load_is_concat(mock_get_data):
    test_data = [pd.DataFrame([1, 4, 5]),
                 pd.DataFrame([7, 2]),
                 pd.DataFrame([4.2, 4]),
                 pd.DataFrame(),
                 ]

    mock_get_data.side_effect = test_data
    result = load()
    expected = pd.concat(test_data, ignore_index=True)
    pd.testing.assert_frame_equal(result, expected)


@mock.patch('openbrewerydb.core._get_data')
def test_load_no_data(mock_get_data):
    with pytest.raises(ValueError) as err:
        mock_get_data.return_value = pd.DataFrame()
        load()
    assert 'No data found for this query' in str(err.value)


@pytest.mark.remote_data
def test_load():
    df = load(city='dallas',
              state='texas',
              brewery_type='micro')
    assert isinstance(df, pd.DataFrame)
    assert (df['city'] == 'Dallas').all()
    assert (df['state'] == 'Texas').all()
    assert (df['brewery_type'] == 'micro').all()


@pytest.mark.parametrize('verbose', [True, False])
@mock.patch('openbrewerydb.core._get_data')
def test_load_verbose(mock_get_data, verbose, capsys):
    test_data = [pd.DataFrame([1, 4, 5]),
                 pd.DataFrame([7, 2]),
                 pd.DataFrame([4.2, 4]),
                 pd.DataFrame(),
                 ]
    mock_get_data.side_effect = test_data
    load(verbose=verbose)
    out, err = capsys.readouterr()
    if verbose:
        assert 'Loaded data for ' in out
        assert 'Time elapsed: ' in out
    else:
        assert out == ''


@pytest.mark.parametrize('verbose', [True, False])
def test_timer(capsys, verbose):
    with timer(verbose=verbose):
        time.sleep(1)
    out, err = capsys.readouterr()
    if verbose:
        assert re.match(r'\nTime elapsed: \d+\.\d+ sec', out) is not None
    else:
        assert out == ''
