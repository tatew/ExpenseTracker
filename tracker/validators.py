from django.core.exceptions import ValidationError

def validate_file_extension_csv(value):
    if not value.name.endswith('.csv'):
        raise ValidationError(u'File extention must be .csv')