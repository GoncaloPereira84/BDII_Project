from django.urls import path
from backend.views import(
    dashboard, 
    generic_list, 
    error404, 
    Sem_Acesso,
    delete_record, 
    edit_record, 
    edit_componente, 
    edit_equipamento,
    edit_utilizador,
    new_order, 
    save_encomenda, 
    new_prod,
    new_utilizador, 
    save_utilizador,     
    criar_mao_obra, 
    form_create_componente, 
    get_atributo_options, 
    create_componente, 
    create_equipamento, 
    new_prod_existente, 
    create_producao_equip_existente, 
    fn_populate_equipamento_comp_atrib,
    list_compra_FR_doc,
    receber_encomenda,
    import_componente_json,
    import_componente_html,
    edit_fornecedor,
    detalhes_fornecedor,
    detalhes_componente,
    detalhes_venda,
    export_encomendas,
    imprimir_export_encomendas,
    detalhes_compra,
    detalhes_equipamento,
    detalhes_producao,
    detalhes_utilizador,
    criar_fornecedor_view
)
from frontend.views import(
    index, 
    kanban,
    login_utilizador, 
    logout_utilizador, 
    equipamento_type, 
    detalhes_equipamento_list, 
    fulllogin,
    aplicarfiltros, 
    aplicarpreco,
    pesquisa_equipamento, 
    usercompras, 
    adicionar_ao_carrinho,
    get_carrinho_data,
    remover_do_carrinho,
    mudar_quantidade_carrinho,
    finalizarCarrinho,
    completeCarrinho
)

urlpatterns = [
    path("dashboard/", dashboard),
    path("order/create/", new_order),
    path("componente/import/", import_componente_html),
    path("equipamento/create/", new_prod),
    path("producao/create/", new_prod_existente),
    path("utilizador/create/", new_utilizador),
    path("utilizador/save/", save_utilizador), 
    path('save_utilizador/', save_utilizador, name='save_utilizador'),       
    path('utilizador/edit/<int:record_id>/', edit_utilizador, name='edit_utilizador'),     
    path("404/", error404),
    path("sem_acesso/", Sem_Acesso),    
    path("<str:table_name>/list/", generic_list, name='generic_list'),
    path("<str:table_name>/editar/<int:record_id>/", edit_record, name='edit_record'),
    path("", index),
    path('kanban/', kanban, name='kanban'),
    path('tipo/<int:tipo>', equipamento_type, name='equipamento_type'),
    path('delete_record/<str:table_name>/<int:record_id>/', delete_record, name='delete_record'),
    path('login/', login_utilizador, name='login'),
    path('logout/', logout_utilizador, name='logout'),
    path('componente/edit/<int:record_id>/', edit_componente, name='edit_componente'),
    path('equipamento/edit/<int:record_id>/', edit_equipamento, name='edit_equipamento'),
    path('fornecedor/edit/<int:record_id>/', edit_fornecedor, name='edit_fornecedor'),
    path('save_encomenda/', save_encomenda, name='save_encomenda'),
    path('criar_mao_obra/', criar_mao_obra, name='criar_mao_obra'),
    path('pesquisa_equipamento/', pesquisa_equipamento, name='pesquisa_equipamento'),
    path('equipamento/<int:equipamento_id>/', detalhes_equipamento_list, name='detalhes_equipamento_list'),
    path('mango/', fn_populate_equipamento_comp_atrib),
    path("componente/create", form_create_componente),
    path("get_atributo_options/", get_atributo_options, name='get_atributo_options'),
    path('create_componente/', create_componente, name='create_componente'),
    path('create_equipamento/', create_equipamento, name='create_equipamento'),
    path('create_producao_equip_existente/', create_producao_equip_existente, name='create_producao_equip_existente'),
    path('fulllogin/', fulllogin, name='login'),
    path("compra/list/fr", list_compra_FR_doc, name='list_compra_FR_doc'),
    path('receive_order/<int:record_id>/', receber_encomenda, name='receber_encomenda'),
    path("import_componente_json/", import_componente_json, name='import_componente_json'),
    path('aplicarfiltros/', aplicarfiltros, name='aplicarfiltros'),
    path('aplicarpreco/', aplicarpreco, name='aplicarpreco'),
    path('adicionar_ao_carrinho/', adicionar_ao_carrinho, name='adicionar_ao_carrinho'),
    path('get_carrinho_data/', get_carrinho_data, name='get_carrinho_data'),
    path('remover_do_carrinho/', remover_do_carrinho, name='remover_do_carrinho'),
    path('mudar_quantidade_carrinho/', mudar_quantidade_carrinho, name='mudar_quantidade_carrinho'),
    path('finalizarCarrinho/', finalizarCarrinho, name='finalizarCarrinho'),
    path('completeCarrinho/', completeCarrinho, name='completeCarrinho'),
    path('usercompras/', usercompras, name='usercompras'),  
    path('detalhes_fornecedor/<int:fornecedor_id>/', detalhes_fornecedor, name='detalhes_fornecedor'),
    path('detalhes_componente/<int:componente_id>/', detalhes_componente, name='detalhes_componente'),
    path('detalhes_venda/<int:venda_id>/', detalhes_venda, name='detalhes_venda'),
    path('detalhes_compra/<int:compra_id>/', detalhes_compra, name='detalhes_compra'),
    path('detalhes_equipamento/<int:equipamento_id>/', detalhes_equipamento, name='detalhes_equipamento'),
    path('detalhes_producao/<int:producao_id>/', detalhes_producao, name='detalhes_producao'),
    path('detalhes_utilizador/<int:utilizador_id>/', detalhes_utilizador, name='detalhes_utilizador'),
    path('export_encomendas/', export_encomendas, name='export_encomendas'),   
    path('imprimir_export_encomendas/', imprimir_export_encomendas, name='imprimir_export_encomendas'),
    path("fornecedor/create/", criar_fornecedor_view),
    path('criar_fornecedor_view/', criar_fornecedor_view, name='criar_fornecedor_view'),       
]
