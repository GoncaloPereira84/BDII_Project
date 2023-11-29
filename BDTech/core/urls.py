from django.contrib import admin
from django.urls import path
from backend.views import utilizador_list, fornecedor_list, dashboard

urlpatterns = [
    path('', dashboard),
    # --utilizador--
    path('utilizadores/list/', utilizador_list, name='utilizador_list'),
    # --fornecedor--
    path('fornecedores/list/', fornecedor_list, name='fornecedor_list'),
]

