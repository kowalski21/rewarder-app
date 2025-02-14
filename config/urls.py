"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from ninja import NinjaAPI, Redoc
from accounts.api import router as account_router
from voucher.api import router as voucher_router

api = NinjaAPI(docs=Redoc())
api.add_router("/accounts", account_router)
api.add_router("/voucher", voucher_router)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", api.urls),
]
