from django.conf import settings
from django.db import connection
from django.db.models.query import QuerySet


def extract_rel_field(model, related_to):
    """
    Given a model, extra the name of the field that rels to a user
    see: django-relationships
    """
    for field in model._meta.fields + model._meta.many_to_many:
        if field.rel and field.rel.to == related_to:
            return field.name
    for rel in model._meta.get_all_related_many_to_many_objects():
        if rel.model == related_to:
            return rel.var_name
