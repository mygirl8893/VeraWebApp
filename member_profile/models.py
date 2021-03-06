from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _

from google_address.models import Address

SEX_CHOICES = (
    ('male', 'male'),
    ('female', 'female'),
)

YEARS = [(i, i) for i in range(1950, now().year + 1)][::-1]

DAYS = [(i, i) for i in range(1, 32)]

MONTHS = (
    (1, _('january')),
    (2, _('february')),
    (3, _('march')),
    (4, _('april')),
    (5, _('may')),
    (6, _('june')),
    (7, _('july')),
    (8, _('august')),
    (9, _('september')),
    (10, _('october')),
    (11, _('november')),
    (12, _('december')),
)

WEIGHTS = (
    (0, _('Minor')),
    (1, _('Medium')),
    (2, _('Major')),
)

LANGUAGE_LEVELS = (
    ('NOT', _("Notion")),
    ('BAS', _('Basic')),
    ('ADV', _('Advanced')),
    ('PRO', _('Professional')),
    ('BIL', _('Bilingual')),
)

ADDITIONAL_CHOICES = (
    ('COURSE', 'Course'),
    ('TRAINING', 'Training'),
    ('CONFERENCE', 'Conference'),
)


def current_year():
    return now().year


def current_month():
    return now().month


class Busyness(models.Model):
    title = models.CharField(max_length=127)

    def __str__(self):
        return self.title


class Schedule(models.Model):
    title = models.CharField(max_length=127)

    def __str__(self):
        return self.title


class Profile(models.Model):
    member = models.OneToOneField('users.Member',
                                  on_delete=models.CASCADE,
                                  related_name='profile')
    photo = models.ImageField(null=True,
                              blank=True)
    birth_date = models.DateField(blank=True,
                                  null=True,
                                  default=None)
    sex = models.CharField(max_length=20,
                           choices=SEX_CHOICES)
    address = models.CharField(max_length=255,
                               blank=True,
                               null=True)
    relocation = models.NullBooleanField(default=None)
    official_journey = models.NullBooleanField(default=None)
    specialisations = models.ManyToManyField('jobboard.Specialisation',
                                             blank=True)
    keywords = models.ManyToManyField('jobboard.Keyword',
                                      blank=True)
    level = models.ForeignKey('EducationLevel',
                              on_delete=models.SET_NULL,
                              null=True,
                              blank=True)
    enabled = models.NullBooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return 'Profile: {}'.format(self.member.full_name)

    def get_absolute_url(self):
        return reverse('member_profile', kwargs={'username': self.member.username})

    def get_statistic_url(self):
        return reverse('cvstatistic', kwargs={'pk': self.pk})

    @property
    def title(self):
        return self.position.title if hasattr(self, 'position') else self.member.username

    @property
    def user_field_name(self):
        return 'member'


class Position(models.Model):
    profile = models.OneToOneField(Profile,
                                   on_delete=models.CASCADE,
                                   null=False,
                                   blank=False,
                                   related_name='position')
    title = models.CharField(max_length=50, blank=False, null=False)
    busyness = models.ManyToManyField(Busyness)
    schedule = models.ManyToManyField(Schedule)
    salary_from = models.PositiveIntegerField(default=0, blank=False, null=False)
    career_start = models.BooleanField(default=False)
    description = models.TextField(blank=False, null=False)

    def __str__(self):
        return self.title

    @staticmethod
    def get_absolute_url():
        return reverse('profile')


class Experience(models.Model):
    profile = models.ForeignKey(Profile,
                                on_delete=models.CASCADE,
                                related_name='experience')
    start_year = models.IntegerField(choices=YEARS,
                                     default=current_year,
                                     verbose_name=_("start year"))
    start_month = models.IntegerField(choices=MONTHS,
                                      default=current_month,
                                      verbose_name=_("start month"))
    still = models.BooleanField(default=False,
                                verbose_name=_("still in office"))
    end_year = models.IntegerField(choices=YEARS,
                                   null=True,
                                   blank=True,
                                   verbose_name=_("end year"))
    end_month = models.IntegerField(choices=MONTHS,
                                    null=True,
                                    blank=True,
                                    verbose_name=_("end month"))
    organization = models.CharField(max_length=255,
                                    blank=False,
                                    null=False)
    city = models.CharField(max_length=127,
                            blank=False,
                            null=False)
    position = models.CharField(max_length=127)
    description = models.TextField(null=True,
                                   blank=True,
                                   default=None)

    def __str__(self):
        return 'Experience {}'.format(self.position)

    def get_absolute_url(self):
        return reverse('profile')


