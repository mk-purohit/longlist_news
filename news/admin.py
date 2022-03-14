from django.contrib import admin

from .models import Newsitem, Key, Company, Postingsite

# Register your models here.

class NewsitemAdmin(admin.ModelAdmin):
   list_display = ('title', 'link', 'source', 'snippet', 'date_posted', 'quality_source')

class KeyAdmin(admin.ModelAdmin):
    list_display = ('name', 'status')
    
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'status')

class PostingsiteAdmin(admin.ModelAdmin):
    list_display = ('name', 'quality')

admin.site.register(Newsitem,NewsitemAdmin)
admin.site.register(Key, KeyAdmin)  
admin.site.register(Company,CompanyAdmin)
admin.site.register(Postingsite, PostingsiteAdmin)