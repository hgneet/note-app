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