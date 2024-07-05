from django.forms import ModelForm, CharField, TextInput, Textarea
from .models import Author, Tag, Quote


class AuthorForm(ModelForm):
    
    fullname = CharField(
        min_length=3, 
        max_length=50, 
        required=True, 
        widget=TextInput(),
    )
    
    born_date = CharField(
        max_length=50,
        required=False,
        widget=TextInput(),
    )
    
    born_location = CharField(
        max_length=150,
        required=False,
        widget=TextInput(),
    )
    
    description = CharField(
        required=False,
        widget=Textarea()
    )
    
    class Meta:
        model = Author
        fields = ['fullname', 'born_date', 'born_location', 'description']


class TagForm(ModelForm):

    name = CharField(
        max_length = 50,
        required = True,
        widget = TextInput()
    )

    class Meta:
        model = Tag
        fields = ['name']


class QuoteForm(ModelForm):

    quote = CharField(
        required=True,
        widget=Textarea(
            attrs={"placeholder": "enter quote"}
        ),
    )

    class Meta:
        model = Quote
        fields = ['quote']
        exclude = ['author', 'tags']