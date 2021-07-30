from django.contrib import admin
from django.urls import path

import app1.views
import scanner.views
import activity.views

urlpatterns = [
    path('', scanner.views.scanner),
    path('admin/', admin.site.urls),
    path('login/', app1.views.loginPage, name="login"),
    path('logout/', app1.views.logoutUser, name="logout"),
    path('scanner/', scanner.views.scanner, name="scanner"),
    path('scanner/visitor/<str:barcode>', scanner.views.visitor, name="visitor"),
    path('filter/', activity.views.filteredVisits, name="filter"),
]
