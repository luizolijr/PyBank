import os
import streamlit as st
from datetime import datetime, timedelta, timezone
import csv
import json
import pandas as pd

def retorna_hoje(offset: int = -3) -> datetime.date:
    """
    Essa funcao retorna a data de hoje no fuso horario informado.
    Por padrão o fuso horario é o UTC -3:00, America/Sao_Paulo
    """
    timezone_offset = offset  # America/Sao_Paulo (UTC−03:00)
    tzinfo = timezone(timedelta(hours=timezone_offset))
    today = datetime.now(tzinfo)
    return today

def caminho_relatorios(nome_arquivo):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    path_to_file = os.path.join(script_dir, nome_arquivo)
    return path_to_file

def salvar_csv(dados, nome_arquivo):
    data = str(retorna_hoje())
    data = data[0:19]
    data = data.replace(":", "-")
    path_to_file = caminho_relatorios(data+"_"+nome_arquivo)
    arquivo_existente = False
    try:
        with open(path_to_file, 'r') as file:
            arquivo_existente = True
    except FileNotFoundError:
        pass
    with open(path_to_file, 'a', newline='') as file:
        writer = csv.writer(file)
        if not arquivo_existente:
            writer.writerow(['id_registro', 'id_usuario', 'tipo', 'categoria', 'valor', 'data_registro'])
        writer.writerow(dados)

# Carregar dados
def ler_em_json(nome_arquivo):
    path_to_file = caminho_relatorios(nome_arquivo)
    try:
        with open(path_to_file, 'r') as arq_json:
            dados_json = json.load(arq_json)
        return dados_json
    except FileNotFoundError:
        return []

# Salvar dados
def salvar_em_json(registros_geral, nome_arquivo):
    path_to_file = caminho_relatorios(nome_arquivo)
    with open(path_to_file, 'w') as arq_json:
        json.dump(registros_geral, arq_json)


# Função para exportar o relatório
def exportar_relatorio(dados_filtrados):
    data = str(retorna_hoje())
    data = data[0:19]
    data = data.replace(":", "-")
    formato_exportacao = ['CSV', 'JSON']
    escolha = st.radio('Exportar Relatório', formato_exportacao)

    if escolha == 'CSV':
        botao_exportar = st.button("Exportar")
        if botao_exportar:
            for i in dados_filtrados:
                dados_para_salvar = [i['id_registro'], i['id_usuario'], i['tipo'], i['categoria'], i['valor'], i['data_registro']]
                salvar_csv(dados_para_salvar, 'relatorio.csv')
            st.success(f"Relatório salvo em {data}_relatorio.csv")
    if escolha == 'JSON':
        botao_exportar = st.button("Exportar")
        if botao_exportar:
            salvar_em_json(dados_filtrados, 'relatorio.json')
            st.success("Relatório salvo em relatorio.json")



# Função para adicionar registro
def adicionar_registro(id_usuario, registros_geral):
    tipo = st.selectbox("Tipo", ["Despesa", "Receita", "Investimento"])
    valor = st.number_input("Valor", step=1)
    categoria = st.text_input("Categoria")
    data_registro = st.date_input("Data do Registro", datetime.now().date())

    if st.button("Adicionar Registro"):
        novo_registro = {
            'id_registro': max([i['id_registro'] for i in registros_geral], default=-1) + 1,
            'id_usuario': id_usuario,
            'tipo': tipo,
            'categoria': categoria,
            'valor': -valor if tipo == "Despesa" else valor,
            'dia': data_registro.day,
            'mes': data_registro.month,
            'ano': data_registro.year,
            'data_registro': data_registro.strftime("%Y-%m-%d")
        }
        registros_geral.append(novo_registro)
        salvar_em_json(registros_geral, 'registros.json')
        st.success("Registro adicionado com sucesso!")

