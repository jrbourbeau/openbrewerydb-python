
from openbrewerydb.constants import states


def test_num_states():
    # Number of US states + District of Columbia
    assert len(states) == 51
