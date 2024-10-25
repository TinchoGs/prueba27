import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
from streamlit_gsheets import GSheetsConnection
from st_aggrid import AgGrid, GridUpdateMode
from st_aggrid.grid_options_builder import GridOptionsBuilder
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Image, Table, TableStyle, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.units import inch
from io import BytesIO

# Configuración de la página
st.set_page_config(layout="wide")

# Creamos un objeto de sesión
session_state = st.session_state

st.title("Productos Almar")

# Lee el archivo CSV
conn = st.connection("gsheets", type=GSheetsConnection)
df = conn.read(worksheet='Productos')

# Agrega una nueva columna llamada "categoria_producto"  y guarda las letras del codigo
df['Categoria Producto'] = df.iloc[:, 0].str.extract(r'^([a-zA-Z]*)', expand=False)
# Elimina la columna "categoria_producto" de su posición actual
categoria_producto = df.pop('Categoria Producto')

# Inserta la columna "categoria_producto" en la posición 2
df.insert(1, 'Categoria Producto', categoria_producto)


st.session_state.reset_filtros = False

col1, col2, col3, col4, col5, col6,col7,col8 = st.columns(8)

# Botón para resetear los filtros
if st.button('Resetear filtros'):
    # Resetea la sesión de filtros y selecciona todos los valores por defecto
    st.session_state.reset_filtros = True
    st.session_state.codigo_seleccionado = 'Todos'
    st.session_state.categoria_seleccionada = 'Todos'
    st.session_state.tela_madre_seleccionado = 'Todos'
    st.session_state.tela_seleccionada = 'Todos'
    st.session_state.corte_seleccionado = 'Todos'
    st.session_state.ancho_seleccionado = 'Todos'
    st.session_state.peso_seleccionado = 'Todos'
    # Asigna el dataframe original a la variable df_filtrado
    df_filtrado = df

# Filtro por código
with col1:
    # Crea un selectbox para seleccionar el código
    codigo_seleccionado = st.selectbox('Filtrar por código', ['Todos'] + df['Codigo'].dropna().unique().tolist(), key='codigo_seleccionado')
    # Si se ha reseteado el filtro, selecciona 'Todos'
    if st.session_state.reset_filtros:
        codigo_seleccionado = 'Todos'

# Filtro por código
if codigo_seleccionado == 'Todos':
    # Si se selecciona 'Todos', asigna el dataframe original a df_codigo
    df_codigo = df
else:
    # Si se selecciona un código específico, filtra el dataframe por ese código
    df_codigo = df.loc[df['Codigo'] == codigo_seleccionado]

# Filtro por categoría
with col2:
    # Crea un selectbox para seleccionar la categoría
    categoria_seleccionada = st.selectbox('Filtrar por categoría', ['Todos'] + df_codigo['Categoria Producto'].dropna().unique().tolist(), key='categoria_seleccionada')
    # Si se ha reseteado el filtro, selecciona 'Todos'
    if st.session_state.reset_filtros:
        categoria_seleccionada = 'Todos'

# Filtro por categoría
if categoria_seleccionada == 'Todos':
    # Si se selecciona 'Todos', asigna el dataframe df_codigo a df_categoria
    df_categoria = df_codigo
else:
    # Si se selecciona una categoría específica, filtra el dataframe por esa categoría
    df_categoria = df_codigo.loc[df_codigo['Categoria Producto'] == categoria_seleccionada]

# Filtro por tela madre
with col3:
    # Crea un selectbox para seleccionar la tela madre
    tela_madre_seleccionado = st.selectbox('Filtrar por Tela Madre', ['Todos'] + df_categoria['Tela Madre'].dropna().unique().tolist(), key='tela_madre_seleccionado')
    # Si se ha reseteado el filtro, selecciona 'Todos'
    if st.session_state.reset_filtros:
        tela_madre_seleccionado = 'Todos'

# Filtro por tela madre
if 'Tela Madre' in df_categoria.columns:
    if tela_madre_seleccionado == 'Todos':
        df_tela_madre = df_categoria
    else:
        df_tela_madre = df_categoria.loc[(df_categoria['Tela Madre'] == tela_madre_seleccionado) | (df_categoria['Tela Madre'].isna())]
else:
    print("Error: La columna 'Tela Madre' no existe en el DataFrame.")
    # Maneja el error o proporciona un valor predeterminado
    df_tela_madre = df_categoria

