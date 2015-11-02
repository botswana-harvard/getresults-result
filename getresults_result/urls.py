"""xx URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url
from getresults_result.views import (
    ResultSectionView, UnvalidatedResultsView, UnreleasedResultsView,
    ResultValidateView, ResultReleaseView, ResultReleaseHistoryView)

urlpatterns = [
    url(r'(?P<section_title>(unvalidated))/(?P<pk>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})/$', ResultValidateView.as_view(), name='validated_result_url'),
    url(r'(?P<section_title>(unreleased))/(?P<pk>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})/$', ResultReleaseView.as_view(), name='released_result_url'),
    url(r'unvalidated/$', UnvalidatedResultsView.as_view(), name='unvalidated_results_url'),
    url(r'unreleased/$', UnreleasedResultsView.as_view(), name='unreleased_results_url'),
    url(r'history/(?P<section_title>(released))/$', ResultReleaseHistoryView.as_view(), name='released_results_history_url'),
    url(r'', ResultSectionView.as_view(), name='result_home_url'),
]
