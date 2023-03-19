from django.contrib import admin
from .models import Emprestimos, Lojas
# Register your models here.


"""class ListandoEmprestimos(admin.ModelAdmin):
    list_display = ( 'id', 'valor', 'status')
    list_display_links = ('id',)
    search_fields = ('credor', 'devedor', 'status')
    
class ListandoLojas(admin.ModelAdmin):
    list_display = ('nome',)
    list_display_links = ('nome',)
    search_fields = ('nome',)"""
    
admin.site.register(Emprestimos)
admin.site.register(Lojas)