# Filtro por tela
with col4:
    tela_seleccionada = st.selectbox('Filtrar por tela', ['Todos'] + df_tela_madre['Tela'].dropna().unique().tolist(), key='tela_seleccionada')
    if st.session_state.reset_filtros:
        tela_seleccionada = 'Todos'

# Filtro por tela
if tela_seleccionada == 'Todos':
    df_tela = df_tela_madre
else:
    df_tela = df_tela_madre.loc[df_tela_madre['Tela'] == tela_seleccionada]

# Filtro por corte
with col5:
    # Crea un selectbox para seleccionar el corte
    corte_seleccionado = st.selectbox('Filtrar por corte', ['Todos'] + df_tela['Corte'].dropna().unique().tolist(), key='corte_seleccionado')
    # Si se ha reseteado el filtro, selecciona 'Todos'
    if st.session_state.reset_filtros:
        corte_seleccionado = 'Todos'

# Filtro por corte
if corte_seleccionado == 'Todos':
    # Si se selecciona 'Todos', asigna el dataframe df_tela_madre a df_corte
    df_corte = df_tela
else:
    # Si se selecciona un corte específico, filtra el dataframe por ese corte
    df_corte = df_tela.loc[df_tela['Corte'] == corte_seleccionado]
# Filtro por ancho
with col6:
     # Crea un selectbox para seleccionar el ancho
    ancho_seleccionado = st.selectbox('Filtrar por ancho', ['Todos'] + df_corte['Ancho'].dropna().unique().tolist(), key='ancho_seleccionado')
    if st.session_state.reset_filtros:
        ancho_seleccionado = 'Todos'
#  Si la variable de sesión "reset_filtros" es True, se resetea el valor seleccionado en el selectbox a "Todos"
    if st.session_state.reset_filtros:
        ancho_seleccionado = 'Todos'

#  Se filtra el dataframe según el valor seleccionado en el selectbox de ancho
if ancho_seleccionado == 'Todos':  
    df_ancho = df_corte  # . Si se seleccionó "Todos", se asigna el dataframe original a df_ancho
else:
    df_ancho = df_corte.loc[df_corte['Ancho'] == ancho_seleccionado]  #  Si se seleccionó un valor específico, se filtra el dataframe por ancho

# Filtro por peso
with col7:
    peso_seleccionado = st.selectbox('Filtrar por peso', ['Todos'] + df_ancho['Peso'].dropna().unique().tolist(), key='peso_seleccionado')
    if st.session_state.reset_filtros:
        peso_seleccionado = 'Todos'

# Se filtra el dataframe según el valor seleccionado en el selectbox de peso
if peso_seleccionado == 'Todos':
    df_peso = df_ancho
else:
    df_peso = df_ancho.loc[df_ancho['Peso'] == peso_seleccionado]


# Filtro por color
with col8:
    color_seleccionado = st.selectbox('Filtrar por color', ['Todos'] + df_peso['Color'].dropna().unique().tolist(), key='color_seleccionado')
    if st.session_state.reset_filtros:
        color_seleccionado = 'Todos'

# Filtro por color
if color_seleccionado == 'Todos':
    df_color = df_peso
else:
    df_color = df_peso.loc[df_peso['Color'] == color_seleccionado]

# Asigna el dataframe filtrado final
df_filtrado = df_color
df_filtrado = df_filtrado.loc[:, ['Codigo', 'Articulo', 'Tela Madre', 'Tela', 'Precio/USD', 'PrecioKg/USD','Corte','Ancho','Peso','Color']]
gd = GridOptionsBuilder.from_dataframe(df_filtrado)
gd.configure_pagination(enabled=True)
gd.configure_default_column(editable=False, groupable=True)
# Configura una columna especifica para que tenga un fondo diferente

gd.configure_selection(selection_mode='multiple', use_checkbox=True)
gridoptions = gd.build()

filas_seleccionadas = []  # Inicializa la lista vacía
# Almacenar las filas seleccionadas en la variable de sesión
if 'filas_seleccionadas' not in st.session_state:
    st.session_state.filas_seleccionadas = []

# Cuando los filtros cambian, restaurar las filas seleccionadas
if st.session_state.reset_filtros:
    filas_seleccionadas = st.session_state.filas_seleccionadas
else:
    filas_seleccionadas = []

grid_table = AgGrid(
    df_filtrado,
    gridOptions=gridoptions,
    selected_rows=filas_seleccionadas  # Restaurar las filas seleccionadas
)

