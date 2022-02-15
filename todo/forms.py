from django.forms import ModelForm
from .models import list

class todoform(ModelForm):
    class Meta:
        model = list
        fields = ['title','description','impo']

