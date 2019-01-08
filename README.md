Simple client library for the excellent [apify.com API](https://www.apify.com/docs) 
## Installation
### Using pip (Recommended)
`pip install apifyunofficial`
### From source
1. Clone this repository
1. `python setup.py install`

## First use
To ensure the module works, create a .json configuration file like the example `apify_config.json`, then run this python code:
```python
import apifyunofficial as apify
print(apify.get_private_user_data(config=<CONFIG FILE>))
```

## What you get
* Most functions specified in the official API docs.
* Object-oriented structure that follows the docs closely.
* Fairly simple code
* Bugs (probably)

## How to help
* Contributing to this source code
* Finding bugs! (then filing issues)
* Suggesting ideas and improvements
