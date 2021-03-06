import django_filters

from member_profile.models import Profile, Busyness, Schedule
from vacancy.models import Vacancy


class VacancyFilter(django_filters.FilterSet):
    salary_from = django_filters.NumberFilter(method='salary_filter')

    def salary_filter(self, queryset, name, value):
        return queryset.filter(salary_from__gte=value)

    class Meta:
        model = Vacancy
        fields = ["specialisations", "keywords", "salary_from", "busyness", "schedule", ]


class CPFilter(django_filters.FilterSet):
    salary_from = django_filters.NumberFilter(method='salary_filter')
    busyness = django_filters.ModelChoiceFilter(queryset=Busyness.objects.all(), method='busyness_filter')
    schedule = django_filters.ModelChoiceFilter(queryset=Schedule.objects.all(), method='schedule_filter')

    def busyness_filter(self, queryset, name, value):
        return queryset.filter(position__busyness=value)

    def schedule_filter(self, queryset, name, value):
        return queryset.filter(position__schedule=value)

    def salary_filter(self, queryset, name, value):
        return queryset.filter(position__salary_from__gte=value)

    class Meta:
        model = Profile
        fields = ["specialisations", "keywords", "position__salary_from", "position__busyness", "position__schedule", ]
