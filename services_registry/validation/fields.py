"""
Field classes.
"""

import logging

from .validators import (ValidationError,
                         EnumValidator,
                         RegexValidator,
                         MinValueValidator,
                         MaxValueValidator)

LOG = logging.getLogger(__name__)

__all__ = (
    'Field', 'IntegerField', 'FloatField',
    'RegexField', 'BooleanField', 'NullBooleanField', 'ChoiceField', 
)

# These values, if given to validate(), will trigger the self.required check.
EMPTY_VALUES = (None, '', [], (), {}, set())

class FieldError(ValidationError):
    def __init__(self, key, message):
        msg = '{} for {}: {}'.format(self.__class__.__name__, key, message)
        super().__init__(msg)

class Field:

    error_message = 'Field not follow its specification'

    def __init__(self, *, required=False, default=None, error_message=None, validators=()):
        # required -- Boolean that specifies whether the field is required.
        # error_message -- optional
        # validators -- List of additional validators to use
        self.required = required
        self.validators = list(validators)
        if error_message is not None:
            self.error_message = error_message or self.error_message
        self.default = default
        # Using assertion: we don't start the beacon
        assert not required or default is None, 'required and default are mutually exclusive'
        self.name = 'Unknown'

    def set_name(self, n):
        self.name = n

    def run_validators(self, value):
        errors = []
        for v in self.validators:
            try:
                v(value)
            except ValidationError as e:
                errors.append(str(e))
        if errors:
            message = errors[0] if len(errors) == 1 else '\n' + '\n'.join([f'* {err}' for err in errors])
            raise FieldError(self.name, message)

    async def validate(self, value): # converted value
        if value in EMPTY_VALUES:
            if self.required:
                raise FieldError(self.name, 'required field')
            # LOG.debug('%s: %s is an empty value', self.name, value)
            return
        self.run_validators(value)

    async def convert(self, value, **kwargs):
        if value in EMPTY_VALUES:
            return self.default
        return value

    async def clean(self, req, value):
        """
        Validate the given value and return its "cleaned" value as an
        appropriate Python object. Raise FieldError for any errors.
        """
        value = await self.convert(value, request=req)
        await self.validate(value)
        return value


class ChoiceField(Field):

    def __init__(self, *args, **kwargs):
        self.choices = args
        if not self.choices:
            raise FieldError(self.name, 'You should select some choices')
        super().__init__(**kwargs)
        self.item_type = type(self.choices[0])
        self.validators.append(EnumValidator(self.choices))

    async def convert(self, value: str, **kwargs):
        if value in EMPTY_VALUES:
            return self.default
        try:
            return self.item_type(value)
        except (ValueError, TypeError):
            raise FieldError(self.name, f'{value} is not of type {self.item_type}')


class RegexField(Field):
    def __init__(self, pattern, ignore_case=False, **kwargs):
        self.pattern = pattern
        self.ignore_case = ignore_case
        super().__init__(**kwargs)
        self.validators = [RegexValidator(pattern, ignore_case)]


class IntegerField(Field):
    error_message = 'not a number'

    def __init__(self, *, max_value=None, min_value=None, **kwargs):
        self.max_value, self.min_value = max_value, min_value
        super().__init__(**kwargs)

        if max_value is not None:
            self.validators.append(MaxValueValidator(max_value))
        if min_value is not None:
            self.validators.append(MinValueValidator(min_value))

    async def convert(self, value: str, **kwargs) -> int:
        """
        Validate that int() can be called on the input. Return the result
        of int() or None for empty values.
        """
        # value = super().convert(value, **kwargs)
        if value in EMPTY_VALUES:
            return self.default
        try:
            return int(value)
        except (ValueError, TypeError):
            raise FieldError(self.name, self.error_message)

class FloatField(Field):
    error_message = 'not a float'

    def __init__(self, *, max_value=None, min_value=None, **kwargs):
        self.max_value, self.min_value = max_value, min_value
        super().__init__(**kwargs)

        if max_value is not None:
            self.validators.append(MaxValueValidator(max_value))
        if min_value is not None:
            self.validators.append(MinValueValidator(min_value))

    async def convert(self, value: str, **kwargs) -> int:
        """
        Validate that float() can be called on the input. Return the result
        of float() or None for empty values.
        Also works for scientific notation.
        """
        # value = super().convert(value, **kwargs)
        if value in EMPTY_VALUES:
            return self.default
        try:
            return float(value)
        except (ValueError, TypeError):
            raise FieldError(self.name, self.error_message)


class BooleanField(Field):
    error_message = 'not a boolean value'

    async def convert(self, value: str, **kwargs) -> bool:
        if value in EMPTY_VALUES:
            return self.default
        if value.lower() in ('false', '0'):
            return False
        return bool(value)


class NullBooleanField(Field):
    error_message = 'not a boolean value'

    async def convert(self, value: str, **kwargs) -> bool:
        # value = super().convert(value, **kwargs)
        if value in EMPTY_VALUES:
            return self.default
        if value.lower() in ('true', '1'):
            return True
        if value.lower() in ('false', '0'):
            return False
        return self.default


class ListField(Field):

    def __init__(self, *, items=None, separator=',', trim=True, **kwargs):
        self.separator = separator
        self.item_type = items or Field()
        self.trim = trim or True
        super().__init__(**kwargs)

    async def convert(self, value: str, **kwargs) -> set:
        if value in EMPTY_VALUES:
            return self.default
        values = value.split(self.separator)
        res = set()
        for v in values:
            if self.trim:
                v = v.strip()
            converted_v = await self.item_type.convert(v, **kwargs)
            res.add(converted_v)
        return list(res) # for the moment, cuz json.dumps not happy

    async def validate(self, values):
        if values in EMPTY_VALUES:
            return
        for value in values:
            await self.item_type.validate(value)
        return values


class SchemasField(ListField):

    async def convert(self, value: str, **kwargs) -> (set, set):
        values = value.split(self.separator) if value not in EMPTY_VALUES else []
        from ..schemas import partition
        return partition(values)