# Cuando el usuario selecciona filas, actualizar la variable de sesión
if grid_table['selected_rows'] is not None:
    selected_rows = grid_table['selected_rows']
    filas_seleccionadas = [fila[0] for fila in selected_rows]
    st.session_state.filas_seleccionadas = filas_seleccionadas

tipo_venta = st.selectbox('Tipo de venta', ['Venta por peso', 'Venta por unidad', 'Venta por metro'])

# Almacenar los artículos seleccionados en la variable de sesión
articulo_seleccionado_df = grid_table['selected_rows']
articulo_seleccionado_df = pd.DataFrame(articulo_seleccionado_df)

# Verifica si la lista 'carrito' ya existe en la sesión, si no, inicialízala
if 'carrito' not in st.session_state:
    st.session_state.carrito = pd.DataFrame()  # El carrito inicialmente es un DataFrame vacío

# Función para agregar productos seleccionados al carrito
def agregar_al_carrito(nuevos_articulos):
    if not nuevos_articulos.empty:  # Si hay artículos seleccionados
        # Concatenar los artículos seleccionados al carrito almacenado en la sesión
        st.session_state.carrito = pd.concat([st.session_state.carrito, nuevos_articulos]).drop_duplicates().reset_index(drop=True)

# Almacena los artículos seleccionados
articulo_seleccionado_df = pd.DataFrame(grid_table['selected_rows'])
if st.button("Agregar al carrito"):
    # Verificar si se han seleccionado nuevos artículos antes de agregar al carrito
    if not articulo_seleccionado_df.empty:
        agregar_al_carrito(articulo_seleccionado_df)

# Mantener el contenido del carrito incluso cuando se cambian los filtros o se resetean
if not st.session_state.carrito.empty:
    # Selecciona las columnas necesarias para la cotización del producto según el tipo de venta
    if tipo_venta == 'Venta por unidad':
        carrito_df = pd.DataFrame(st.session_state.carrito[['Articulo', 'Precio/USD']])
        carrito_df['Cantidad'] = 1  # Inicializa la columna "Cantidad" con un valor predeterminado de 1
        carrito_go = GridOptionsBuilder.from_dataframe(carrito_df)
        carrito_go.configure_column("Cantidad", editable=True)  # Habilita la edición para la columna "Cantidad"
        carrito_go.configure_column("Precio/USD", editable=True)
        carrito_go.configure_columns(['Articulo', 'Cantidad', 'Precio/USD'], columns_to_display='visible')

    elif tipo_venta == 'Venta por peso':
        carrito_df = pd.DataFrame(st.session_state.carrito[['Articulo', 'PrecioKg/USD']])
        carrito_df['Kg_vender'] = 1 # Inicializa la columna "Kg_vender" con un valor predeterminado de 1
        carrito_go = GridOptionsBuilder.from_dataframe(carrito_df)
        carrito_go.configure_column("Kg_vender", editable=True)
        carrito_go.configure_column("PrecioKg/USD", editable=True)
        carrito_go.configure_columns(['Articulo', 'Kg_vender', 'PrecioKg/USD'], columns_to_display='visible')

    elif tipo_venta == 'Venta por metro':
        carrito_df = pd.DataFrame(st.session_state.carrito[['Articulo', 'Precio/USD']])
        carrito_df['Metros_vender'] = 1  # Inicializa la columna "Metros_vender" con un valor predeterminado de 1
        carrito_go = GridOptionsBuilder.from_dataframe(carrito_df)
        carrito_go.configure_column("Metros_vender", editable=True)
        carrito_go.configure_column("Precio/USD", editable=True)
        carrito_go.configure_columns(['Articulo', 'Metros_vender', 'Precio/USD'], columns_to_display='visible')

    carrito_go.configure_default_column(editable=False)
    carrito_go.configure_selection(selection_mode='multiple', use_checkbox=True)
    # Configurar las opciones de edición para el AgGrid

    
    carrito_lindo = AgGrid(
        st.session_state.carrito,
        gridOptions=carrito_go.build(),
        update_mode=GridUpdateMode.MODEL_CHANGED,
        allow_unsafe_jscode=True,
        reload_data=True
    )

