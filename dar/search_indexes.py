import datetime
from haystack import indexes
from dar.models import Entry

class EntryIndex(indexes.SearchIndex):
    text = indexes.CharField(document=True, use_template=True)
    author = indexes.CharField(model_attr='mp', null=True)
    day = indexes.DateField(model_attr='day__date')

    def get_model(self):
        return Entry

site.register(Entry, EntryIndex)
