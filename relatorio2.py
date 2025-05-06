# Importa bibliotecas
import streamlit as st  # Streamlit para interface web
from fpdf import FPDF  # FPDF para geração do PDF
import os  # Biblioteca para manipulação de arquivos
from PIL import Image   # Biblioteca para manipulação de imagens
import base64 # Biblioteca para codificação e decodificação de dados binários
from io import BytesIO # Biblioteca para manipulação de fluxos de bytes
import requests

# -------------------- Baixar imagens do GitHub (se não existirem localmente) --------------------

# Dicionário com os caminhos locais e URLs das imagens no GitHub
IMAGENS = {
    "assets/logo_iqony.png": "https://raw.githubusercontent.com/Ruan2829/Relatoriodepa3/main/assets/logo_iqony.png",
    "assets/nomenclaturas.png": "https://raw.githubusercontent.com/Ruan2829/Relatoriodepa3/main/assets/nomenclaturas.png",
    "assets/wind_turbine_draw.png": "https://raw.githubusercontent.com/Ruan2829/Relatoriodepa3/main/assets/wind_turbine_draw.png",
}

# Cria a pasta 'assets' local se ainda não existir
os.makedirs("assets", exist_ok=True)

# Faz o download das imagens apenas se ainda não estiverem salvas localmente
for caminho_local, url_github in IMAGENS.items():
    if not os.path.exists(caminho_local):
        try:
            response = requests.get(url_github)
            if response.status_code == 200:
                with open(caminho_local, "wb") as f:
                    f.write(response.content)
        except Exception as e:
            print(f"Erro ao baixar {url_github}: {e}")



# Configuração da página Streamlit
st.set_page_config(page_title="Relatório de Inspeção", layout="centered")  # Título e layout da página
st.title("📄 Relatório de Inspeção de Pás")  # Título principal

