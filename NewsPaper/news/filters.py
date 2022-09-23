from django_filters import FilterSet, ModelChoiceFilter, DateFilter, CharFilter
# from django_filters.widgets import DateRangeWidget
from .models import Post, Category
from django.forms import DateInput
from django.utils.translation import pgettext_lazy

class PostFilter(FilterSet):
    post_title = CharFilter(lookup_expr='icontains', label=pgettext_lazy('Search in the title', 'Search in the title of a news or article')) #'Поиск в заголовке новости или статьи'
    post_category = ModelChoiceFilter(queryset=Category.objects.all(), label=pgettext_lazy('Category', 'Category'), empty_label=pgettext_lazy('All categories', 'All categories'))
    post_create_datetime = DateFilter(field_name='post_create_datetime',
                                      lookup_expr='gt', label=pgettext_lazy('Article published after', 'Article published after'),
                                      widget=DateInput(attrs={'type': 'date'})
                                      )
    post_create_datetime.field.error_messages = {'invalid': pgettext_lazy('Input date format', 'Enter the date in the format DD.MM.YYYY. Example: 07.27.2022')}
    post_create_datetime.field.widget.attrs = {'placeholder': 'DD.MM.YYYY'}

    class Meta:
        fields = {'post_title': ['icontains'],
                  'post_category__post': ['exact'],
                  'post_create_datetime': ['gt'],
                  }

# class PostFilter(FilterSet):
#     date = DateFilter(field_name='post_create_datetime',
#                       lookup_expr='gte',
#                       label='Create after',
#                       widget=DateInput(attrs={'type': 'date'})
#                       )
#
#     title = CharFilter(lookup_expr='icontains')
#
#     category = ModelChoiceFilter(queryset=Category.objects.all())
#
#     date.field.error_messages = {'invalid': 'Enter date in format DD.MM.YYYY. Example: 24.07.2022'}
#     date.field.widget.attrs = {'placeholder': 'DD.MM.YYYY'}
#
#     class Meta:
#         model = Post
#         fields = ['date', 'title', 'category']
# category = ModelChoiceFilter(field_name='postcategory__post_category',
#                              queryset=Category.objects.all(),
#                              label='Категория',
#                              empty_label=''
#                              )
# DateCreation = DateTimeFilter(field_name='post_create_datetime',
#                               lookup_expr='date_lt',
#                               label='Дата создания',
#                               method=DateRangeWidget()
#                               )
