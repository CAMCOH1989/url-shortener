from datetime import datetime
from functools import singledispatch
from types import MappingProxyType

from asyncpg import Record


@singledispatch
def convert(value):
    raise NotImplementedError(f'Unserializable value: {value!r}')


@convert.register(Record)
def convert_asyncpg_record(value: Record):
    return dict(value)


@convert.register(datetime)
def convert_datetime(value: datetime):
    return value.isoformat()


@convert.register(MappingProxyType)
def convert_mapping_proxy_type(value: MappingProxyType):
    return dict(value.items())
