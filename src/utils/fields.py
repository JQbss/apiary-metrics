import django.db.models as model


class LowerCaseField(model.CharField):
    """
    A custom Django model field that stores the value in lowercase.
    """

    def get_prep_value(self, value):
        if value is not None:
            return value.lower()
        return value
