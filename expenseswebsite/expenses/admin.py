from django.contrib import admin
from .models import Expense, Category

# Register your models here.


class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('amount','date','description','category','owner')
    search_fields = ['category']

admin.site.register(Expense,ExpenseAdmin)
admin.site.register(Category)