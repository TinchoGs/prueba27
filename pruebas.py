import streamlit as st
import pandas as pd

# Función para cargar la tabla de artículos
def cargar_articulos():
    # Simula la carga de datos desde Google Sheets
    data = {
        'Articulo': ['Producto 1', 'Producto 2', 'Producto 3'],
        'Precio': [100, 200, 300]
    }
    return pd.DataFrame(data)

# Cargar los artículos en un DataFrame
df_articulos = cargar_articulos()

# Título de la aplicación
st.title("Carrito de Compras")

# Mostrar los artículos disponibles
st.write("Selecciona los artículos para agregar al carrito:")

# Mostrar la tabla de artículos con sus precios
st.dataframe(df_articulos)

# Selección de artículos
articulos_seleccionados = st.multiselect(
    'Selecciona los artículos', df_articulos['Articulo'].tolist())

# Crear una tabla para que el usuario ingrese la cantidad de cada artículo seleccionado
cantidades = {}
total_por_articulo = {}

if articulos_seleccionados:
    st.subheader("Tu carrito de compras:")
    for articulo in articulos_seleccionados:
        cantidad = st.number_input(f'Cantidad de {articulo}', min_value=0, value=1)
        cantidades[articulo] = cantidad
        precio = df_articulos.loc[df_articulos['Articulo'] == articulo, 'Precio'].values[0]
        total_por_articulo[articulo] = precio * cantidad

    # Mostrar resumen del carrito
    for articulo, total in total_por_articulo.items():
        st.write(f"{articulo} - Cantidad: {cantidades[articulo]} - Total: ${total}")

    # Calcular el total general
    total_general = sum(total_por_articulo.values())
    st.write(f"**Total de la cotización: ${total_general}**")

# Botón para finalizar la cotización
if st.button("Finalizar cotización"):
    st.success("¡Cotización finalizada!")
    st.write(f"Total final: ${total_general}")
