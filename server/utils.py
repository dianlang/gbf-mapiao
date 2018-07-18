from typing import List, Dict, Union

import aiohttp
from aiohttp import web


class MissingInputException(Exception):
    pass


def check_and_covert_input(request: aiohttp.web.Request, fields: Union[List[Dict], Dict], source: str) -> Dict:
    r"""check input and convert them to requested type

        Several sentences providing an extended description. Refer to
        variables using back-ticks, e.g. `var`.


        Parameters
        ----------
        request : aiohttp.web.Request
            given request by aiohttp
        fields : Union[List[Dict], Dict]
            dict must have this keys: `name`, `type`, `required`.

             If `required` is `false`, you must give a `default`.

             example:
                 {'name': 'start', 'type': int, 'required': True, }

                 {'name': 'end', 'type': int, 'required': False, 'default': int(time.time())}

        source : {'query', 'match_info', 'headers'}

        Returns
        -------
        dict
            Dict[str, str]

        Raises
        ------
        MissingInputException
            If not all required fields were given.
        ValueError
            If not all given value can't be converted correctly

        Examples
        --------
        These are written in doctest format, and should illustrate how to
        use the function.

        >>> import time
        >>> fields = [
        >>>     {'name': 'start', 'type': int, 'required': True, },
        >>>     {'name': 'end', 'type': int, 'required': False, 'default': int(time.time())}
        >>> ]
        >>> data = check_and_covert_input(request, fields, 'query')

        >>> print(data)
            {'start': 123, 'end': 233}
        """
    data = {}
    missing_fields = []
    if isinstance(fields, dict):
        fields = [fields, ]
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
            if value is not None:
                try:
                    value = field.get('type', str)(value)
                except ValueError:
                    raise ValueError("Invalid input {}, can't be {}".format(field['name'], value))
            else:
                if 'default' in field:
                    value = field.get('type', str)(field['default'])
                else:
                    value = None
            data[field['name']] = value
    return data