if st.button("Eliminar"):
    if carrito_lindo['selected_rows'] is not None and not carrito_lindo['selected_rows'].empty:
        # Convertir los artículos seleccionados a un DataFrame
        articulos_seleccionados = pd.DataFrame(carrito_lindo['selected_rows'])
        
        # Filtrar el carrito para eliminar los artículos seleccionados
        st.session_state.carrito = st.session_state.carrito[~st.session_state.carrito['Articulo'].isin(articulos_seleccionados['Articulo'])]
        st.rerun()
    else:
        st.warning("Por favor, selecciona al menos un artículo para eliminar.")

        # Cálculo del total a pagar
if tipo_venta == 'Venta por unidad':
    if st.button("Calcular"):
        calculo_carrito_lindo = pd.DataFrame(carrito_lindo['data'])
        if 'Cantidad' not in calculo_carrito_lindo.columns or calculo_carrito_lindo['Cantidad'].isna().any():
            st.warning('Llene los campos de cantidad.')
        else:
            cotiza_df = pd.DataFrame(carrito_lindo.data[["Articulo", "Precio/USD", "Cantidad"]])
            cotiza_df["Total"] = cotiza_df.apply(lambda row: float(row["Precio/USD"]) * float(row["Cantidad"]), axis=1)
            st.write(cotiza_df)
            total = (cotiza_df['Total']).sum()
            st.write(f"Total a pagar: ${total:.2f}")
            pagesize = letter
            leftMargin = 18  # 1 pulgada   
            rightMargin = 18  # 1 pulgada
            topMargin = 180 # 1 pulgada
            bottomMargin = 0  # 1 pulgada           
            
        data = [
                ['Articulo', 'Precio/USD', 'Cantidad', 'Total']
            ]

   
        for index, row in cotiza_df.iterrows():
    # Asegúrate de que estás accediendo a los valores correctamente
            data.append([row["Articulo"], row["Precio/USD"], row["Cantidad"],  row["Total"]])

            




        tablo = Table(data)

    # Estilo de la tabla
        style = TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.black),  # Fila de encabezado
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ])
        tablo.setStyle(style)

        pdf_buffer = BytesIO()

        doc = SimpleDocTemplate(pdf_buffer, pagesize=pagesize, leftMargin=leftMargin, rightMargin=rightMargin,
                                topMargin=topMargin, bottomMargin=bottomMargin)

# Crea un estilo de texto
        styles = getSampleStyleSheet()
        style = styles["BodyText"]

# Crea un párrafo de texto

# Función para dibujar en el PDF
        def draw(c, doc):
    # Dibuja la imagen en la posición deseada
                

    # Dibuja una línea
                
            width, height = letter

    # Dibujar un borde
            c.setStrokeColor(colors.black)
            c.rect(0.5 * inch, 0.5 * inch, width - 1 * inch, height - 1 * inch)

    # Logo de la empresa
            #c.drawImage("img/logo_Almar.png", 0.7 * inch, height - 1.5 * inch, width=1 * inch, height=0.9 * inch)

    # Título y pretexto
            #c.setFont("HandelGothic BT", 16)
            c.drawString(1.8 * inch, height - 1 * inch, "Ricardo Almar E Hijos S.A")

            #c.setFont("HandelGothic BT", 12)
            c.drawString(1.8 * inch, height - 1.2 * inch, "Telas - Envases - Estructuras Flexibles")

            #c.drawImage("img/logo_Almar.png", 1.7 * inch, height - 7 * inch, width=3 * inch, height=3 * inch)



            cliente_data = [
                ["CLIENTE","CUENTA"],
                ["XXXXXXX","XXXXXX"],
            ]

            col_widths = [439.8, 100]
    
            table = Table(cliente_data, colWidths=col_widths)
            table.setStyle(TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (4, -6), (-1, -1), 'CENTER'),
                ('CELLPADDING', (0, 0), (-1, -1), 10),
                ('FONTNAME', (0, 0), (0, 0), 'Helvetica-Bold'),  
                ('BACKGROUND', (0, 0),(-1, 0), colors.black),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTNAME', (0, 6), (0, 6), 'Helvetica-Bold'),
                ('FONTNAME', (1, 6), (1, 6), 'Helvetica-Bold'),
                ('GRID', (0, 0), (-1, -1), 0, colors.black),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        
            ]))
    
    # Dibujar la tabla de información de contacto
            table.wrapOn(c, width, height)
            table.drawOn(c, 0.5 * inch, height - 2.2 * inch) # Coordenadas y tamaño del rectángulo
        elementos = [tablo]  # Solo el párrafo, la imagen se dibuja en la función draw
        doc.build(elementos, onFirstPage=draw, onLaterPages=draw)
        pdf_buffer.seek(0)
        
        st.download_button(
            label="Descargar Cotización",
            data=pdf_buffer,
            file_name="Cotizacion.pdf",
            mime="application/pdf"
        )









        
            
          
