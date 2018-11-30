.. _examples:

:github_url: https://github.com/jrbourbeau/openbrewerydb-python

*************
Example Usage
*************

We can use the ``openbrewerydb.load`` function to query Open Brewery DB and retrieve brewery information. For example, we can get brewery data for the state of Wisconsin

.. code-block:: python

    >>> import openbrewerydb
    >>> data = openbrewerydb.load(state='wisconsin')

What's returned is a Pandas ``DataFrame`` with information about the breweries in Wisconsin (each row is a different brewery). The columns of this ``DataFrame`` are:

.. code-block:: python

    >>> data.columns
    Index(['brewery_type', 'city', 'country', 'id', 'latitude', 'longitude',
        'name', 'phone', 'postal_code', 'state', 'street', 'tag_list',
        'updated_at', 'website_url'],
        dtype='object')

At this point, all the normal functionality in Pandas is available for us to play with. For example, if we want to know what the distribution of brewery types, we can use the ``DataFrame.value_counts()`` method to get the total number of each brewery type

.. code-block:: python

    >>> brewery_types = data['brewery_type'].value_counts()
    >>> brewery_types
    micro         89
    brewpub       73
    contract      17
    planning      16
    regional       9
    large          5
    proprietor     2
    Name: brewery_type, dtype: int64