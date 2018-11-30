.. _installation:

:github_url: https://github.com/jrbourbeau/openbrewerydb-python

************
Installation
************

----
PyPI
----

The latest release of ``openbrewerydb`` can be installed with ``pip``:

.. code-block:: console

    $ pip install openbrewerydb

This installs ``openbrewerydb``, along with it's dependencies.


-------------------
Development Version
-------------------

The latest development version of ``openbrewerydb`` can be installed directly from GitHub

.. code-block:: console

    $ pip install git+https://github.com/jrbourbeau/openbrewerydb-python.git

or you can fork the `openbrewerydb-python GitHub repository <https://github.com/jrbourbeau/openbrewerydb-python>`_ and install ``openbrewerydb`` on your local machine via

.. code-block:: console

    $ git clone https://github.com/jrbourbeau/openbrewerydb-python.git
    $ pip install openbrewerydb-python


------------
Dependencies
------------

``openbrewerydb`` has the following dependencies:

- `Python <https://www.python.org/>`_ (tested on versions >= 3.6)
- `Requests <http://docs.python-requests.org/en/master/>`_
- `Pandas <http://pandas.pydata.org/pandas-docs/stable/>`_

You can install these dependencies with ``conda`` 

.. code-block:: console

    $ conda install -c conda-forge python=3.6 requests pandas


or with ``pip``

.. code-block:: console

    $ pip install requests pandas