elif tipo_venta == 'Venta por peso':
    if st.button("Calcular"):
        calculo_carrito_lindo = pd.DataFrame(carrito_lindo['data'])
        if 'Kg_vender' not in calculo_carrito_lindo.columns or calculo_carrito_lindo['Kg_vender'].isna().any():
            st.warning('Llene los campos de Kg_vender.')
        else:
            cotiza_df = pd.DataFrame(carrito_lindo.data[["Articulo", "PrecioKg/USD", "Kg_vender"]])
            cotiza_df["Total"] = cotiza_df.apply(lambda row: float(row["PrecioKg/USD"]) * float(row["Kg_vender"]), axis=1)
            st.write(cotiza_df)
            total = (cotiza_df['Total']).sum()
            st.write(f"Total a pagar: ${total:.2f}")
            pagesize = letter
            leftMargin = 18  # 1 pulgada   
            rightMargin = 18  # 1 pulgada
            topMargin = 180 # 1 pulgada
            bottomMargin = 0  # 1 pulgada           
            
        data = [
                ['Articulo', 'PrecioKg/USD', 'Kg_vender', 'Total']
            ]

   
        for index, row in cotiza_df.iterrows():
    # Asegúrate de que estás accediendo a los valores correctamente
            data.append([row["Articulo"], row["PrecioKg/USD"], row["Kg_vender"],  row["Total"]])

            




        tablo = Table(data)

    # Estilo de la tabla
        style = TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.black),  # Fila de encabezado
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ])
        tablo.setStyle(style)

        pdf_buffer = BytesIO()

        doc = SimpleDocTemplate(pdf_buffer, pagesize=pagesize, leftMargin=leftMargin, rightMargin=rightMargin,
                                topMargin=topMargin, bottomMargin=bottomMargin)

# Crea un estilo de texto
        styles = getSampleStyleSheet()
        style = styles["BodyText"]

# Crea un párrafo de texto

# Función para dibujar en el PDF
        def draw(c, doc):
    # Dibuja la imagen en la posición deseada
                

    # Dibuja una línea
                
            width, height = letter

    # Dibujar un borde
            c.setStrokeColor(colors.black)
            c.rect(0.5 * inch, 0.5 * inch, width - 1 * inch, height - 1 * inch)

    # Logo de la empresa
            #c.drawImage("img/logo_Almar.png", 0.7 * inch, height - 1.5 * inch, width=1 * inch, height=0.9 * inch)

    # Título y pretexto
            #c.setFont("HandelGothic BT", 16)
            c.drawString(1.8 * inch, height - 1 * inch, "Ricardo Almar E Hijos S.A")

            #c.setFont("HandelGothic BT", 12)
            c.drawString(1.8 * inch, height - 1.2 * inch, "Telas - Envases - Estructuras Flexibles")

            #c.drawImage("img/logo_Almar.png", 1.7 * inch, height - 7 * inch, width=3 * inch, height=3 * inch)



            cliente_data = [
                ["CLIENTE","CUENTA"],
                ["XXXXXXX","XXXXXX"],
            ]

            col_widths = [439.8, 100]
    
            table = Table(cliente_data, colWidths=col_widths)
            table.setStyle(TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (4, -6), (-1, -1), 'CENTER'),
                ('CELLPADDING', (0, 0), (-1, -1), 10),
                ('FONTNAME', (0, 0), (0, 0), 'Helvetica-Bold'),  
                ('BACKGROUND', (0, 0),(-1, 0), colors.black),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTNAME', (0, 6), (0, 6), 'Helvetica-Bold'),
                ('FONTNAME', (1, 6), (1, 6), 'Helvetica-Bold'),
                ('GRID', (0, 0), (-1, -1), 0, colors.black),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        
            ]))
    
    # Dibujar la tabla de información de contacto
            table.wrapOn(c, width, height)
            table.drawOn(c, 0.5 * inch, height - 2.2 * inch) # Coordenadas y tamaño del rectángulo
        elementos = [tablo]  # Solo el párrafo, la imagen se dibuja en la función draw
        doc.build(elementos, onFirstPage=draw, onLaterPages=draw)
        pdf_buffer.seek(0)
        
        st.download_button(
            label="Descargar Cotización",
            data=pdf_buffer,
            file_name="Cotizacion.pdf",
            mime="application/pdf"
        )












          

