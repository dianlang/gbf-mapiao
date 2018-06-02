from typing import List, Dict

import aiohttp
from aiohttp import web


class MissingInputException(Exception):
    pass


def check_and_covert_input(request: aiohttp.web.BaseRequest, fields: List[Dict], source: str):
    data = {}
    missing_fields = []

    for field in fields:
        if field['required']:
            if not field['name'] in getattr(request, source):
                missing_fields.append(field['name'])

    if missing_fields:
        raise MissingInputException('missing {}'.format(', '.join(missing_fields)))
    else:
        for field in fields:
            # if field is required, default value is useless
            value = getattr(request, source).get(field['name'])
            if not value is None:
                try:
                    value = field.get('type', str)(value)
                except ValueError:
                    raise ValueError("Invalid input {}, can't be {}".format(field['name'], value))
            else:
                print(field['name'])
                value = field.get('type', str)(field['default'])
            data[field['name']] = value
    return data
