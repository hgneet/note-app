from django import forms
from .models import Diary


class DiarySearchForm(forms.Form):
    """検索フォーム。"""
    key_word = forms.CharField(
        label='検索キーワード',
        required=False,
    )

class DiaryCreateForm(forms.ModelForm):
    class Meta:
        model = Diary
        fields = ('title', 'text', 'category')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs = {'placeholder': 'Title', 'class': 'input-title'}
        self.fields['text'].widget.attrs = {'placeholder': 'Text',  'class': 'input-text'}
        self.fields['category'].widget.attrs = {'placeholder': 'Category',  'class': 'input-category'}