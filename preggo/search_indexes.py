import datetime
from haystack import indexes
from preggo.models import *

class QuestionIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    #title = indexes.CharField(document=True, use_template=True)
    author = indexes.CharField(model_attr='user')
    upvotes = indexes.IntegerField(model_attr='upvotes')
    pub_date = indexes.DateTimeField(model_attr='pub_date')
    
    def get_model(self):
        return Question
    
    def index_queryset(self, using=None):
        "Used when the entire index for model is updated."
        return self.get_model().objects.filter(pub_date__lte=datetime.datetime.now())