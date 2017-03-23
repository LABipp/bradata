def _make_url(api_house=None, base_url= None, params=None):
    """
    It builds the url based on the house webservice and parameters
    Args:
        api_house: str:: 'camara' or 'senado'
        webservice: str:: specify a webservice such as 'deputados', '
        params: dict::  parameters that compose the url

    Returns: str
        The API url
    """



    if api_house == None:
        raise ReferenceError ('No API House Specified')

    if base_url == None:
        raise ReferenceError ('No Base Url Specified')

    elif api_house == 'camara':
        # EndPoints
        for i, items in enumerate(params.items()):

            key, value = [_treat_inputs(i) for i in items]

            if value == None:
                value = ''

            base_url += key + '=' + value

            if len(params) - i > 1:

                base_url += '&'

    return base_url

def _treat_inputs(value):
    """
    Make sure that inputs are in the right type

    Ints and floats are converted to strings

    Args:
        value: str, int, float

    Returns: Ints and floats are converted to strings
    """
    if value is None:
        return value

    if not isinstance(value, (int, float, str)):
        raise AttributeError('This is a {}.\n'
                             'Make sure to insert an int, float or str'
                             .format(type(value)))

    if isinstance(value, (int, float)):
        value = str(value)

    return value


def _must_contain(this=None, keys=None):
    """
    Check whether the specified values exists on a dict

    This function presumes that all keys are mapped on this dict
    Args:
        this: dict :: variable names and their values
        keys: list :: variable names that must not be None

    Returns:
        True if the dict contains the values
        Raise error if there are missing values
    """

    result = {k: v is None for k, v in this.items() if k in keys}

    missing_keys = [k for k, v in result.items() if v is True]

    if len(missing_keys) != 0:
        raise AttributeError('{} must have a value'.format(','.join(str(p) for p in missing_keys)))

    else:
        return True