#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 17/12/2017 15:49
# @Author  : Charles
# @File    : bitmexClient.py.py
# @Software: PyCharm Community Edition

from bravado.client import SwaggerClient
from bravado.requests_client import RequestsClient
from library.BitMEXAPIKeyAuthenticator import APIKeyAuthenticator
import json
import pprint


HOST = "https://www.bitmex.com"
SPEC_URI = HOST + "/api/explorer/swagger.json"

# See full config options at http://bravado.readthedocs.io/en/latest/configuration.html
config = {
  # Don't use models (Python classes) instead of dicts for #/definitions/{models}
  'use_models': False,
  # This library has some issues with nullable fields
  'validate_responses': False,
  # Returns response in 2-tuple of (body, response); if False, will only return body
  'also_return_response': True,
}

bitMEX = SwaggerClient.from_url(
  SPEC_URI,
  config=config)

pp = pprint.PrettyPrinter(indent=2)

# You can get a feel for what is available by printing these objects.
# See also https://testnet.bitmex.com/api/explorer
print('---The BitMEX Object:---')
print(dir(bitMEX))
print('\n---The BitMEX.Trade Object:---')
print(dir(bitMEX.Trade))

# Basic unauthenticated call
res, http_response = bitMEX.Trade.Trade_get(symbol='XBTUSD', count=1).result()
print('\n---A basic Trade GET:---')
pp.pprint(res)
print('\n---Response details:---')
print("Status Code: %d, headers: %s" % (http_response.status_code, http_response.headers))


#
# Authenticated calls
#
# To do authentication, you must generate an API key.
# Do so at https://testnet.bitmex.com/app/apiKeys

API_KEY = 'SwcHA0YKoYai55_aDRnwP6v9'
API_SECRET = 'ere_BrBO7BLNHK290zAPLzhBhII2zUrsWM3gG0R3MbJgtXxp'

request_client = RequestsClient()
request_client.authenticator = APIKeyAuthenticator(HOST, API_KEY, API_SECRET)

bitMEXAuthenticated = SwaggerClient.from_url(
  SPEC_URI,
  config=config,
  http_client=request_client)

# Basic authenticated call
print('\n---A basic Position GET:---')
print('The following call requires an API key. If one is not set, it will throw an Unauthorized error.')
res, http_response = bitMEXAuthenticated.Position.Position_get(filter=json.dumps({'symbol': 'XBTUSD'})).result()
pp.pprint(res)


# Basic order placement
# print(dir(bitMEXAuthenticated.Order))
# res, http_response = bitMEXAuthenticated.Order.Order_new(symbol='XBTUSD', orderQty=3, price=1000).result()
# print(res)
