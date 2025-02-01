import pandas as pd
import streamlit as st
import webbrowser
import datetime as datetime
import pydeck


st.set_page_config(
    page_title='Inicial',
    page_icon='🗺️',
    layout='wide'
)

df_BaseGeral = pd.read_csv('BaseLatLong_SP_2.csv',
                           sep=';', decimal=',', index_col=0)

st.markdown('# Mapa de REPPresentantes 💊')
btn = st.button('Acesse nosso site')  # use_container_width=True)
if btn:
    webbrowser.open_new_tab('www.Repp.com')


# Create an empty DataFrame to store filtered data
df_Filtrado = pd.DataFrame()

# Initialize the Inicializacao variable
Inicializacao = None

# Get a list of unique UF options from the original DataFrame
Opcoes_UFs = df_BaseGeral['ESTADO'].unique()

# Create a multi-select widget to select UF
UF_Selecionado = list(st.sidebar.segmented_control(
    "Selecione as UFs", Opcoes_UFs, selection_mode='multi'))

# Create a flag to track if the UF select has been changed
UF_Selecionado_Alterado = False

# If the user selects one or more UF:
if UF_Selecionado:
    # Set the flag to indicate the colUFor select has been changed
    UF_Selecionado_Alterado = True

    # Filter the original DataFrame to only include rows with the selected UF
    df_Filtrado = df_BaseGeral[df_BaseGeral['ESTADO'].isin(UF_Selecionado)]

    # Get a list of unique CIDADES options from the filtered DataFrame
    Opcoes_Cidades = df_Filtrado['CIDADE'].unique()

    # Create a multi-select widget to select CIDADES
    Cidade_Selecionado = st.sidebar.multiselect(
        "Selecione as Cidades", Opcoes_Cidades)

    df_BaseGeral = df_BaseGeral[df_BaseGeral['CIDADE'].isin(
        Cidade_Selecionado)]

    Colunas = ['ESPECIALIDADE', 'CRM', 'BAIRRO', 'CIDADE', 'ESTADO']
    st.dataframe(df_BaseGeral[Colunas], use_container_width=True)
    # st.map(df_BaseGeral)

else:
    Colunas = ['ESPECIALIDADE', 'CRM', 'BAIRRO', 'CIDADE', 'ESTADO']
    st.dataframe(df_BaseGeral[Colunas], use_container_width=True)
    # st.map(df_BaseGeral)


point_layer = pydeck.Layer(
    "ScatterplotLayer",
    data=df_BaseGeral,
    id="CRM",
    get_position=["LON", "LAT"],
    get_color="[255, 75, 75]",
    pickable=True,
    auto_highlight=True,
    get_radius="Tamanho",
)

view_state = pydeck.ViewState(
    latitude=-23, longitude=-46, controller=True, zoom=3.5, pitch=30
)

chart = pydeck.Deck(
    point_layer,
    initial_view_state=view_state,
    tooltip={"text": "{CIDADE}, {ESTADO}\nNúmero de Médicos: {Tamanho}"},
    map_style=None,
)

event = st.pydeck_chart(chart, on_select="rerun",
                        selection_mode="multi-object")

event.selection

st.sidebar.markdown('Desenvolvido por [Repp] (www.Repp.com.br)')
