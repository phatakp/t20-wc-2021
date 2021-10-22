from django.core.exceptions import ValidationError


def score_validator(value):
    if value:
        if '/' in value:
            vals = value.split('/')
            try:
                vals[0] = int(vals[0])
                vals[1] = float(vals[1])
            except:
                raise ValidationError("Invalid format")
        else:
            raise ValidationError('Invalid format')
