# SWU API

Python libary for the use of the public transport and carsharing API of the Stadtwerke Ulm / Neu-Ulm (SWU) more easily.

[![Python](https://img.shields.io/pypi/pyversions/swu_api.svg)](https://badge.fury.io/py/swu_api)
[![PyPI](https://badge.fury.io/py/swu_api.svg)](https://badge.fury.io/py/swu_api)
[![Python](https://img.shields.io/github/license/CeKl/dev_swu_api.svg)](https://opensource.org/licenses/MIT)
[![DeepSource](https://deepsource.io/gh/CeKl/dev_swu_api.svg/?label=active+issues&token=qITdjDkP_9a7eS5lCgccaIHO)](https://deepsource.io/gh/CeKl/swu_api/?ref=repository-badge)

Details and documentation of the API can be found on their website: <https://api.swu.de/mobility/>.

SWU provides the data free of charge under [CC-0-license](http://creativecommons.org/publicdomain/zero/1.0/).

Principle of using API requests: As much as necessary and as little as possible.

## Table of Contents

- [SWU API](#swu-api)
  - [Table of Contents](#table-of-contents)
  - [Install](#install)
  - [Structure](#structure)
  - [Usage](#usage)
    - [example for helper functions](#example-for-helper-functions)
      - [public transport](#public-transport)
      - [carsharing](#carsharing)
    - [example for basic API request](#example-for-basic-api-request)
    - [save API examples](#save-api-examples)
  - [Release Notes](#release-notes)
    - [0.1](#01)
    - [0.1.1](#011)

## Install

For installation use [Pypi](https://pypi.org/project/swu_api/):

`pip install swu_api` or `pip3 install swu_api`

## Structure

The libary is divided into two components. One part deals with the request of the basedata and livedata (swu_functions.py). The other part (swu_helper.py) provides help functions to support requests.

The swu_helper is able to request data that changes infrequently (basedata) at a predefined interval and store it in a buffer. This reduces the number of queries.

With the help of swu_demo_data you can download examples of the API data and save them to a json file.

## Usage

Short example are listed below. Details are listed in the notebook [example_carsharing](https://github.com/CeKl/dev_swu_api/blob/main/examples/example_carsharing.ipynb) and [example_public_transport](https://github.com/CeKl/dev_swu_api/blob/main/examples/example_public_transport.ipynb).

### example for helper functions

#### public transport

Get information about public transport.

```python
from swu_api.swu_helper import swu_api_pt_helper

swu_pt_helper = swu_api_pt_helper(use_buffer=True)

# get data of station with searchterm for searchparameter
station_info = swu_pt_helper.get_station_info(serach_parameter='StopName', serach_term='Justizgebäude')

# get informations for a given vehicle
vehicle_info = swu_pt_helper.get_vehicle_info(vehiclenumber=42)

# get direction of a given route
route_direction = swu_pt_helper.get_route_direction(routenumber=1)

# get routepoints for given route and direction
get_route = swu_pt_helper.get_route(routenumber=1, direction=1)
```

#### carsharing

Get information about carsharing.

```python
from swu_api.swu_helper import swu_api_cs_helper

swu_cs_helper = swu_api_cs_helper(use_buffer=True)

# get details of a station with given id
station_details = swu_cs_helper.get_station_details(station_id='5162')
```

### example for basic API request

Basic data of the SWU API.

```python
from swu_api.swu_fuctions import swu_pt_functions

swu_func = swu_pt_functions()

# get data of a route
route_data = swu_func.base_route(routenumber=1, contentscope='basic')

# get livedata of trip for given vehiclenumber
vehicle_trip = swu_func.live_vehicle_trip(vehiclenumber=42)

```

### save API examples

Save output of the API to a json file for further analyse.

```python
from swu_api.swu_demo_data import api_to_json

swu_demo = api_to_json(save_filter='all', folderpath='C:/Users/Default/Desktop/swu_data')

```

## Release Notes

### 0.1

- Initial release

### 0.1.1

- Fix Readme

- - -
[MIT License](https://opensource.org/licenses/MIT) Copyright (c) 2021 Cedric Klimt

API-data provided by SWU verkehrstechnik@swu.de [![License: CC0-1.0](https://licensebuttons.net/l/zero/1.0/80x15.png)](http://creativecommons.org/publicdomain/zero/1.0/)
