from django.views import generic
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect

from .forms import DiaryCreateForm

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
    success_url = reverse_lazy('diary:list')
    form_class = DiaryCreateForm


def DiaryDelete(request, diary_id):
    diary_pk = get_object_or_404(Diary, pk=diary_id)
    diary_pk.delete()
    return redirect('diary:list')


def DiaryAdd(request):
    category = Category.objects.get(pk=1)
    Diary.objects.create(title='新規作成', category=category)
    return redirect('diary:list')
   