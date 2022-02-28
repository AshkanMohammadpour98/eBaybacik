from django.contrib import admin
from .models import List, ProposedPrice, Comment, Category, Bid


class ListAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'Initial_price')
    list_filter = ('title', 'status')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug':('title',)}



admin.site.register(List, ListAdmin)
admin.site.register(ProposedPrice)
admin.site.register(Comment)
admin.site.register(Category)
admin.site.register(Bid)