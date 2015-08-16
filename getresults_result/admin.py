from django.contrib import admin

from getresults.admin import admin_site

from .models import Result, ResultItem


class ResultItemInline(admin.TabularInline):
    model = ResultItem
    extra = 0


class ResultItemAdmin(admin.ModelAdmin):
    date_hierarchy = 'result_datetime'
    list_display = ('result', 'utestid', 'value', 'quantifier', 'result_datetime')
    search_fields = ('result__result_identifier', 'result__order__panel__name',
                     'result_datetime')
admin_site.register(ResultItem, ResultItemAdmin)


class ResultInline(admin.TabularInline):
    model = Result
    extra = 0


class ResultAdmin(admin.ModelAdmin):
    date_hierarchy = 'collection_datetime'
    list_display = ('result_identifier', 'collection_datetime', 'order',
                    'operator', 'analyzer_name')
    search_fields = ('result_identifier', 'analyzer_name', 'order__order_identifier')
    inlines = [ResultItemInline]
admin_site.register(Result, ResultAdmin)
