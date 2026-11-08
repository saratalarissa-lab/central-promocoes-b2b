import streamlit as st
import pandas as pd
import os
from datetime import datetime, timedelta

# Configuração da página
st.set_page_config(
    page_title="Central Exclusiva de Promoções",
    page_icon="🛒",
    layout="wide"
)

# Estilização visual limpa e profissional original
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        font-weight: bold;
        background-color: #ff4b4b;
        color: white;
    }
    .stButton>button:hover {
        background-color: #e03e3e;
        color: white;
    }
    .product-card {
        background-color: white;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        margin-bottom: 20px;
        border: 1px solid #eaeaea;
        text-align: center;
    }
    .cart-box {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 12px;
        border: 2px solid #ff4b4b;
        margin-top: 20px;
    }
    .promo-banner {
        background-color: #fff3cd;
        color: #856404;
        padding: 12px;
        border-radius: 8px;
        border: 1px solid #ffeeba;
        text-align: center;
        font-weight: bold;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# ----------------- INICIALIZAÇÃO DE DADOS (Permanentes) -----------------
if "produtos" not in st.session_state:
    st.session_state["produtos"] = [
        {
            "id": 1, 
            "cod": "VIP-920002", 
            "nome": "PNEU VIPAL ST300 TRAS TITAN", 
            "categoria": "Pneus", 
            "marca": "Vipal", 
            "modelo": "Titan 150 / Fan 150", 
            "preco": 195.00, 
            "foto": "https://new-vipal-prd.s3.sa-east-1.amazonaws.com/product-images/product-4447-2_600x600.png"
        },
        {
            "id": 2, 
            "cod": "VIP-920001", 
            "nome": "PNEU VIPAL ST300 DIANT 275/18", 
            "categoria": "Pneus", 
            "marca": "Vipal", 
            "modelo": "Titan 125 / YBR 125", 
            "preco": 174.00, 
            "foto": "https://new-vipal-prd.s3.sa-east-1.amazonaws.com/product-images/product-4447-2_600x600.png"
        }
    ]

if "carrinho" not in st.session_state:
    st.session_state["carrinho"] = {}

if "pedido_enviado" not in st.session_state:
    st.session_state["pedido_enviado"] = False

if "nome_cliente_atual" not in st.session_state:
    st.session_state["nome_cliente_atual"] = ""

if "ultimo_pedido_gerado" not in st.session_state:
    st.session_state["ultimo_pedido_gerado"] = None

if "pedidos_recebidos" not in st.session_state:
    st.session_state["pedidos_recebidos"] = []

if "prazo_fim_promo" not in st.session_state:
    st.session_state["prazo_fim_promo"] = datetime.now() + timedelta(days=1)

if "senha_cliente" not in st.session_state:
    st.session_state["senha_cliente"] = "promo2026"

if "senha_admin" not in st.session_state:
    st.session_state["senha_admin"] = "admin123"

# ----------------- NAVEGAÇÃO LATERAL -----------------
st.sidebar.markdown("## 🧭 Navegação")
perfil = st.sidebar.radio("Escolha o perfil:", ["Área do Cliente", "Painel Administrativo (Admin)"])

# -------------------------------------------------------------------------
# ÁREA DO CLIENTE
# -------------------------------------------------------------------------
if perfil == "Área do Cliente":
    st.title("🛒 Central Exclusiva de Promoções")
    
    st.markdown("""
        <div class="promo-banner">
            ⚡ ATENÇÃO: Promoções válidas por TEMPO LIMITADO e enquanto durar o estoque!
        </div>
    """, unsafe_allow_html=True)
    
    # Contador Regressivo
    agora = datetime.now()
    diferenca = st.session_state["prazo_fim_promo"] - agora
    
    if diferenca.total_seconds() > 0:
        horas = int(diferenca.total_seconds() // 3600)
        minutos = int((diferenca.total_seconds() % 3600) // 60)
        segundos = int(diferenca.total_seconds() % 60)
        
        data_hoje_str = agora.strftime('%d/%m/%Y')
        st.markdown(f"**DATA DE HOJE:** {data_hoje_str} | **OFERTA TERMINA EM:** **{horas:02d}h {minutos:02d}m {segundos:02d}s**")
    else:
        st.error("⚠️ A promoção foi encerrada!")

    senha_digitada = st.text_input("Senha de Acesso:", type="password")
    
    if senha_digitada:
        if senha_digitada == st.session_state["senha_cliente"]:
            st.success("Acesso liberado!")
            
            if st.session_state["pedido_enviado"] and st.session_state["ultimo_pedido_gerado"]:
                p_info = st.session_state["ultimo_pedido_gerado"]
                st.success(f"🎉 Pedido finalizado com sucesso em nome de **{p_info['cliente']}** em **{p_info['data_hora']}**!")
                
                st.markdown("### 📋 Resumo do Pedido Realizado:")
                st.table(pd.DataFrame(p_info["itens"]))
                st.markdown(f"### Valor Total: R$ {p_info['total']:.2f}")
                
                espelho_texto = f"""=== ESPELHO DO PEDIDO - CENTRAL DE PROMOÇÕES ===
Número do Pedido: #{p_info['id_pedido']}
Data e Hora: {p_info['data_hora']}
Cliente / Oficina: {p_info['cliente']}
--------------------------------------------------
ITENS SOLICITADOS:
"""
                for item in p_info["itens"]:
                    espelho_texto += f"- [{item['Cód']}] {item['Nome']} | Qtd: {item['Qtd']} | Preço Unit: R$ {item['Preço Unit']:.2f} | Subtotal: R$ {item['Subtotal']:.2f}\n"
                
                espelho_texto += f"--------------------------------------------------\nVALOR TOTAL DO PEDIDO: R$ {p_info['total']:.2f}\n=================================================="

                st.download_button(
                    label="📥 Baixar Espelho do Pedido (Salvar no Celular ou Notebook)",
                    data=espelho_texto,
                    file_name=f"pedido_{p_info['id_pedido']}_{p_info['cliente'].replace(' ', '_')}.txt",
                    mime="text/plain"
                )
                
                st.divider()
                if st.button("🔄 Fazer Novo Pedido (Comprar Novamente)"):
                    st.session_state["carrinho"] = {}
                    st.session_state["pedido_enviado"] = False
                    st.session_state["nome_cliente_atual"] = ""
                    st.session_state["ultimo_pedido_gerado"] = None
                    st.rerun()
                
            else:
                produtos = st.session_state["produtos"]
                if not produtos:
                    st.info("Nenhum produto cadastrado no momento.")
                else:
                    st.markdown("---")
                    busca_cliente = st.text_input("🔎 Buscar produto por código ou nome")
                    
                    col_f1, col_f2, col_f3 = st.columns(3)
                    categorias_disponiveis = ["Todas"] + sorted(list(set(p.get('categoria', 'Geral') for p in produtos)))
                    marcas_disponiveis = ["Todas"] + sorted(list(set(p.get('marca', 'Diversas') for p in produtos)))
                    modelos_disponiveis = ["Todos"] + sorted(list(set(p.get('modelo', 'Geral') for p in produtos)))
                    
                    with col_f1:
                        filtro_cat = st.selectbox("Categoria", categorias_disponiveis)
                    with col_f2:
                        filtro_marca = st.selectbox("Marca", marcas_disponiveis)
                    with col_f3:
                        filtro_modelo = st.selectbox("Modelo / Aplicação", modelos_disponiveis)
                    
                    produtos_filtrados = produtos
                    if busca_cliente.strip():
                        termo = busca_cliente.lower()
                        produtos_filtrados = [
                            p for p in produtos_filtrados 
                            if termo in str(p.get('cod', '')).lower() or termo in p['nome'].lower()
                        ]
                    if filtro_cat != "Todas":
                        produtos_filtrados = [p for p in produtos_filtrados if p.get('categoria', 'Geral') == filtro_cat]
                    if filtro_marca != "Todas":
                        produtos_filtrados = [p for p in produtos_filtrados if p.get('marca', 'Diversas') == filtro_marca]
                    if filtro_modelo != "Todos":
                        produtos_filtrados = [p for p in produtos_filtrados if p.get('modelo', 'Geral') == filtro_modelo]
                    
                    st.markdown(f"### Produtos Disponíveis ({len(produtos_filtrados)})")
                    
                    if not produtos_filtrados:
                        st.warning("Nenhum produto encontrado com os filtros selecionados.")
                    else:
                        num_cols = 3
                        grid_cols = st.columns(num_cols)
                        
                        for index, prod in enumerate(produtos_filtrados):
                            col = grid_cols[index % num_cols]
                            with col:
                                cod_exibicao = prod.get('cod', 'N/D')
                                modelo_aplicacao = prod.get('modelo', 'Geral')
                                
                                st.markdown(f"""
                                    <div class="product-card">
                                        <div style="text-align: left;">
                                            <span style="font-size: 11px; font-weight: bold; color: #6c757d; background-color: #e9ecef; padding: 2px 6px; border-radius: 4px;">Cód: {cod_exibicao}</span>
                                        </div>
                                        <div style="text-align: center; margin: 10px 0;">
                                            <img src="{prod['foto']}" width="100" style="border-radius: 8px; object-fit: cover; height: 100px;" onerror="this.onerror=null;this.src='https://via.placeholder.com/150';">
                                        </div>
                                        <h4 style="margin: 5px 0; color: #333; font-size: 14px; font-weight: 700; height: 38px; overflow: hidden;">{prod['nome']}</h4>
                                        <p style="margin: 0 0 5px 0; color: #6c757d; font-size: 11px;"><b>Aplicação:</b> {modelo_aplicacao}</p>
                                        <div style="font-size: 18px; color: #ff4b4b; font-weight: 800; margin: 8px 0;">R$ {prod['preco']:.2f}</div>
                                    </div>
                                """, unsafe_allow_html=True)
                                
                                qtd_atual = st.session_state["carrinho"].get(prod['id'], 0)
                                nova_qtd = st.number_input(f"Qtd p/ {cod_exibicao}", min_value=0, max_value=1000, value=qtd_atual, key=f"qtd_{prod['id']}")
                                
                                if nova_qtd > 0:
                                    st.session_state["carrinho"][prod['id']] = nova_qtd
                                elif prod['id'] in st.session_state["carrinho"]:
                                    del st.session_state["carrinho"][prod['id']]

                    st.divider()
                    
                    st.markdown("### 🛍️ Seu Carrinho")
                    if not st.session_state["carrinho"]:
                        st.info("O carrinho está vazio. Selecione a quantidade nos itens acima.")
                    else:
                        valor_total = 0.0
                        dados_carrinho = []
                        
                        for prod_id, quantidade in st.session_state["carrinho"].items():
                            produto_info = next((p for p in produtos if p['id'] == prod_id), None)
                            if produto_info:
                                subtotal = produto_info['preco'] * quantidade
                                valor_total += subtotal
                                dados_carrinho.append({
                                    "Cód": produto_info.get('cod', 'N/D'),
                                    "Produto": produto_info['nome'],
                                    "Preço Unitário": f"R$ {produto_info['preco']:.2f}",
                                    "Quantidade": quantidade,
                                    "Subtotal": f"R$ {subtotal:.2f}"
                                })
                        
                        st.table(pd.DataFrame(dados_carrinho))
                        
                        st.markdown(f"""
                            <div class="cart-box">
                                <h3 style="color: #333; margin: 0;">Valor Total Atual: <span style="color: #ff4b4b;">R$ {valor_total:.2f}</span></h3>
                            </div>
                        """, unsafe_allow_html=True)
                        
                        st.markdown("### 👤 Identificação do Cliente")
                        nome_cliente_input = st.text_input("Digite seu Nome ou Nome da Oficina para finalizar:", value=st.session_state["nome_cliente_atual"])
                        
                        if st.button("Finalizar Pedido Oficial"):
                            if not nome_cliente_input.strip():
                                st.error("Por favor, digite seu nome ou o nome da sua oficina para identificar o pedido.")
                            else:
                                st.session_state["nome_cliente_atual"] = nome_cliente_input
                                data_hora_str = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                                data_apenas_str = datetime.now().strftime("%d/%m/%Y")
                                
                                pedido_itens = []
                                for prod_id, quantidade in st.session_state["carrinho"].items():
                                    p_info = next((p for p in produtos if p['id'] == prod_id), None)
                                    if p_info:
                                        pedido_itens.append({
                                            "Cód": p_info.get('cod', 'N/D'),
                                            "Nome": p_info['nome'],
                                            "Preço Unit": p_info['preco'],
                                            "Qtd": quantidade,
                                            "Subtotal": p_info['preco'] * quantidade
                                        })
                                
                                novo_pedido = {
                                    "id_pedido": len(st.session_state["pedidos_recebidos"]) + 1,
                                    "data": data_apenas_str,
                                    "data_hora": data_hora_str,
                                    "cliente": nome_cliente_input,
                                    "itens": pedido_itens,
                                    "total": valor_total
                                }
                                
                                st.session_state["pedidos_recebidos"].append(novo_pedido)
                                st.session_state["ultimo_pedido_gerado"] = novo_pedido
                                st.session_state["pedido_enviado"] = True
                                st.balloons()
                                st.success("Pedido enviado com sucesso!")
                                st.rerun()
        else:
            st.error("Senha incorreta. Verifique com o administrador.")

# ----------------- PAINEL ADMINISTRATIVO -----------------
else:
    st.title("🛠️ Painel Administrativo")
    st.markdown("Gerencie produtos, defina o tempo da promoção, consulte pedidos e controle acessos.")
    
    senha_adm_digitada = st.text_input("Senha do Administrador:", type="password")
    
    if senha_adm_digitada:
        if senha_adm_digitada == st.session_state["senha_admin"]:
            st.success("Painel Administrativo Autorizado!")
            
            abas_admin = st.tabs(["📅 Agenda de Pedidos", "⏳ Prazo / Validade", "📦 Produtos", "📥 Importar Excel", "✏️ Editar", "🔑 Senhas"])
            
            # Aba 0: Agenda de Pedidos
            with abas_admin[0]:
                st.subheader("📅 Agenda e Histórico de Vendas por Data")
                if not st.session_state["pedidos_recebidos"]:
                    st.info("Nenhum pedido registrado no sistema.")
                else:
                    datas_disponiveis = sorted(list(set(p["data"] for p in st.session_state["pedidos_recebidos"])), reverse=True)
                    data_hoje_str = datetime.now().strftime("%d/%m/%Y")
                    
                    if data_hoje_str not in datas_disponiveis:
                        datas_disponiveis.insert(0, data_hoje_str)
                    
                    data_selecionada = st.selectbox("Selecione a Data da Venda (Agenda):", datas_disponiveis)
                    
                    pedidos_filtrados_data = [p for p in st.session_state["pedidos_recebidos"] if p.get("data") == data_selecionada]
                    
                    st.markdown(f"### Exibindo vendas para o dia: **{data_selecionada}** ({len(pedidos_filtrados_data)} pedido(s))")
                    
                    if not pedidos_filtrados_data:
                        st.info(f"Nenhum pedido registrado para a data {data_selecionada}.")
                    else:
                        for ped in pedidos_filtrados_data:
                            with st.expander(f"📦 Pedido #{ped['id_pedido']} | Hora: {ped['data_hora']} | Cliente: **{ped['cliente']}** — Total: R$ {ped['total']:.2f}"):
                                st.markdown(f"**Data e Hora do Pedido:** {ped['data_hora']}")
                                st.markdown(f"**Cliente / Oficina:** {ped['cliente']}")
                                df_ped = pd.DataFrame(ped["itens"])
                                st.table(df_ped)
                                st.markdown(f"**Total Geral:** R$ {ped['total']:.2f}")
                
                st.divider()
                if st.button("Limpar Todo o Histórico de Pedidos"):
                    st.session_state["pedidos_recebidos"] = []
                    st.success("Histórico limpo!")
                    st.rerun()

            # Aba 1: Prazo e Validade da Promoção
            with abas_admin[1]:
                st.subheader("Configurar Validade da Promoção")
                data_atual_val = st.session_state["prazo_fim_promo"].date()
                hora_atual_val = st.session_state["prazo_fim_promo"].time()
                
                nova_data = st.date_input("Data de Término", value=data_atual_val)
                nova_hora = st.time_input("Horário de Término", value=hora_atual_val)
                
                if st.button("Salvar Novo Prazo"):
                    st.session_state["prazo_fim_promo"] = datetime.combine(nova_data, nova_hora)
                    st.success("Prazo da promoção atualizado com sucesso!")

            # Aba 2: Cadastro Manual e Exclusão
            with abas_admin[2]:
                st.subheader("Cadastrar Produto (Permanente)")
                with st.form("form_cad_man", clear_on_submit=True):
                    c_cod = st.text_input("Código do Produto")
                    c_nome = st.text_input("Nome do Produto")
                    c_cat = st.text_input("Categoria", value="Geral")
                    c_marca = st.text_input("Marca", value="Diversas")
                    c_mod = st.text_input("Modelo / Aplicação", value="Universal")
                    c_preco = st.number_input("Preço Promocional (R$)", min_value=0.0, format="%.2f")
                    c_foto = st.text_input("URL da Foto", value="https://new-vipal-prd.s3.sa-east-1.amazonaws.com/product-images/product-4447-2_600x600.png")
                    
                    if st.form_submit_button("Cadastrar"):
                        if c_nome.strip():
                            novo_id = max([p["id"] for p in st.session_state["produtos"]], default=0) + 1
                            st.session_state["produtos"].append({
                                "id": novo_id,
                                "cod": c_cod if c_cod else f"COD-{novo_id}",
                                "nome": c_nome,
                                "categoria": c_cat,
                                "marca": c_marca,
                                "modelo": c_mod,
                                "preco": c_preco,
                                "foto": c_foto
                            })
                            st.success("Produto cadastrado com sucesso!")
                        else:
                            st.error("Informe o nome do produto.")
                
                st.divider()
                st.subheader("Gerenciar Produtos / Excluir")
                for p in st.session_state["produtos"]:
                    cols = st.columns([4, 1, 1])
                    cols[0].markdown(f"**[{p.get('cod','N/D')}]** {p['nome']} - R$ {p['preco']:.2f}")
                    if cols[2].button("Excluir", key=f"del_prod_{p['id']}"):
                        st.session_state["produtos"] = [item for item in st.session_state["produtos"] if item["id"] != p["id"]]
                        st.rerun()

            # Aba 3: Importar do Excel
            with abas_admin[3]:
                st.subheader("Importar Planilhas Excel")
                up_files = st.file_uploader("Carregar planilhas", type=["xlsx", "xls"], accept_multiple_files=True)
                if up_files:
                    for arq in up_files:
                        st.markdown(f"### Arquivo: {arq.name}")
                        try:
                            df_ex = pd.read_excel(arq)
                            with st.form(f"form_ex_{arq.name}"):
                                itens_add = []
                                for idx, row in df_ex.iterrows():
                                    cod_i = str(row.get('COD PROD', 'N/D'))
                                    nome_i = str(row.get('DESCRIÇÃO', ''))
                                    marca_i = str(row.get('MARCA', 'Geral'))
                                    preco_i = float(row.get('VLR VENDA', 0.0))
                                    
                                    chk = st.checkbox(f"[{cod_i}] {nome_i} - R$ {preco_i:.2f}", key=f"chk_imp_{arq.name}_{idx}")
                                    if chk:
                                        itens_add.append({
                                            "cod": cod_i,
                                            "nome": nome_i,
                                            "categoria": "Importados",
                                            "marca": marca_i,
                                            "modelo": "Universal",
                                            "preco": preco_i,
                                            "foto": "https://new-vipal-prd.s3.sa-east-1.amazonaws.com/product-images/product-4447-2_600x600.png"
                                        })
                                
                                if st.form_submit_button("Adicionar Selecionados"):
                                    for item in itens_add:
                                        ja_tem = any(p['nome'] == item['nome'] for p in st.session_state["produtos"])
                                        if not ja_tem:
                                            novo_id = max([p["id"] for p in st.session_state["produtos"]], default=0) + 1
                                            item["id"] = novo_id
                                            st.session_state["produtos"].append(item)
                                    st.success("Itens importados com sucesso!")
                                    st.rerun()
                        except Exception as e:
                            st.error(f"Erro: {e}")

            # Aba 4: Editar Itens
            with abas_admin[4]:
                st.subheader("Editar Produtos")
                if not st.session_state["produtos"]:
                    st.info("Nenhum produto cadastrado.")
                else:
                    d_prods = {f"[{p.get('cod','N/D')}] {p['nome']}": p for p in st.session_state["produtos"]}
                    sel_p = st.selectbox("Selecione o produto", list(d_prods.keys()))
                    if sel_p:
                        p_sel = d_prods[sel_p]
                        with st.form("form_edit_prod"):
                            e_cod = st.text_input("Código", value=p_sel.get('cod',''))
                            e_nome = st.text_input("Nome", value=p_sel['nome'])
                            e_preco = st.text_input("Preço", value=str(p_sel['preco']))
                            
                            if st.form_submit_button("Salvar"):
                                for p in st.session_state["produtos"]:
                                    if p['id'] == p_sel['id']:
                                        p['cod'] = e_cod
                                        p['nome'] = e_nome
                                        try:
                                            p['preco'] = float(e_preco)
                                        except:
                                            pass
                                st.success("Atualizado com sucesso!")
                                st.rerun()

            # Aba 5: Senhas
            with abas_admin[5]:
                st.subheader("Alterar Senha do Cliente")
                nova_s = st.text_input("Nova Senha", type="password")
                if st.button("Atualizar Senha"):
                    if nova_s.strip():
                        st.session_state["senha_cliente"] = nova_s
                        st.success("Senha alterada com sucesso!")
        else:
            st.error("Senha de Administrador incorreta.")