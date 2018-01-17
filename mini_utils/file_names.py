import datetime
import hashlib
import os
import uuid

from django.utils.encoding import force_str


def file_name_generator(prefix, instance, filename):
    now = datetime.datetime.now()
    year = str(now.year)
    month = str(now.month)
    day = str(now.day)

    hash_year = hashlib.sha1(year.encode()).hexdigest()[30:]
    hash_month = hashlib.sha1(('{}-{}'.format(year, month)).encode()).hexdigest()[20:30]
    hash_day = hashlib.sha1('{}-{}-{}'.format(year, month, day).encode()).hexdigest()[10:20]

    dirname = force_str('{prefix}{sep}{y}{sep}{m}{sep}{d}'.format(prefix=prefix, y=hash_year, m=hash_month,
                                                                  d=hash_day, sep=os.sep))
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4().hex, ext)
    return os.path.join(dirname, filename)


def get_generator(prefix):
    def generator(instance, filename):
        return file_name_generator(prefix=prefix, instance=instance, filename=filename)

    return generator
