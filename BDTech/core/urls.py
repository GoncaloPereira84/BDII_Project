from django.urls import path
from backend.views import dashboard, generic_list, error404, delete_record, edit_record, edit_componente, new_order, save_encomenda, new_prod, criar_mao_obra, mango, form_create_componente, get_atributo_options, create_componente
from frontend.views import index, kanban, login_utilizador, logout_utilizador, equipamento_type, detalhes_equipamento

urlpatterns = [
    path("dashboard/", dashboard),
    path("order/create/", new_order),
    path("equipamento/create/", new_prod),
    path("404/", error404),
    path("<str:table_name>/list/", generic_list, name='generic_list'),
    path("<str:table_name>/editar/<int:record_id>/", edit_record, name='edit_record'),
    path("", index),
    path('kanban/', kanban, name='kanban'),
    path('tipo/<int:tipo>', equipamento_type, name='equipamento_type'),
    path('delete_record/<str:table_name>/<int:record_id>/', delete_record, name='delete_record'),
    path('login/', login_utilizador, name='login'),
    path('logout/', logout_utilizador, name='logout'),
    path('componente/edit/<int:record_id>/', edit_componente, name='edit_componente'),
    path('save_encomenda/', save_encomenda, name='save_encomenda'),
    path('criar_mao_obra/', criar_mao_obra, name='criar_mao_obra'),
    path('equipamento/<int:equipamento_id>/', detalhes_equipamento, name='detalhes_equipamento'),
    path('mango/', mango),
    path("componente/create", form_create_componente),
    path("get_atributo_options/", get_atributo_options, name='get_atributo_options'),
    path('create_componente/', create_componente, name='create_componente'),
]
