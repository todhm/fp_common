from datetime import datetime as dt
from marshmallow import (
    fields
)
from marshmallow_dataclass import NewType
from marshmallow.validate import ValidationError, Validator
import typing
import logging

logger = logging.getLogger(__name__)


class PyDateTimeField(fields.DateTime):
    def deserialize(
        self,
        value: typing.Any,
        attr: str = None,
        data: typing.Mapping[str, typing.Any] = None,
        **kwargs
    ):
        if isinstance(value, dt):
            return value
        return super().deserialize(value, attr, data, **kwargs)


class DateTimeValidator(Validator):

    default_message = "Not a valid datetime"

    def _format_error(self, value) -> str:
        value_text = f"{value} error "
        return super()._format_error(value_text)

    def __call__(self, value) -> dt:
        try:
            if type(value) is not dt:
                raise ValidationError(self._format_error(value))
        except TypeError as error:
            raise ValidationError(self._format_error(value)) from error

        return value


DataclassDateTime = NewType("NewDateTime", dt, field=PyDateTimeField, validate=DateTimeValidator)