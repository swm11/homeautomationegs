#!/usr/bin/env python3
##############################################################################
# Display Octopus tariff data

import json
import octoclient
from dateutil.parser import parse

# personal data needed to access Octopus Energy site
from octopus_personal import Octopus_personal

def get_tariffs(apikey, tariff_code, product_code):
    client = octoclient.octoAPIClient(apikey)
    sc = client.electricity_tariff_unit_rates(tariff_code=tariff_code,
                                              product_code=product_code)
    return list(map(lambda t: {'from': parse(t['valid_from']),
                               'to'  : parse(t['valid_to']),
                               'cost': t['value_inc_vat']}, sc['results']))

# get tariff data from Octopus Energy
tariffs = get_tariffs(apikey=Octopus_personal.apikey,
                      product_code=Octopus_personal.product_code,
                      tariff_code=Octopus_personal.tariff_code)

# print tariff data
print("Tariffs going forward:")
for t in tariffs:
    print("%s - %s: %f" % (t['from'], t['to'], t['cost']))

exit(0)
