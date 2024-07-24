import uuid
from dataclasses import fields
from datetime import datetime
from typing import List, Type


def convert_value(value):
    if isinstance(value, uuid.UUID):
        return str(value)
    elif isinstance(value, datetime):
        # Прошу прощения за костыль,
        # форматируем дату и время с миллисекундами и таймзоной, так как в sqlite
        # обрезан 0 в конце миллисекунд
        formatted_date = value.strftime('%Y-%m-%d %H:%M:%S.%f%z')
        main_part, timezone = formatted_date[:-2], formatted_date[-2:]
        millis_part = main_part.split('.')[1].split('+')[0]
        trimmed_millis = millis_part.rstrip('0') if millis_part[-1] == '0' else millis_part
        formatted_main = main_part.split('.')[0] + '.' + trimmed_millis
        return f'{formatted_main}+{timezone}'
    return value


def rows_to_dataclass(dataclass_type: Type, rows: List[tuple]) -> List:
    dataclass_objects = []
    field_names = [field.name for field in fields(dataclass_type)]
    for row in rows:
        field_values = {field_name: convert_value(value)
                        for field_name, value in zip(field_names, row)}
        dataclass_objects.append(dataclass_type(**field_values))
    return dataclass_objects
