import datetime
from haystack.indexes import *
from haystack import site
from dar.models import Entry

class EntryIndex(SearchIndex):
    text = CharField(document=True, use_template=True)
    author = CharField(model_attr='mp', null=True, faceted=True)
    day = DateField(model_attr='day__date', faceted=True)

    def get_queryset(self):
        """Used when the entire index for model is updated."""
        return Entry.objects.filter(day__date__lte=datetime.date.today())

site.register(Entry, EntryIndex)


