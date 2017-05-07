from datetime import datetime


def maybe_convert_int(data, key):
    return maybe_convert(data, key, int)


def maybe_convert_date(data, key, timestamp=False):
    if timestamp:
        return maybe_convert(data, key, lambda value: int(datetime.strptime(value, '%Y-%m-%d').timestamp()))

    return maybe_convert(data, key, lambda value: datetime.strptime(value, '%Y-%m-%d'))


def maybe_convert(data, key, convert_func):
    if key in data:
        try:
            value = data[key]
            if isinstance(value, list):
                data[key] = convert_func(next(iter(value)))
            else:
                data[key] = convert_func(value)

        except ValueError:
            del data[key]