# Função para visualizar registros
def visualizar_registros(registros):

    # Filtros
    filtro_tipo = st.selectbox("Filtrar por Tipo", ["Todos"] + list(set(registro['tipo'] for registro in registros)))
    filtro_mes = st.selectbox("Filtrar por Mês", ["Todos"] + list(set(registro['mes'] for registro in registros)))
    filtro_ano = st.selectbox("Filtrar por Ano", ["Todos"] + list(set(registro['ano'] for registro in registros)))

    # Aplicar filtros
    registros_filtrados = registros.copy()

    if filtro_tipo != "Todos":
        registros_filtrados = [registro for registro in registros_filtrados if registro['tipo'] == filtro_tipo]

    if filtro_mes != "Todos":
        registros_filtrados = [registro for registro in registros_filtrados if registro['mes'] == filtro_mes]

    if filtro_ano != "Todos":
        registros_filtrados = [registro for registro in registros_filtrados if registro['ano'] == filtro_ano]

    df = pd.DataFrame(registros_filtrados)
    agrupado = df.groupby('tipo').valor.sum().reset_index()


    check_despesa = (agrupado['tipo'] == "Despesa").any()
    check_receita = (agrupado['tipo'] == "Receita").any()
    check_investimento = (agrupado['tipo'] == "Investimento").any()

    if check_despesa:
        valor_total_despesa = agrupado.loc[agrupado['tipo'] == "Despesa", "valor"].values[0]
    if check_receita:
        valor_total_receita = agrupado.loc[agrupado['tipo'] == "Receita", "valor"].values[0]
    if check_investimento:
        valor_total_investimento = agrupado.loc[agrupado['tipo'] == "Investimento", "valor"].values[0]

    col1, col2 = st.columns(2)
    if registros_filtrados:
        with col1:
            exportar_relatorio(registros_filtrados)

        with col2:
            st.subheader("Total por tipo:")
            if check_despesa:
                st.write(f"Total de Despesa: R$ {valor_total_despesa}")
            else:
                st.write(f"Total de Despesa: R$ 0.00")

            if check_receita:
                st.write(f"Total de Receita: R$ {valor_total_receita}")
            else:
                st.write(f"Total de Receita: R$ 0.00")

            if check_investimento:
                st.write(f"Total de Investimento: R$ {valor_total_investimento}")
            else:
                st.write(f"Total de Investimento: R$ 0.00")
        st.table(registros_filtrados)

    else:
        st.warning("Nenhum registro encontrado com os filtros selecionados.")


# Outras funções (como editar, deletar, filtrar, etc.) podem ser adicionadas de maneira semelhante.
def editar_registro(id_usuario, registros_geral):
    data = str(retorna_hoje().date())
    ano, mes, dia = map(int, data.split('-'))

    consulta_registros = [registro for registro in registros_geral if registro['id_usuario'] == id_usuario]


    id_registro_para_editar = st.number_input("Selecione o ID do REGISTRO que deseja EDITAR", step=1)
    indice_para_editar = [i for i, registro in enumerate(registros_geral) if registro['id_registro'] == id_registro_para_editar]

    tipo = st.text_input('Digite o novo TIPO do registro - Despesa: d, Receita: r, Investimento: i')
    if tipo != 'd' and tipo != 'r' and tipo != 'i' and tipo != '':
        st.warning('Opção inválida. Escolha d, r ou i')

    categoria = st.text_input('Digite a nova CATEGORIA do registro')
    valor = st.number_input('Digite o novo VALOR do registro')
    botao_exportar = st.button("Editar Registro")
    st.write(f"Registros do usuário {id_usuario} ")
    st.table(consulta_registros)

    if tipo.lower() == 'd':
        tipo = "Despesa"
    elif tipo.lower() == 'r':
        tipo = "Receita"
    elif tipo.lower() == 'i':
        tipo = "Investimento"
    else:
        return

    valor = -valor if tipo == "Despesa" else valor
    valor = "{:.2f}".format(valor)

    if botao_exportar:
        registros_geral[indice_para_editar[0]]['tipo'] = tipo
        registros_geral[indice_para_editar[0]]['categoria'] = categoria
        registros_geral[indice_para_editar[0]]['valor'] = valor
        registros_geral[indice_para_editar[0]]['dia'] = dia
        registros_geral[indice_para_editar[0]]['mes'] = mes
        registros_geral[indice_para_editar[0]]['ano'] = ano
        registros_geral[indice_para_editar[0]]['data_registro'] = data

        salvar_em_json(registros_geral, 'registros.json')
        st.success("Registro Editado!")

def deletar_registro(id_usuario, registros_geral):
    registros_do_usuario = [registro for registro in registros_geral if registro['id_usuario'] == id_usuario]

    id_registro_para_deletar = st.number_input("Informe o ID do REGISTRO que deseja deletar", step=1)
    st.warning(f'Tem certeza que deseja DELETAR o registro {id_registro_para_deletar}?')

    if st.button("Deletar"):
        registros_do_usuario = [registro for registro in registros_do_usuario if registro['id_registro'] != id_registro_para_deletar]
        st.success("Registro Deletado!")
        salvar_em_json(registros_do_usuario, 'registros.json')

    st.write(f"Registros do usuário {id_usuario}")
    st.table(registros_do_usuario)

def calcula_diferenca_dias(data_fim:datetime.date,data_ini:datetime.date)->int:
    """
    Recebe duas datas e calcula a diferenca de dias entre elas.
    """
    dif = data_fim - data_ini
    dias = dif.days
    return dias


