from rest_framework import serializers
from django.core.exceptions import ObjectDoesNotExist


class ObjectIDField(serializers.PrimaryKeyRelatedField):
    def to_internal_value(self, data):
        try:
            value = self.get_queryset().get(pk=data)
            return value.id
        except ObjectDoesNotExist:
            self.fail('does_not_exist', pk_value=data)
        except (TypeError, ValueError):
            self.fail('incorrect_type', data_type=type(data).__name__)
