import datetime
from haystack import indexes
from dar.models import Entry

class EntryIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    author = indexes.CharField(model_attr='mp', null=True)
    day = indexes.DateField(model_attr='day__date')

    def get_model(self):
        return Entry

    #def index_queryset(self):
    #    """Used when the entire index for model is updated."""
    #    return self.get_model().objects.filter(day__date__lte=datetime.date.today())

