from django.contrib import admin
from .models import Visitor, Visit , PeakHours, Configuration

admin.site.register(Visitor)
admin.site.register(Visit)
admin.site.register(PeakHours)
admin.site.register(Configuration)