elif tipo_venta == 'Venta por metro':
    if st.button("Calcular"):
        calculo_carrito_lindo = pd.DataFrame(carrito_lindo['data'])
        if 'Metros_vender' not in calculo_carrito_lindo.columns or calculo_carrito_lindo['Metros_vender'].isna().any():
            st.warning('Llene los campos de Metros_vender.')
        else:
            cotiza_df = pd.DataFrame(carrito_lindo.data[["Articulo", "Precio/USD", "Metros_vender"]])
            cotiza_df["Total"] = cotiza_df.apply(lambda row: float(row["Precio/USD"]) * float(row["Metros_vender"]), axis=1)
            st.write(cotiza_df)
            total = (cotiza_df['Total']).sum()
            st.write(f"Total a pagar: ${total:.2f}")
            pagesize = letter
            leftMargin = 18  # 1 pulgada   
            rightMargin = 18  # 1 pulgada
            topMargin = 180 # 1 pulgada
            bottomMargin = 0  # 1 pulgada           
            
        data = [
                ['Articulo', 'Precio/USD', 'Metros_vender', 'Total']
            ]

   
        for index, row in cotiza_df.iterrows():
    # Asegúrate de que estás accediendo a los valores correctamente
            data.append([row["Articulo"], row["Precio/USD"], row["Metros_vender"],  row["Total"]])

            




        tablo = Table(data)

    # Estilo de la tabla
        style = TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.black),  # Fila de encabezado
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ])
        tablo.setStyle(style)

        pdf_buffer = BytesIO()

        doc = SimpleDocTemplate(pdf_buffer, pagesize=pagesize, leftMargin=leftMargin, rightMargin=rightMargin,
                                topMargin=topMargin, bottomMargin=bottomMargin)

# Crea un estilo de texto
        styles = getSampleStyleSheet()
        style = styles["BodyText"]

# Crea un párrafo de texto

# Función para dibujar en el PDF
        def draw(c, doc):
    # Dibuja la imagen en la posición deseada
                

    # Dibuja una línea
                
            width, height = letter

    # Dibujar un borde
            c.setStrokeColor(colors.black)
            c.rect(0.5 * inch, 0.5 * inch, width - 1 * inch, height - 1 * inch)

    # Logo de la empresa
            #c.drawImage("img/logo_Almar.png", 0.7 * inch, height - 1.5 * inch, width=1 * inch, height=0.9 * inch)

    # Título y pretexto
            #c.setFont("HandelGothic BT", 16)
            c.drawString(1.8 * inch, height - 1 * inch, "Ricardo Almar E Hijos S.A")

            #c.setFont("HandelGothic BT", 12)
            c.drawString(1.8 * inch, height - 1.2 * inch, "Telas - Envases - Estructuras Flexibles")

            #c.drawImage("img/logo_Almar.png", 1.7 * inch, height - 7 * inch, width=3 * inch, height=3 * inch)



            cliente_data = [
                ["CLIENTE","CUENTA"],
                ["XXXXXXX","XXXXXX"],
            ]

            col_widths = [439.8, 100]
    
            table = Table(cliente_data, colWidths=col_widths)
            table.setStyle(TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (4, -6), (-1, -1), 'CENTER'),
                ('CELLPADDING', (0, 0), (-1, -1), 10),
                ('FONTNAME', (0, 0), (0, 0), 'Helvetica-Bold'),  
                ('BACKGROUND', (0, 0),(-1, 0), colors.black),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTNAME', (0, 6), (0, 6), 'Helvetica-Bold'),
                ('FONTNAME', (1, 6), (1, 6), 'Helvetica-Bold'),
                ('GRID', (0, 0), (-1, -1), 0, colors.black),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        
            ]))
    
    # Dibujar la tabla de información de contacto
            table.wrapOn(c, width, height)
            table.drawOn(c, 0.5 * inch, height - 2.2 * inch) # Coordenadas y tamaño del rectángulo
        elementos = [tablo]  # Solo el párrafo, la imagen se dibuja en la función draw
        doc.build(elementos, onFirstPage=draw, onLaterPages=draw)
        pdf_buffer.seek(0)
        
        st.download_button(
            label="Descargar Cotización",
            data=pdf_buffer,
            file_name="Cotizacion.pdf",
            mime="application/pdf"
        )

     






else:
    st.write("No hay artículos en el carrito.")


