from django.contrib.auth import views as auth_views
from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('emprestimo/<int:id_emprestimo>', views.emprestimo, name='emprestimo'),
    path('lojas/<int:id_loja>', views.lojas, name='lojas'),
    path('cadastra_loja', views.cadastra_loja, name='cadastra_loja'),
    path('lancar_emprestimo', views.lancar_emprestimo, name='lancar_emprestimo'),
    path('editar_emprestimo/<int:id_emprestimo>', views.editar_emprestimo, name='editar_emprestimo'),
    path('pagar_emprestimo/<int:id_emprestimo>', views.pagar_emprestimo, name='pagar_emprestimo'),
    path('cancela_emprestimo/<int:id_emprestimo>', views.cancela_emprestimo, name='cancela_emprestimo')
]