# ------------------------------------ Estilo Streamlit ----------------------------------
st.markdown(
    """
    <style>
    /* Estilo geral dos campos de input */
    input {
        background-color: #ffffff !important;  /* branco */
        color: #000000 !important;             /* texto preto */
        border: 2px solid #4CAF50 !important;   /* borda verde bonito */
        border-radius: 8px;                     /* cantos arredondados */
        padding: 10px;                          /* espaço interno */
        font-size: 16px;                        /* tamanho da fonte */
    }

    /* Estilo dos campos de texto (textarea) */
    textarea {
        background-color: #ffffff !important;
        color: #000000 !important;
        border: 2px solid #4CAF50 !important;
        border-radius: 8px;
        padding: 10px;
        font-size: 16px;
    }

    /* Melhorando também os botões */
    button[kind="primary"] {
        background-color: #4CAF50 !important;  /* fundo verde */
        color: white !important;               /* texto branco */
        border: none !important;
        border-radius: 8px;
        padding: 10px 20px;
        font-size: 16px;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# Classe PDF personalizada
class PDF(FPDF):
    def header(self):
        # Verifica se o arquivo da logo existe e insere a imagem no canto superior esquerdo (x=10, y=10, largura=30mm)
        if os.path.exists("logo_iqony.png"):
            self.image("assets/logo_iqony.png", x=15, y=15, w=25)


        # Define a posição e fonte do título central do relatório
        self.set_xy(10, 10)                       # Define a posição (x=40, y=10) para o título
        self.set_font("Arial", "B", 16)           # Define a fonte Arial, negrito, tamanho 12
        self.cell(190, 40, "Relatório de Inspeção de Pás", border=1, ln=1, align="C")  # Linha 1 do título centralizada
        self.ln(5)                            # Adiciona uma quebra de linha após o título

        self.ln(5)
# ------------------------------------ Rodapé do PDF Com imagem -------------------------------------
    def footer(self):
        # Adiciona imagem no canto inferior esquerdo
        if os.path.exists("wind_turbine_draw.png"):
            self.image("assets/wind_turbine_draw.png", x=10, y=260, w=40)
  # Ajuste 'x', 'y' e 'w' conforme o necessário

        # Texto do rodapé
        self.set_y(-10)
        self.set_font("Arial", "I", 7)
        self.multi_cell(
            0, 4,      # Texto do rodapé, 0 largura, 6 altura
            "Este documento é de propriedade da Iqony Solutions do Brasil LTDA. Nenhuma parte deste documento pode\n"
            "ser distribuída sem sua permissão prévia por escrito.",
            border=0, align="C"
            
        )
        # Número da página centralizado
        # Número da página no formato "Página X de Y"
        self.set_y(-10)  # Ajusta posição
        self.cell(0, 10, f"Página {self.page_no()} de {{nb}}", align="R") # adiciona um rodapé ao documento, mostrando o número da página atual e o total de páginas, como por exemplo: "Página 3 de 10"

# ------------------------------------------- Área Departamento Responsável --------------------------

    def primeira_pagina(self, ambito_aplicacao, codigo_relatorio, revisado_por_1, revisado_por_2, data_revisao):
        self.set_font("Arial", "B", 12)
        self.multi_cell(0, 50, f"Departamento Responsável: O&M.\nÂmbito da aplicação: {ambito_aplicacao}", border=1)
        self.ln(10)
        self.cell(95, 10, f"Número: {codigo_relatorio}", 1)
        self.set_font("Arial", "B", 10)
        self.cell(95, 10, "Revisão: 02", 1, ln=True)

        self.set_font("Arial", "B", 10)
        self.cell(45, 10, "", 1)
        self.cell(80, 10, "(Assinatura):", 1)
        self.cell(65, 10, "Data:", 1, ln=True)

        self.set_font("Arial", "B", 10)
        linhas = [
            ["Elaborado por:", "Ruan Lopes da Silva", "12/04/2025"],
            ["Revisado por:", revisado_por_1, data_revisao],
            ["Revisado por:", revisado_por_2, data_revisao],
            ["Aprovado por:", "Vinícius Pazzini", "28/04/2025"]
        ]
        for linha in linhas:
            self.cell(45, 10, linha[0], 1)
            self.cell(80, 10, linha[1], 1)
            self.cell(65, 10, linha[2], 1, ln=True) 
    
# --------------------------------- Sumário ---------------------------------------------------
    def pagina_sumario(self): #
        self.add_page()
        self.set_font("Arial", "B", 14)
        self.cell(0, 10, "Sumário", ln=True, align="C")
        self.ln(5)

        self.set_font("Arial", "B", 12)
        topicos = [
            "1. Introdução",
            "2. Objetivo",
            "3. Dados Gerais do Aerogerador",
            "4. Dados Gerais das Pás",
            "5. Nomenclaturas",
            "6. Itens das pás a serem inspecionados",
            "7. Referência da Avaliação de defeitos",
            "8. Identificação da Máquina",
            "9. Especificação e identificação das pás",
            "10. Inspeção Externa",
            "  10.1. Classificação de defeitos evidenciados na área externa da pá 1",
            "  10.2. Classificação de defeitos evidenciados na área externa da pá 2",
            "  10.3. Classificação de defeitos evidenciados na área externa da pá 3",
            "11. Inspeção interna",
            "  11.1. Classificação de defeitos evidenciados na área interna da pá 1",
            "  11.2. Classificação de defeitos evidenciados na área interna da pá 2",
            "  11.3. Classificação de defeitos evidenciados na área interna da pá 3",
        ]
        for item in topicos:
            self.cell(0, 8, item, ln=True)


# ------------------------ 3. Dados Gerais do Aerogerador e 4. Dados Gerais das Pás  - Objetivo e introdução---------------------
    def pagina_dados(self, dados_gerais, dados_pas):
        self.add_page()
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, "1. Introdução", ln=True)

        
        self.set_font("Arial", "", 12)
        self.multi_cell(0, 8,
            "A atividade contratada consiste na inspeção das pás, realizada nas cascas externas, bordas de ataque e de fuga, "
            "e em toda a extensão das pás. A análise e classificação dos defeitos, bem como a avaliação dos reparos, foram "
            "realizadas pela equipe de serviços de O&M da IQONY.")
        self.ln(5)

        self.set_font("Arial", "B", 12)
        self.cell(0, 10, "2. Objetivo", ln=True)
        self.set_font("Arial", "", 12)
        self.multi_cell(0, 8,
            "Este relatório tem como objetivo apresentar os dados de uma inspeção de pás, realizada no aerogerador WEG modelo "
            "AGW 110 2.1MW, localizado nos parques eólicos Cutia e Bento Miguel. As evidências têm por finalidade documentar o "
            "estado operacional das pás.")
        self.ln(5)

        self.set_font("Arial", "B", 12)
        self.cell(0, 10, "3. Dados Gerais do Aerogerador", ln=True)
        self.set_font("Arial", "", 11)
        for rotulo, valor in dados_gerais.items(): # 
            self.cell(60, 10, rotulo, border=1)
            self.cell(130, 10, valor, border=1, ln=True)

        self.ln(5)
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, "4. Dados Gerais das Pás", ln=True)
        self.set_font("Arial", "", 11)
        for rotulo, valor in dados_pas.items():
            self.cell(60, 10, rotulo, border=1)
            self.cell(130, 10, valor, border=1, ln=True)

        self.ln(5)

# ------------------------ 5. Nomenclaturas -------------------------------------
    def pagina_nomenclaturas(self): 
        self.add_page()
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, "5. Nomenclaturas", ln=True)
        if os.path.exists("nomenclaturas.png"):
            self.image("assets/nomenclaturas.png", x=10, w=190)

        else:
            self.set_font("Arial", "I", 11)
            self.multi_cell(0, 10, "Imagem de nomenclaturas não encontrada.")



  # -------------- 6. Itens das Pás a Serem Inspecionados -----------------------------

    def pagina_itens_referencia_identificacao(self, imagem_maquina_path=None):
        self.add_page()
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, "6. Itens das Pás a Serem Inspecionados", ln=True)

        
        itens = [
            ("Extradorso", "E.D."),
            ("Intradorso", "I.D"),
            ("Bordo de Ataque", "B.A."),
            ("Bordo de Fuga", "B.F."),
            ("Tip", "T.P."),
            ("Raiz", "R.A."),
            ("Almas (B.A e B.F)", "A.B.A, A.B.F"),
            ("Áreas de Colagens (B.A e B.F)", "B.A.C, B.F.C"),
            ("SPDA", "SPDA")
        ]

        for nome, sigla in itens:   # Cria uma célula para cada item
            self.set_fill_color(220, 230, 241) # Cor de fundo azul claro
            self.set_font("Arial", "B", 12) # Define a fonte para o título
            self.cell(80, 10, nome, border=1, fill=True, align="C") # Cria célula com borda e fundo azul claro
            self.set_font("Arial", "", 11) # Define a fonte para o conteúdo
            self.cell(110, 10, sigla, border=1, ln=True) # Cria célula com borda e quebra de linha (ln=True)

   # ----------------- 7. Referência da Avaliação de Defeitos -----------------------------------------
        self.ln(5)
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, "7. Referência da Avaliação de Defeitos", ln=True)

        referencias = [
            ("1", "Danos leves", "Operação normal"),
            ("2", "Danos médios", "Reparo planejado"),
            ("3", "Danos Graves", "Reparo imediato"),
            ("4", "Danos Críticos", "Parar o aerogerador")
        ]

    
        for ref, desc, acao in referencias:
            self.set_font("Arial", "", 11)
            self.cell(20, 10, ref, border=1, align="C")
            self.cell(70, 10, desc, border=1, align="C")
            self.cell(100, 10, acao, border=1, ln=True, align="C")



 #-------------- 8. Identificação da Máquina ----------------------------------------------------------

        self.ln(5)
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, "8. Identificação da Máquina", ln=True)

        if imagem_maquina_path and os.path.exists(imagem_maquina_path):
            w = 190                 # Largura da imagem
            h = w * 0.2             # Altura proporcional
            x = (self.w - w) / 2    # Centraliza horizontalmente
            y = self.get_y()        # Usa posição vertical atual após o título

            self.rect(x, y, w, h)   # Borda ao redor da imagem
            self.image(imagem_maquina_path, x=x + 2, y=y + 2, w=w - 4, h=h - 4)  # Imagem com margens internas
            self.ln(h + 10)         # Espaço abaixo da imagem
        else:
            self.set_font("Arial", "I", 11)
            self.multi_cell(0, 10, "Imagem de identificação da máquina não enviada.")


# ------------------------ 9. Especificação e Identificação das Pás ---------------------
    def pagina_identificacao_pas(self, imagens_pás):
        self.add_page()
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, "9. Especificação e Identificação das Pás", ln=True)
        self.ln(1)

        for nome_pa, lista_imgs in imagens_pás.items():
            self.set_font("Arial", "B", 11)
            self.cell(0, 10, nome_pa, ln=True)
            self.ln(2)

            altura_foto = 50
            largura_foto = 80
            espacamento_x = 10

            # 🔵 Cálculo para centralizar
            total_largura = len(lista_imgs) * largura_foto + (len(lista_imgs) - 1) * espacamento_x
            x_inicial = (self.w - total_largura) / 2  # Centraliza as imagens
            y_inicial = self.get_y()

            for i, img in enumerate(lista_imgs):
                if os.path.exists(img):
                    x = x_inicial + i * (largura_foto + espacamento_x)
                    y = y_inicial

                    # 🔵 Desenha o retângulo (quadro)
                    self.rect(x, y, largura_foto, altura_foto)

                    # 🔵 Insere a imagem dentro do quadro
                    self.image(img, x=x + 2, y=y + 2, w=largura_foto - 4, h=altura_foto - 4)

            self.ln(altura_foto + 1)  # espaço abaixo das fotos antes da próxima PÁ



    #----------------------- 10. Expeção externa e 10.1 Classificação de Defeitos Pa1, Pa2 e Pa3 -------------------

    
    def pagina_inspecao_externa(self, numero_pa, tabela): 
        self.add_page()

        self.set_font("Arial", "B", 12)
        self.cell(0, 10, "10. Inspeção Externa", ln=True)
        self.ln(2)

        self.set_font("Arial", "B", 12)
        self.cell(0, 10, f"10.{numero_pa}. Classificação de defeitos evidenciados na área externa da pá {numero_pa}", ln=True)
        self.ln(2)

        self.set_font("Arial", "B", 10)
        self.cell(50, 10, "Localização", border=1)
        self.cell(70, 10, "Descrição dos danos/ evidências", border=1)
        self.cell(30, 10, "Área", border=1)
        self.cell(40, 10, "Código", border=1, ln=True)

        self.set_font("Arial", "", 10)
        for linha in tabela:
            self.cell(50, 10, linha["Localizacao"], border=1)
            self.cell(70, 10, linha["Descricao"], border=1)
            self.cell(30, 10, linha["Area"], border=1)
            self.cell(40, 10, linha["Código"], border=1, ln=True)
            self.ln(0)  # Adiciona um espaço entre as linhas da tabela


    def pagina_inspecao_fotos(self, numero_pa, imagens_obs): 
        #self.add_page()
        self.set_font("Arial", "B", 12)

        topicos = [
            ("Superfície da pá lado sucção", 2),
            ("Receptores do SPDA lado sucção", 2),
            ("B.A lado da sucção", 2),
            ("Superfície do B.A", 4),
            ("Superfície da pá lado da pressão", 4),
            ("Receptores do SPDA lado da pressão", 2),
            ("Superfície no B.A lado da pressão", 2),
        ]

        for i, (titulo, qtd_max) in enumerate(topicos):
            self.cell(0, 10, f"10.{numero_pa}.{i+1} {titulo}", ln=True)
            self.ln(3)
            imagens, obs = imagens_obs.get(titulo, ([], ""))
            self._inserir_imagens_com_obs(imagens, obs, max_img=qtd_max)


    def pagina_inspecao_externa_pa1(self, tabela_pa1):
        self.add_page()
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, "10. Inspeção Externa", ln=True)
        self.ln(3)

        self.set_font("Arial", "B", 11)
        self.cell(0, 10, "10.1. Classificação de defeitos evidenciados na área externa da pá 1", ln=True)
        self.ln(5)

        # Cabeçalhos da tabela
        self.set_font("Arial", "B", 10)
        self.cell(50, 10, "Localização", border=1, align="C")
        self.cell(70, 10, "Descrição dos danos/ evidências", border=1, align="C")
        self.cell(30, 10, "Área", border=1, align="C")
        self.cell(40, 10, "Código", border=1, ln=True, align="C")

        # Linhas da tabela preenchidas a partir do dicionário
        self.set_font("Arial", "", 10)
        for linha in tabela_pa1:
            self.cell(50, 10, linha["Localizacao"], border=1)
            self.cell(70, 10, linha["Descricao"], border=1)
            self.cell(30, 10, linha["Area"], border=1)
            self.cell(40, 10, linha["Código"], border=1, ln=True)

    def pagina_inspecao_externa_pa2(self, tabela_pa2):
        self.add_page()
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, "10.2. Classificação de defeitos evidenciados na área externa da pá 2", ln=True)
        self.ln(5)

        self.set_font("Arial", "B", 10)
        self.cell(50, 10, "Localização", border=1)
        self.cell(70, 10, "Descrição dos danos/ evidências", border=1)
        self.cell(30, 10, "Área", border=1)
        self.cell(40, 10, "Código", border=1, ln=True)

        self.set_font("Arial", "", 10)
        for linha in tabela_pa2:
            self.cell(50, 10, linha["Localizacao"], border=1)
            self.cell(70, 10, linha["Descricao"], border=1)
            self.cell(30, 10, linha["Area"], border=1)
            self.cell(40, 10, linha["Código"], border=1, ln=True)

    def pagina_inspecao_externa_pa3(self, tabela_pa3):
        self.add_page()
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, "10.3. Classificação de defeitos evidenciados na área externa da pá 3", ln=True)
        self.ln(5)

        self.set_font("Arial", "B", 10)
        self.cell(50, 10, "Localização", border=1)
        self.cell(70, 10, "Descrição dos danos/ evidências", border=1)
        self.cell(30, 10, "Área", border=1)
        self.cell(40, 10, "Código", border=1, ln=True)

        self.set_font("Arial", "", 10)
        for linha in tabela_pa3:
            self.cell(50, 10, linha["Localizacao"], border=1)
            self.cell(70, 10, linha["Descricao"], border=1)
            self.cell(30, 10, linha["Area"], border=1)
            self.cell(40, 10, linha["Código"], border=1, ln=True)


    def _inserir_imagens_com_obs(self, lista_imagens, observacao, max_img=2):
        largura_img = 90  # Largura de cada imagem
        altura_img = 60   # Altura de cada imagem
        espacamento = 10  # Espaço horizontal entre imagens

        x_inicial = 10  # Margem esquerda
        y_inicial = self.get_y()  # Posição vertical atual

        # Posiciona cada imagem lado a lado
        for i, img_path in enumerate(lista_imagens[:max_img]):
            if os.path.exists(img_path):
                x = x_inicial + i * (largura_img + espacamento)  # Calcula a posição X de cada imagem
                self.set_xy(x, y_inicial)  # Define a posição
                self.rect(x, y_inicial, largura_img, altura_img)  # Desenha borda
                self.image(img_path, x + 2, y_inicial + 2, w=largura_img - 4, h=altura_img - 4)  # Insere imagem dentro da borda

        # Após todas as imagens, pula para linha de baixo
        self.set_y(y_inicial + altura_img + 5)

        self.set_font("Arial", "I", 11)
        self.multi_cell(0, 8, f"Observações: {observacao or '-'}")
        self.ln(10)


    def pagina_inspecao_completa_pa(self, numero_pa, tabela, imagens_obs):
        self.pagina_inspecao_externa(numero_pa, tabela)
        self.pagina_inspecao_fotos(numero_pa, imagens_obs)

        topicos = [
            ("Superfície da pá lado sucção", 2),
            ("Receptores do SPDA lado sucção", 2),
            ("B.A lado da sucção", 2),
            ("Superfície do B.A", 4),
            ("Superfície da pá lado da pressão", 4),
            ("Receptores do SPDA lado da pressão", 2),
            ("Superfície no B.A lado da pressão", 2),
        ]

        for i, (titulo, max_img) in enumerate(topicos):
            self.cell(0, 10, f"10.{numero_pa}.{i+1} {titulo}", ln=True)
            self.ln(3)
            imagens, obs = imagens_obs.get(titulo, ([], ""))
            self._inserir_imagens_com_obs(imagens, obs, max_img=max_img)

# ------------------------ 11. Inspeção Interna -------------------------------------

    def pagina_inspecao_interna_completa_pa(self, numero_pa, fotos_identificacao, tabela_defeitos, imagens_obs):
        self.add_page()
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, f"11. Inspeção Interna - Pá {numero_pa}", ln=True)
        self.ln(5)

        # 11.1 Identificação da pá
        self.set_font("Arial", "B", 11)
        self.cell(0, 10, "11.1 Identificação da pá", ln=True)
        self.ln(2)

        largura_img = 90
        altura_img = 60
        espacamento = 10

        for i, img in enumerate(fotos_identificacao[:2]):
            if os.path.exists(img):
                x = 10 + i * (largura_img + espacamento)
                y = self.get_y()
                self.rect(x, y, largura_img, altura_img)
                self.image(img, x + 2, y + 2, w=largura_img - 4, h=altura_img - 4)

        self.ln(altura_img + 5)

        # 11.2 Classificação de defeitos evidenciados
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, "11. Inspeção Interna", ln=True)
        self.ln(3)

        self.set_font("Arial", "B", 11)
        self.cell(0, 10, f"11.2 Classificação de defeitos evidenciados na área interna da pá {numero_pa}", ln=True)
        self.ln(3)


        self.set_font("Arial", "B", 10)
        self.set_fill_color(220, 230, 241)
        self.cell(50, 10, "Localização", border=1, fill=True, align="C")
        self.cell(70, 10, "Descrição dos danos/ evidências", border=1, fill=True, align="C")
        self.cell(30, 10, "Área", border=1, fill=True, align="C")
        self.cell(40, 10, "Código", border=1, fill=True, align="C")
        self.ln()

        self.set_font("Arial", "", 10)
        for linha in tabela_defeitos:
            self.cell(50, 10, linha["Localizacao"], border=1)
            self.cell(70, 10, linha["Descricao"], border=1)
            self.cell(30, 10, linha["Area"], border=1)
            self.cell(40, 10, linha["Código"], border=1)
            self.ln()

        self.ln(5)

        # Subitens com fotos
        topicos = [
            f"11.2.1 B.A Não apresenta falhas de colagem visíveis",
            f"11.2.2 Superfície entre as almas do B.F e Alma do B.A",
            f"11.2.3 Coletores do SPDA",
            f"11.2.4 B.F não apresenta falhas de colagem visíveis"
        ]

        for i, titulo in enumerate(topicos):
            self.set_font("Arial", "B", 11)
            self.cell(0, 10, titulo, ln=True)
            self.ln(3)

            imagens, obs = imagens_obs.get(titulo, ([], ""))
            self._inserir_imagens_com_obs(imagens, obs, max_img=2)



# -----------------------CAMPOS DE ENTRADA PARA O USUÁRIO VIA STREAMLIT-------------------------------

#------------------------ Inputs Primeira pagina --------------------------------
st.subheader("📄 Dados da Capa do Relatório")

ambito_aplicacao = st.text_input("Âmbito da Aplicação:", value="Complexo Eólico Cutia - WTG SM2-09")
codigo_relatorio = st.text_input("Código do Relatório:", value="IQONY-INSP-01")
revisado_por_1 = st.text_input("Revisado por (1ª Revisão):", value="")
revisado_por_2 = st.text_input("Revisado por (2ª Revisão):", value="")
data_revisao = st.text_input("Data da Revisão:", value="12/04/2025")

# ------------------------ Inputs Dados Gerais do Aerogerador ----------------------------

st.subheader("🔧 3. Dados Gerais do Aerogerador")
fabricante_modelo = st.text_input("Fabricante Modelo:", value="WEG AGW 110 2.1 MW")
ano_fabricacao = st.text_input("Ano de Fabricação:", value="2015")
altura_torre = st.text_input("Altura da Torre:", value="120m")


st.subheader("🔧 4. Dados Gerais das Pás")
fabricante_pas = st.text_input("Fabricante:")
tipo_pa = st.text_input("Tipo de Pá de Rotor:")
num_serie_pas = st.text_input("Número de Série das Pás:")
num_serie_set = st.text_input("Número de Série do Set:")
elementos_fluxo = st.text_input("Elementos de Fluxo de Ar:")
dispositivos_luz = st.text_input("Dispositivos de iluminação:")


#-------------------------------------- Inputs Nomenclaturas -------------------------------------
# 📸 SEÇÃO 8 – IDENTIFICAÇÃO DA MÁQUINA
st.subheader("📸 8. Identificação da Máquina")

with st.container():
    st.markdown("**📷 Envie uma imagem de identificação do Aerogerador**")
    
    imagem_maquina = st.file_uploader(
        "Selecione a imagem (PNG ou JPG)", 
        type=["jpg", "jpeg", "png"]
    )

    imagem_maquina_path = None
    if imagem_maquina:
        # Detecta a extensão correta a partir do tipo MIME
        extensao = imagem_maquina.type.split("/")[-1]
        imagem_maquina_path = f"imagem_maquina.{extensao}"

        # Salva o arquivo corretamente com a extensão original
        with open(imagem_maquina_path, "wb") as f:
            f.write(imagem_maquina.read())

        # Mostra imagem carregada abaixo
        #st.image(imagem_maquina, caption="Imagem carregada", use_column_width=True)

st.subheader("📷 9. Especificação e Identificação das Pás")

imagens_pás = {}

# Loop para as 3 pás
for i in range(1, 4):  # Loop de 1 a 3 para as pás
    with st.container():  # Cria um container para cada pá
        st.markdown(f"### 📌 PÁ {i}")  # Título para cada pá
        fotos = st.file_uploader(  # Carrega as fotos da pá
            f"Envie até 2 fotos para a PÁ {i}",  # Título do uploader
            type=["jpg", "jpeg", "png"],  # Tipo de arquivo aceito
            accept_multiple_files=True,  # Aceita múltiplos arquivos
            key=f"foto_pa_{i}"  # Chave única para cada pá
        )

        caminhos = []  # Lista para armazenar os caminhos das fotos
        for j, foto in enumerate(fotos[:2]):  # Limita a 2 fotos
            extensao = foto.type.split("/")[-1]  # Detecta a extensão correta
            caminho = f"foto_pa_{i}_{j}.{extensao}"  # Cria o caminho do arquivo
            with open(caminho, "wb") as f:  # Abre o arquivo para escrita
                f.write(foto.read())  # Salva o arquivo
            caminhos.append(caminho)  # Adiciona o caminho à lista

        imagens_pás[f"PÁ {i}"] = caminhos  # Guarda os caminhos por pá

    


# ------------------------ Inputs Inspeção Externa -------------------------------------
# 10. Inspeção Externa - Classificação de Defeitos (PÁ 1, PÁ 2 e PÁ 3)


st.subheader("🔍 10. Inspeção Externa - Classificação de Defeitos (PÁ 1)")

# Lista das localizações da pá
localizacoes = ["R.A Ping Teste", "I.D", "E. D", "B. A", "B. F", "TIP", "SPDA"]

# Lista para armazenar os dados preenchidos
tabela_externa_pa1 = []

# Gera campos de entrada para cada linha da tabela
for loc in localizacoes:
    col1, col2, col3 = st.columns([2, 2, 2])  # Cria 3 colunas com largura igual

    with col1:
        desc = st.text_input(f"Descrição - {loc}", key=f"desc_{loc}")

    with col2:
        area = st.text_input(f"Área - {loc}", key=f"area_{loc}")

    with col3:
        cod_cor = st.text_input(f"Código - {loc}", key=f"cod_{loc}")

    
    # Armazena os dados para o PDF
    tabela_externa_pa1.append({
        "Localizacao": loc,
        "Descricao": desc,
        "Area": area,
        "Código": cod_cor
    })

st.markdown("---") # Linha de separação

st.subheader("🔍 10.2 Inspeção Externa - Classificação de Defeitos (PÁ 2)")

tabela_externa_pa2 = []

for loc in localizacoes:
    st.markdown(f"**📌 Localização: {loc}**")
    
    col1, col2, col3 = st.columns([2, 2, 2])

    with col1:
        desc = st.text_input(f"Descrição - {loc}", key=f"desc_pa2_{loc}")

    with col2:
        area = st.text_input(f"Área - {loc}", key=f"area_pa2_{loc}")

    with col3:
        cod_cor = st.text_input(f"Código- {loc}", key=f"cod_pa2_{loc}")

    tabela_externa_pa2.append({
        "Localizacao": loc,
        "Descricao": desc,
        "Area": area,
        "Código": cod_cor
    })


st.subheader("🔍 10.3 Inspeção Externa - Classificação de Defeitos (PÁ 3)")

tabela_externa_pa3 = []

for loc in localizacoes:
    st.markdown(f"**📌 Localização: {loc}**")
    
    col1, col2, col3 = st.columns([2, 2, 2])

    with col1:
        desc = st.text_input(f"Descrição - {loc}", key=f"desc_pa3_{loc}")

    with col2:
        area = st.text_input(f"Área - {loc}", key=f"area_pa3_{loc}")

    with col3:
        cod_cor = st.text_input(f"Código - {loc}", key=f"cod_pa3_{loc}")

    tabela_externa_pa3.append({
        "Localizacao": loc,
        "Descricao": desc,
        "Area": area,
        "Código": cod_cor
    })


       

# 📸 INSPEÇÃO EXTERNA - NOVO MODELO

# --- Inspeção Externa - PÁ 1 ---
st.subheader("🔍 10.1 Inspeção Externa - PÁ 1")

topicos_externa = [
    "Superfície da pá lado sucção",
    "Receptores do SPDA lado sucção",
    "B.A lado da sucção",
    "Superfície do B.A",
    "Superfície da pá lado da pressão",
    "Receptores do SPDA lado da pressão",
    "Superfície no B.A lado da pressão"
]

topicos_selecionados_pa1 = st.multiselect(
    "Selecione os tópicos com problemas na PÁ 1:", 
    topicos_externa, 
    key="topicos_selecionados_pa1"
)

imagens_obs_externa_pa1 = {}

for topico in topicos_selecionados_pa1:
    st.markdown(f"### 📸 {topico} (PÁ 1)")
    fotos = st.file_uploader(f"Envie até 2 fotos para '{topico}' (PÁ 1)", 
                             type=["jpg", "jpeg", "png"], 
                             accept_multiple_files=True, 
                             key=f"fotos_externa_pa1_{topico}")
    obs = st.text_area(f"Observações sobre '{topico}' (PÁ 1)", key=f"obs_externa_pa1_{topico}")
    imagens_obs_externa_pa1[topico] = (fotos, obs)

# --- Inspeção Externa - PÁ 2 ---
st.subheader("🔍 10.2 Inspeção Externa - PÁ 2")

topicos_selecionados_pa2 = st.multiselect(
    "Selecione os tópicos com problemas na PÁ 2:", 
    topicos_externa, 
    key="topicos_selecionados_pa2"
)

imagens_obs_externa_pa2 = {}

for topico in topicos_selecionados_pa2:
    st.markdown(f"### 📸 {topico} (PÁ 2)")
    fotos = st.file_uploader(f"Envie até 2 fotos para '{topico}' (PÁ 2)", 
                             type=["jpg", "jpeg", "png"], 
                             accept_multiple_files=True, 
                             key=f"fotos_externa_pa2_{topico}")
    obs = st.text_area(f"Observações sobre '{topico}' (PÁ 2)", key=f"obs_externa_pa2_{topico}")
    imagens_obs_externa_pa2[topico] = (fotos, obs)

# --- Inspeção Externa - PÁ 3 ---
st.subheader("🔍 10.3 Inspeção Externa - PÁ 3")

topicos_selecionados_pa3 = st.multiselect(
    "Selecione os tópicos com problemas na PÁ 3:", 
    topicos_externa, 
    key="topicos_selecionados_pa3"
)

imagens_obs_externa_pa3 = {}

for topico in topicos_selecionados_pa3:
    st.markdown(f"### 📸 {topico} (PÁ 3)")
    fotos = st.file_uploader(f"Envie até 2 fotos para '{topico}' (PÁ 3)", 
                             type=["jpg", "jpeg", "png"], 
                             accept_multiple_files=True, 
                             key=f"fotos_externa_pa3_{topico}")
    obs = st.text_area(f"Observações sobre '{topico}' (PÁ 3)", key=f"obs_externa_pa3_{topico}")
    imagens_obs_externa_pa3[topico] = (fotos, obs)

          
# ----------------------------- INSPEÇÃO INTERNA -----------------------------



# Função para gerar a tabela de defeitos internos

def tabela_defeitos_interna(numero_pa):
    st.subheader(f"📋 11.2 Inspeção Interna - Classificação de Defeitos - PÁ {numero_pa}")
    tabela = []
    localizacoes = [
        "C.E.", "B.F.", "B.F.C.", "I.D.B.F.", "E.D.B.F.", "A.B.F.",
        "I.D.E.A.", "A.B.A.", "I.D.B.A.", "E.D.B.A.", "B.A.", "B.A.C"
    ]
    for loc in localizacoes:
        col1, col2, col3 = st.columns([2, 2, 2])

        with col1:
            desc = st.text_input(f"Descrição interna - {loc} (PÁ {numero_pa})", key=f"desc_def_interna_pa{numero_pa}_{loc}")

        with col2:
            area = st.text_input(f"Área interna - {loc} (PÁ {numero_pa})", key=f"area_def_interna_pa{numero_pa}_{loc}")

        with col3:
            cod_interno = st.text_input(f"Código - {loc} (PÁ {numero_pa})", key=f"cod_def_interna_pa{numero_pa}_{loc}")

        tabela.append({
            "Localizacao": loc,
            "Descricao": desc or "-",
            "Area": area or "-",
            "Código": cod_interno or "-"
        })
    return tabela

# Listas de tópicos com fotos (Inspeção Interna)
topicos_interna = [
    "B.A",
    "Superfície entre as almas do B.F e Alma do B.A",
    "Coletores do SPDA",
    "B.F"
]

# Bloco dinâmico para fotos e observações por PÁ

def bloco_inspecao_interna(pa_num):
    st.subheader(f"📷 11.3 Itens com evidências fotográficas - PÁ {pa_num}")
    imagens_obs = {}
    topicos_selecionados = st.multiselect(
        f"Selecione os tópicos com problemas (PÁ {pa_num} - interna):",
        topicos_interna, key=f"topicos_interna_pa{pa_num}"
    )
    for topico in topicos_selecionados:
        st.markdown(f"### 📸 {topico} (PÁ {pa_num})")
        fotos = st.file_uploader(
            f"Envie até 2 fotos para '{topico}' (PÁ {pa_num})",
            type=["jpg", "jpeg", "png"],
            accept_multiple_files=True,
            key=f"fotos_interna_pa{pa_num}_{topico}"
        )
        obs = st.text_area(f"Observações sobre '{topico}' (PÁ {pa_num})", key=f"obs_interna_pa{pa_num}_{topico}")
        imagens_obs[topico] = (fotos, obs)
    return imagens_obs

#------------------------ Inspeção Interna - PÁ 1 ----------------------------
# PDF - Tabelas + Fotos

def gerar_tabela_defeitos(pdf, titulo, tabela):
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, titulo, ln=True)
    pdf.set_font("Arial", "B", 10)
    pdf.set_fill_color(220, 230, 241)
    pdf.cell(50, 10, "Localização", border=1, fill=True, align="C")
    pdf.cell(70, 10, "Descrição dos danos/ evidências", border=1, fill=True, align="C")
    pdf.cell(30, 10, "Área", border=1, fill=True, align="C")
    pdf.cell(40, 10, "Código", border=1, fill=True, align="C")
    pdf.ln()
    pdf.set_font("Arial", "", 10)
    for linha in tabela:
        pdf.cell(50, 10, linha["Localizacao"], border=1)
        pdf.cell(70, 10, linha["Descricao"], border=1)
        pdf.cell(30, 10, linha["Area"], border=1)
        pdf.cell(40, 10, linha["Código"], border=1)
        pdf.ln()

def inserir_topicos_fotos(pdf, imagens_obs, pa_num):
    for titulo, (fotos, obs) in imagens_obs.items():
        if fotos or obs:
            pdf.set_font("Arial", "B", 12)
            pdf.cell(0, 10, f"- {titulo}", ln=True)
            pdf.ln(3)

            largura_img = 90
            altura_img = 60
            espacamento = 10
            x_inicial = 10  # Começar um pouco da margem
            y_inicial = pdf.get_y()

            for i, foto in enumerate(fotos[:2]):
                if foto:
                    extensao = foto.type.split("/")[-1]
                    caminho_temp = f"temp_interna_pa{pa_num}_{i}.{extensao}".replace(" ", "_")
                    with open(caminho_temp, "wb") as f:
                        f.write(foto.read())

                    # Posiciona corretamente a imagem lado a lado
                    x = x_inicial + i * (largura_img + espacamento)
                    pdf.set_xy(x, y_inicial)
                    pdf.rect(x, y_inicial, largura_img, altura_img)
                    pdf.image(caminho_temp, x + 2, y_inicial + 2, w=largura_img - 4, h=altura_img - 4)

                    os.remove(caminho_temp)

            pdf.set_y(y_inicial + altura_img + 5)  # Move para baixo depois das imagens

            pdf.set_font("Arial", "I", 11)
            pdf.multi_cell(0, 8, f"Observações: {obs or '-'}")
            pdf.ln(10)



# Chamadas para as 3 PÁs
tabela_defeitos_pa1 = tabela_defeitos_interna(1)
tabela_defeitos_pa2 = tabela_defeitos_interna(2)
tabela_defeitos_pa3 = tabela_defeitos_interna(3)

imagens_obs_interna_pa1 = bloco_inspecao_interna(1)
imagens_obs_interna_pa2 = bloco_inspecao_interna(2)
imagens_obs_interna_pa3 = bloco_inspecao_interna(3)

# -------------------------- Geração do PDF -----------------------------
if st.button("📄 Gerar Relatório em PDF"):
    pdf = PDF()
    pdf.alias_nb_pages()
    pdf.add_page()

    # 👇 Depois começa a montar o PDF
    pdf.primeira_pagina(
        ambito_aplicacao,
        codigo_relatorio,
        revisado_por_1,
        revisado_por_2,
        data_revisao
    )

    pdf.pagina_sumario()

    dados_gerais = {
        "Fabricante Modelo": fabricante_modelo,
        "Ano de Fabricação": ano_fabricacao,
        "Altura do torre": altura_torre
    }

    dados_pas = {
        "Fabricante": fabricante_pas,
        "Tipo de Pá de Rotor": tipo_pa,
        "Número de Série das Pás": num_serie_pas,
        "Número de Série do Set": num_serie_set,
        "Elementos de Fluxo de Ar": elementos_fluxo,
        "Dispositivos de iluminação": dispositivos_luz
    }

    pdf.pagina_dados(dados_gerais, dados_pas)
    pdf.pagina_nomenclaturas()
    pdf.pagina_itens_referencia_identificacao(imagem_maquina_path)
    pdf.pagina_identificacao_pas(imagens_pás)

    # ----------------- Inspeção Externa -----------------
    pdf.add_page()
    gerar_tabela_defeitos(pdf, "10.1 Classificação de defeitos evidenciados na área externa da pá 1", tabela_externa_pa1)
    inserir_topicos_fotos(pdf, imagens_obs_externa_pa1, 1)

    pdf.add_page()
    gerar_tabela_defeitos(pdf, "10.2 Classificação de defeitos evidenciados na área externa da pá 2", tabela_externa_pa2)
    inserir_topicos_fotos(pdf, imagens_obs_externa_pa2, 2)

    pdf.add_page()
    gerar_tabela_defeitos(pdf, "10.3 Classificação de defeitos evidenciados na área externa da pá 3", tabela_externa_pa3)
    inserir_topicos_fotos(pdf, imagens_obs_externa_pa3, 3)

    # ----------------- Inspeção Interna -----------------
    pdf.add_page()
    gerar_tabela_defeitos(pdf, "11.2 Classificação de defeitos evidenciados na área interna da pá 1", tabela_defeitos_pa1)
    inserir_topicos_fotos(pdf, imagens_obs_interna_pa1, 1)

    pdf.add_page()
    gerar_tabela_defeitos(pdf, "11.2 Classificação de defeitos evidenciados na área interna da pá 2", tabela_defeitos_pa2)
    inserir_topicos_fotos(pdf, imagens_obs_interna_pa2, 2)

    pdf.add_page()
    gerar_tabela_defeitos(pdf, "11.2 Classificação de defeitos evidenciados na área interna da pá 3", tabela_defeitos_pa3)
    inserir_topicos_fotos(pdf, imagens_obs_interna_pa3, 3)

    # ----------------- Finalização -----------------
    caminho_pdf = "relatorio_inspecao.pdf"
    pdf.output(caminho_pdf)

    st.success("✅ Relatório gerado com sucesso!")

    with open(caminho_pdf, "rb") as f:
        st.download_button(
            label="📥 Baixar PDF",
            data=f,
            file_name="relatorio_inspecao.pdf",
            mime="application/pdf"
        )
