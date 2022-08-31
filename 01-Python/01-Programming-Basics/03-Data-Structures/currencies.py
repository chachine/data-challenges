# pylint: disable=missing-docstring

# TODO: add some currency rates
RATES = {"USDEUR" : 0.85,
         "GBPEUR": 1.132,
         "CHFEUR": 0.86,
         "EURGBP": 0.885}

def convert(amount, currency):
    """returns the converted amount in the given currency
    amount is a tuple like (100, "EUR")
    currency is a string
    """
    pair = amount[1] + currency
    if pair in RATES.keys():
        return int( amount[0] * RATES[pair])
    else:
        return None
