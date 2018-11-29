# openbrewerydb-python

[![Build Status](https://travis-ci.org/jrbourbeau/openbrewerydb-python.svg?branch=master)](https://travis-ci.org/jrbourbeau/openbrewerydb-python)
[![GitHub license](https://img.shields.io/github/license/jrbourbeau/openbrewerydb-python.svg)](https://github.com/jrbourbeau/openbrewerydb-python/blob/master/LICENSE)


A Python wrapper for the [Open Brewery DB API](https://www.openbrewerydb.org/).


## Installation

`openbrewerydb` can be installed directly from GitHub via

```
pip install git+https://github.com/jrbourbeau/openbrewerydb-python.git
```

This will install `openbrewerydb` along with it's dependencies listed below.

#### Dependencies

- Requests
- Pandas

## Usage

```python
>>> import openbrewerydb
>>> data = openbrewerydb.load(state='wisconsin')
>>> data.head()
```

brewery_type|city|country|id|latitude|longitude|name|phone|postal_code|state|street|updated_at|website_url
---|---|---|---|---|---|---|---|---|---|---|---|---
brewpub|Whitewater|United States|7783|42.8323014016847|-88.7142734423486|841 Brewhouse|2624738000|53190-2126|Wisconsin|841 E Milwaukee St|2018-08-24T16:41:48.283Z|
brewpub|Sheboygan|United States|7784|43.7567439183673|-87.7130570204082|8th Street Ale Haus|9202087540|53081-3402|Wisconsin|1132 N 8th St|2018-08-24T16:41:49.804Z|http://www.sheboyganalehaus.com
brewpub|Madison|United States|7788|43.1257630536673|-89.33026|ALT Brew / Greenview Brewing LLC|6083523373|53704-2522|Wisconsin|1808 Wright St|2018-08-24T16:41:54.256Z|http://www.altbrew.com
brewpub|Hayward|United States|7789|46.0104853|-91.4887672|Angry Minnow, The|7159343055|54843-7112|Wisconsin|10440 Florida Ave|2018-08-24T16:41:55.714Z|http://www.angryminnow.com
brewpub|Appleton|United States|7790|44.2617360204082|-88.4139147959184|Appleton Beer Factory|9203649931|54911-5803|Wisconsin|603 W College Ave|2018-08-24T16:41:57.265Z|http://www.appletonbeerfactory.com


## License

[MIT License](LICENSE)
