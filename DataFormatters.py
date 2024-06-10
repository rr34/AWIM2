import datetime
import numpy as np

# numpy datetime64 is International Atomic Time (TAI), not UTC, so it ignores leap seconds.
# numpy datetime64 uses astronomical year numbering, i.e. year 2BC = year -1, 1BC = year 0, 1AD = year 1
def format_datetime(input_datetime_UTC, direction):
    exif_datetime_format = "%Y:%m:%d %H:%M:%S" # directly from exif documentation
    numpy_datetime_format = "%Y-%m-%dT%H:%M:%S" # from numpy documentation
    readable_datetime_format = "%Y-%m-%d %H:%M:%S" # my opinion
    filename_datetime_format = "%Y-%m-%d %H%M%S" # my opinion

    
    if direction == 'to string for exif':
        if isinstance(input_datetime_UTC, datetime.datetime):
            output = input_datetime_UTC.strftime(exif_datetime_format)
        elif isinstance(input_datetime_UTC, np.datetime64):
            pass # TODO convert this format, necessary?

    elif direction == 'to string for AWIMtag':
        if isinstance(input_datetime_UTC, datetime.datetime):
            output = input_datetime_UTC.strftime(readable_datetime_format)
        elif isinstance(input_datetime_UTC, np.datetime64):
            pass # TODO convert this format, necessary?

    elif direction == 'to string for filename':
        if isinstance(input_datetime_UTC, datetime.datetime):
            output = input_datetime_UTC.strftime(filename_datetime_format)
        elif isinstance(input_datetime_UTC, np.datetime64):
            pass # TODO convert this format, necessary?

    elif direction == 'from AWIM string':
        datetime_object = datetime.datetime.strptime(input_datetime_UTC, readable_datetime_format)
        datetime_string_for_numpy = datetime.datetime.strftime(datetime_object, numpy_datetime_format)
        output = np.datetime64(datetime_string_for_numpy)

    return output