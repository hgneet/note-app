from django.views import generic
from django.http import Http404
from django.utils import timezone
from django.urls import reverse_lazy
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_POST

from .forms import DiarySearchForm, DiaryCreateForm

from .models import Diary, Category


class ArchiveListMixin:
    model = Diary
    paginate_by = 12
    date_field = 'created_at'
    template_name = 'diary/diary_list.html'
    allow_empty = True
    make_object_list = True

    
class DiaryListMixin(generic.base.ContextMixin):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['diary_list'] = Diary.objects.all().order_by('created_at').reverse()
        return context
    
    
class DiaryList(DiaryListMixin, ArchiveListMixin, generic.ArchiveIndexView):

    def get_queryset(self):
        return super().get_queryset().select_related('category')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['heading'] = '最近の日記'
        return context


    
class DiaryDetail(DiaryListMixin, generic.UpdateView):
    template_name = 'diary/diary_detail.html'
    model = Diary
    success_url = reverse_lazy('diary:diary_create_complete')
    form_class = DiaryCreateForm


class DiaryCategoryList(ArchiveListMixin, generic.ArchiveIndexView):

    def get_queryset(self):
        self.category = category = get_object_or_404(Category, pk=self.kwargs['pk'])
        return super().get_queryset().filter(category=category).select_related('category')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['heading'] = '「{}」 カテゴリの日記'.format(self.category.name)
        return context
    

class DiaryYearList(ArchiveListMixin, generic.YearArchiveView):

    def get_queryset(self):
        return super().get_queryset().select_related('category')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['heading'] = '{}年の日記'.format(self.kwargs['year'])
        return context


class DiaryMonthList(ArchiveListMixin, generic.MonthArchiveView):
    month_format = '%m'

    def get_queryset(self):
        return super().get_queryset().select_related('category')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['heading'] = '{}年{}月の日記'.format(self.kwargs['year'], self.kwargs['month'])
        return context
    

class DiarySearchList(ArchiveListMixin, generic.ArchiveIndexView):

    def get_queryset(self):
        queryset = super().get_queryset()
        self.request.form = form = DiarySearchForm(self.request.GET)
        form.is_valid()
        self.key_word = key_word = form.cleaned_data['key_word']
        if key_word:
            queryset = queryset.filter(Q(title__icontains=key_word) | Q(text__icontains=key_word))
        return queryset.select_related('category')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['heading'] = '「{}」 の検索結果'.format(self.key_word)
        return context
    

class DiaryNote(generic.DetailView):
    template_name = 'diary/note.html'
    model = Diary

    def get_object(self, queryset=None):
        diary = super().get_object()
        if diary.created_at <= timezone.now():
            return diary
        raise Http404


class DiaryCreateView(generic.CreateView):
    template_name = 'diary/diary_create.html'
    form_class = DiaryCreateForm
    success_url = reverse_lazy('diary:diary_create_complete')


class DiaryCreateCompleteView(generic.TemplateView):
    template_name = 'diary/diary_create_complete.html'

# @require_POST
def DiaryDelete(request, diary_id):
    diary_pk = get_object_or_404(Diary, pk=diary_id)
    diary_pk.delete()
    return redirect('diary:list')

# @require_POST
def DiaryAdd(request):
    category = Category.objects.get(pk=1)
    Diary.objects.create(title='新規作成', category=category)
    return redirect('diary:list')
   