class EducationLevel(models.Model):
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=127)

    def __str__(self):
        return self.title


class Education(models.Model):
    profile = models.ForeignKey(Profile,
                                on_delete=models.CASCADE,
                                related_name='education',
                                blank=False,
                                null=False)
    institute = models.CharField(max_length=127,
                                 blank=True,
                                 null=True)
    faculty = models.CharField(max_length=127,
                               blank=True,
                               null=True)
    profession = models.CharField(max_length=127,
                                  blank=True,
                                  null=True)
    start = models.DateField()
    end = models.DateField()

    def __str__(self):
        return self.institute or '-'

    @staticmethod
    def get_absolute_url():
        return reverse('profile')


class Language(models.Model):
    name = models.CharField(max_length=255, primary_key=True, unique=True, verbose_name=_("name"))
    code = models.CharField(max_length=5, unique=True, verbose_name=_("language code"))
    native_name = models.TextField(max_length=2000, blank=True, verbose_name=_("native name"))

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class LanguageItem(models.Model):
    profile = models.ForeignKey(Profile,
                                related_name='languages',
                                on_delete=models.CASCADE)
    language = models.ForeignKey(Language,
                                 'name',
                                 related_name='items')
    level = models.CharField(max_length=5,
                             choices=LANGUAGE_LEVELS,
                             default=LANGUAGE_LEVELS[0][0],
                             verbose_name=_('level'))

    class Meta:
        unique_together = ('language', 'profile')

    def __str__(self):
        return self.language.name


class Country(models.Model):
    name = models.CharField(max_length=127,
                            null=False,
                            blank=False)

    def __str__(self):
        return self.name


class Citizenship(models.Model):
    profile = models.ForeignKey(Profile,
                                on_delete=models.CASCADE,
                                null=False,
                                blank=False,
                                related_name='citizenship')
    country = models.ForeignKey(Country,
                                on_delete=models.CASCADE,
                                null=False,
                                blank=False)

    def __str__(self):
        return '{}: {}'.format(self.profile, self.country.name)


class WorkPermit(models.Model):
    profile = models.ForeignKey(Profile,
                                on_delete=models.CASCADE,
                                null=False,
                                blank=False,
                                related_name='work_permit')
    country = models.ForeignKey(Country,
                                on_delete=models.CASCADE,
                                null=False,
                                blank=False)

    def __str__(self):
        return '{}: {}'.format(self.profile, self.country.name)


class Achievement(models.Model):
    profile = models.ForeignKey(Profile,
                                related_name='achievements',
                                on_delete=models.CASCADE)
    title = models.CharField(max_length=255,
                             blank=False,
                             null=False)
    text = models.TextField(blank=False,
                            null=False)

    def __str__(self):
        return '{} achievement'.format(self.profile)


class AdditionalEducation(models.Model):
    profile = models.ForeignKey(Profile,
                                on_delete=models.CASCADE,
                                related_name='additional_education',
                                blank=False,
                                null=False)
    education_type = models.CharField(max_length=20,
                                      choices=ADDITIONAL_CHOICES,
                                      null=False,
                                      blank=False)
    institute = models.CharField(max_length=127,
                                 blank=True,
                                 null=True)
    profession = models.CharField(max_length=127,
                                  blank=True,
                                  null=True)
    start = models.DateField()
    end = models.DateField()
    has_certificate = models.BooleanField(default=False)

    def __str__(self):
        return '{} {}'.format(self.profile.member.username, self.education_type)