def atualizar_rendimento(registros):
    data_atual = retorna_hoje().date()
    df = pd.DataFrame(registros)
    df['data_registro'] = pd.to_datetime(df['data_registro'])
    df['data_atual'] = data_atual
    df['data_atual'] = pd.to_datetime(df['data_atual'])
    df.loc[df['tipo'] == 'Investimento', 'dif_dias'] = (data_atual - df.loc[df['tipo'] == 'Investimento', 'data_registro'].dt.date).dt.days
    taxa = 0.1 / 100
    df['rendimento'] = 0
    df['total+rendimento'] = 0
    df.loc[df['tipo'] == 'Investimento', 'rendimento'] = (df.loc[df['tipo'] == 'Investimento', 'valor'] * (1 + taxa) ** df.loc[df['tipo'] == 'Investimento', 'dif_dias']) - df.loc[df['tipo'] == 'Investimento', 'valor']
    df.loc[df['tipo'] == 'Investimento', 'total+rendimento'] = df.loc[df['tipo'] == 'Investimento', 'valor'] * (1 + taxa) ** df.loc[df['tipo'] == 'Investimento', 'dif_dias']


    montante = df['total+rendimento'].sum()
    montante_formatado = "{:.2f}".format(montante)
    rendimento = df['rendimento'].sum()
    rendimento_formatado = "{:.2f}".format(rendimento)
    total_investido = montante - rendimento
    total_investido_formatado = "{:.2f}".format(total_investido)

    st.write(f"Valor investido: R${total_investido_formatado}")
    st.write(f"Montante: R${montante_formatado}")
    st.write(f"Rendimento de: R${rendimento_formatado}")
    df_show = df.set_index('id_registro')
    df_show = df_show.copy()
    df_show = df_show.drop(columns=['dia', 'mes', 'ano'])
    st.dataframe(df_show.loc[df_show['tipo'] == 'Investimento'])

    return montante_formatado


def cabecalho_crud(titulo):
    st.title(f"{titulo} - PyBank")

    id_usuario = st.text_input("Informe o ID do Usuário:")

    if not id_usuario:
        st.warning("Por favor, informe o ID do usuário.")
        st.stop()

    registros_geral = ler_em_json('registros.json')
    registros = [registro for registro in registros_geral if registro['id_usuario'] == id_usuario]

    if titulo != "Área de Investimentos" and titulo != "Adicionar Registro":
        df = pd.DataFrame(registros)
        try:
            capital = (df.loc[df['tipo'] == 'Receita', 'valor'].sum()) + (df.loc[df['tipo'] == 'Despesa', 'valor'].sum())
            st.subheader(f"Capital: R${capital}")
        except:
            pass

    return id_usuario, registros_geral, registros

# Função principal do aplicativo
def main():
    menu = st.sidebar.selectbox(
        "Selecione uma opção:",
        ["Adicionar Registro", "Visualizar Registros", "Editar Registro", "Deletar Registro"]
    )

    st.sidebar.markdown("---")
    botao_investimentos = st.sidebar.button("Área de Investimentos")
    st.sidebar.markdown("---")

    if botao_investimentos:
        id_usuario, registros_geral, registros = cabecalho_crud("Área de Investimentos")
        conferir_se_tem_investimento = [registro for registro in registros if registro['tipo'] == "Investimento"]

        if conferir_se_tem_investimento != []:
            atualizar_rendimento(registros)
        elif conferir_se_tem_investimento == [] and registros != []:
            st.warning("Este usuário não possui investimentos")
        else:
            st.warning("ID de Usuário inexistente")

    else:
        if menu == "Adicionar Registro":
            id_usuario, registros_geral, registros = cabecalho_crud(menu)
            adicionar_registro(id_usuario, registros_geral)

        elif menu == "Visualizar Registros":
            id_usuario, registros_geral, registros = cabecalho_crud(menu)
            if registros != []:
                visualizar_registros(registros)
            else:
                st.warning("ID de Usuário inexistente")

        elif menu == "Editar Registro":
            id_usuario, registros_geral, registros = cabecalho_crud(menu)
            if registros != []:
                editar_registro(id_usuario, registros_geral)
            else:
                st.warning("ID de Usuário inexistente")

        elif menu == "Deletar Registro":
            id_usuario, registros_geral, registros = cabecalho_crud(menu)
            if registros != []:
                deletar_registro(id_usuario, registros_geral)
            else:
                st.warning("ID de Usuário inexistente")


if __name__ == "__main__":
    main()
