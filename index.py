import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import hashlib

# Configuración de la página con tema personalizado
st.set_page_config(
    page_title="Facturador Inteligente",
    layout="wide",
    page_icon="🧾",
    initial_sidebar_state="expanded"
)

# Estilos CSS personalizados con diseño moderno
st.markdown("""
    <style>
    :root {
        --primary: #4361ee;
        --secondary: #3f37c9;
        --accent: #4895ef;
        --success: #4cc9f0;
        --danger: #f72585;
        --warning: #f8961e;
        --info: #43aa8b;
        --light: #f8f9fa;
        --dark: #212529;
    }
    
    .main {
        background-color: #f8f9fa;
    }
    
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #2b2d42 0%, #1a1a2e 100%);
        color: white;
    }
    
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    h1 {
        color: var(--primary);
        border-bottom: 3px solid var(--accent);
        padding-bottom: 12px;
        margin-bottom: 1.5rem;
    }
    
    h2 {
        color: var(--secondary);
        border-left: 4px solid var(--accent);
        padding-left: 12px;
        margin-top: 1.8rem;
    }
    
    .stMetric {
        background: white;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 6px 12px rgba(0,0,0,0.08);
        border-left: 4px solid var(--accent);
    }
    
    .stDataFrame {
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    }
    
    .success-box {
        background-color: #e6f7ee;
        color: #155724;
        padding: 16px;
        border-radius: 8px;
        margin: 12px 0;
        border-left: 4px solid #28a745;
    }
    
    .warning-box {
        background-color: #fff8e6;
        color: #856404;
        padding: 16px;
        border-radius: 8px;
        margin: 12px 0;
        border-left: 4px solid #ffc107;
    }
    
    .info-box {
        background-color: #e6f3ff;
        color: #0c5460;
        padding: 16px;
        border-radius: 8px;
        margin: 12px 0;
        border-left: 4px solid #17a2b8;
    }
    
    .danger-box {
        background-color: #fde8e8;
        color: #721c24;
        padding: 16px;
        border-radius: 8px;
        margin: 12px 0;
        border-left: 4px solid #dc3545;
    }
    
    .file-uploader {
        border: 2px dashed #4361ee;
        border-radius: 12px;
        padding: 30px;
        text-align: center;
        background-color: rgba(67, 97, 238, 0.05);
        margin-bottom: 2rem;
    }
    
    .file-uploader:hover {
        background-color: rgba(67, 97, 238, 0.1);
    }
    
    .stButton>button {
        background-color: var(--primary);
        color: white;
        border-radius: 8px;
        padding: 8px 16px;
        border: none;
        transition: all 0.3s;
    }
    
    .stButton>button:hover {
        background-color: var(--secondary);
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    
    .stSelectbox, .stMultiselect, .stTextInput, .stDateInput {
        border-radius: 8px !important;
    }
    
    .stTab {
        border-radius: 12px;
        overflow: hidden;
    }
    
    .stTab [role="tab"] {
        padding: 10px 16px;
        border-radius: 8px 8px 0 0;
        margin-right: 4px;
    }
    
    .stTab [aria-selected="true"] {
        background-color: var(--primary);
        color: white !important;
    }
    
    .metric-value {
        font-size: 2.2rem;
        font-weight: 700;
        color: var(--primary);
        text-align: center;
        margin: 10px 0;
    }
    
    .metric-label {
        font-size: 1rem;
        color: var(--dark);
        text-align: center;
        margin-bottom: 5px;
    }
    
    .welcome-container {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        border-radius: 16px;
        padding: 40px;
        text-align: center;
        box-shadow: 0 8px 16px rgba(0,0,0,0.05);
        margin: 2rem auto;
        max-width: 800px;
    }
    
    .welcome-icon {
        font-size: 4rem;
        color: var(--primary);
        margin-bottom: 1.5rem;
    }
    
    .welcome-title {
        color: var(--primary);
        margin-bottom: 1rem;
    }
    
    .welcome-subtitle {
        color: var(--secondary);
        margin-bottom: 2rem;
        font-size: 1.2rem;
    }
    
    .sidebar-section {
        margin-bottom: 1.5rem;
    }
    
    .sidebar-title {
        color: white;
        font-size: 1.1rem;
        font-weight: 600;
        margin-bottom: 0.8rem;
        display: flex;
        align-items: center;
    }
    
    .sidebar-title svg {
        margin-right: 8px;
    }
    </style>
    """, unsafe_allow_html=True)

# Título principal con gradiente y sombra
st.markdown("""
<div style="background: linear-gradient(135deg, #4361ee 0%, #3a0ca3 100%); 
            padding: 30px; 
            border-radius: 12px; 
            margin-bottom: 40px;
            box-shadow: 0 8px 16px rgba(0,0,0,0.1);">
    <h1 style="color:white; text-align:center; margin:0; font-size:2.5rem;">🧾 Facturador Inteligente</h1>
    <p style="color:rgba(255,255,255,0.9); text-align:center; font-size:1.2rem; margin:10px 0 0;">
        Sistema avanzado de gestión y análisis de facturas para contadores
    </p>
</div>
""", unsafe_allow_html=True)

# Función para convertir listas en strings para el hashing
def convert_lists_to_strings(df):
    for col in df.columns:
        if df[col].apply(lambda x: isinstance(x, list)).any():
            df[col] = df[col].apply(lambda x: '|'.join(map(str, x)) if isinstance(x, list) else x)
    return df

# Cargar archivo XLS con mejor manejo de errores
def cargar_datos(archivo):
    try:
        df = pd.read_excel(archivo, engine="xlrd")
        # Limpieza básica de datos
        df = df.dropna(how='all')
        df = df.fillna('')
        
        # Procesar relaciones si existe la columna
        if 'Relacionados' in df.columns:
            df['UUIDs_Relacionados'] = df['Relacionados'].str.findall(
                r'[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}'
            )
            # Convertir listas vacías a None
            df['UUIDs_Relacionados'] = df['UUIDs_Relacionados'].apply(lambda x: x if x else None)
        
        return convert_lists_to_strings(df)
    except Exception as e:
        st.error(f"❌ Error cargando archivo: {e}")
        return None

# Función segura para crear multiselect con estilo mejorado
def create_safe_multiselect(label, options, default_values=None):
    options = list(options)
    available_options = [str(opt) for opt in options]
    
    if default_values is None:
        default_values = []
    
    # Filtrar valores por defecto que existan en las opciones
    safe_defaults = [str(val) for val in default_values if str(val) in available_options]
    
    # Si no hay defaults válidos y hay opciones, usar las primeras 2 o 1
    if not safe_defaults and available_options:
        safe_defaults = available_options[:min(2, len(available_options))]
    
    return st.multiselect(
        label,
        options=available_options,
        default=safe_defaults,
        help=f"Seleccione uno o más {label.lower()}"
    )

# Diseño del uploader mejorado
with st.container():
    st.markdown("### 📤 Carga tu archivo de facturas")
    with st.container():
        archivo = st.file_uploader(
            "Arrastra o selecciona tu archivo Excel (.xls)",
            type=["xls"],
            help="El archivo debe contener columnas como UUID, Fecha, Método de Pago, etc.",
            key="file_uploader"
        )

if archivo:
    with st.spinner('🔍 Procesando archivo... Por favor espera'):
        df = cargar_datos(archivo)
    
    if df is not None:
        # Procesamiento inicial de datos
        if 'Fecha' in df.columns:
            df['Fecha'] = pd.to_datetime(df['Fecha'], errors='coerce')
            df['Mes'] = df['Fecha'].dt.to_period('M').astype(str)
        
        if 'XML' in df.columns:
            df['Mes_XML'] = df['XML'].str.extract(r'(\d{6})')
        
        # Sidebar con menú y filtros
        with st.sidebar:
            st.markdown("""
            <div class="sidebar-section">
                <div class="sidebar-title">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16">
                        <path d="M1 2.5A1.5 1.5 0 0 1 2.5 1h3A1.5 1.5 0 0 1 7 2.5v3A1.5 1.5 0 0 1 5.5 7h-3A1.5 1.5 0 0 1 1 5.5v-3zM2.5 2a.5.5 0 0 0-.5.5v3a.5.5 0 0 0 .5.5h3a.5.5 0 0 0 .5-.5v-3a.5.5 0 0 0-.5-.5h-3zm6.5.5A1.5 1.5 0 0 1 10.5 1h3A1.5 1.5 0 0 1 15 2.5v3A1.5 1.5 0 0 1 13.5 7h-3A1.5 1.5 0 0 1 9 5.5v-3zm1.5-.5a.5.5 0 0 0-.5.5v3a.5.5 0 0 0 .5.5h3a.5.5 0 0 0 .5-.5v-3a.5.5 0 0 0-.5-.5h-3zM1 10.5A1.5 1.5 0 0 1 2.5 9h3A1.5 1.5 0 0 1 7 10.5v3A1.5 1.5 0 0 1 5.5 15h-3A1.5 1.5 0 0 1 1 13.5v-3zm1.5-.5a.5.5 0 0 0-.5.5v3a.5.5 0 0 0 .5.5h3a.5.5 0 0 0 .5-.5v-3a.5.5 0 0 0-.5-.5h-3zm6.5.5A1.5 1.5 0 0 1 10.5 9h3a1.5 1.5 0 0 1 1.5 1.5v3a1.5 1.5 0 0 1-1.5 1.5h-3A1.5 1.5 0 0 1 9 13.5v-3zm1.5-.5a.5.5 0 0 0-.5.5v3a.5.5 0 0 0 .5.5h3a.5.5 0 0 0 .5-.5v-3a.5.5 0 0 0-.5-.5h-3z"/>
                    </svg>
                    Menú Principal
                </div>
            """, unsafe_allow_html=True)
            
            menu = st.selectbox("", [
                "Resumen General",
                "Facturas Emitidas",
                "Complementos de Pago", 
                "Gestión PPD/PUE"
            ], index=0, label_visibility="collapsed")
            
            st.markdown("""
            <div class="sidebar-section">
                <div class="sidebar-title">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16">
                        <path d="M11.742 10.344a6.5 6.5 0 1 0-1.397 1.398h-.001c.03.04.062.078.098.115l3.85 3.85a1 1 0 0 0 1.415-1.414l-3.85-3.85a1.007 1.007 0 0 0-.115-.1zM12 6.5a5.5 5.5 0 1 1-11 0 5.5 5.5 0 0 1 11 0z"/>
                    </svg>
                    Filtros Generales
                </div>
            """, unsafe_allow_html=True)
            
            # Filtro de estatus seguro
            if 'Estatus' in df.columns:
                estatus_options = df['Estatus'].unique()
                estatus_filtro = create_safe_multiselect(
                    "Estatus",
                    options=estatus_options,
                    default_values=["Vigente", "Cancelado"]
                )
            
            # Filtro por rango de fechas
            if 'Fecha' in df.columns:
                min_date = df['Fecha'].min()
                max_date = df['Fecha'].max()
                if pd.notna(min_date) and pd.notna(max_date):
                    min_date = min_date.to_pydatetime()
                    max_date = max_date.to_pydatetime()
                    st.markdown("**Rango de fechas**")
                    fecha_range = st.date_input(
                        "",
                        value=[min_date, max_date],
                        min_value=min_date,
                        max_value=max_date,
                        label_visibility="collapsed"
                    )
            
            st.markdown("""
            <div class="sidebar-section">
                <div class="sidebar-title">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16">
                        <path d="M.5 9.9a.5.5 0 0 1 .5.5v2.5a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1v-2.5a.5.5 0 0 1 1 0v2.5a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2v-2.5a.5.5 0 0 1 .5-.5z"/>
                        <path d="M7.646 1.146a.5.5 0 0 1 .708 0l3 3a.5.5 0 0 1-.708.708L8.5 2.707V11.5a.5.5 0 0 1-1 0V2.707L5.354 4.854a.5.5 0 1 1-.708-.708l3-3z"/>
                    </svg>
                    Exportar Datos
                </div>
            """, unsafe_allow_html=True)
            
            if st.button("Exportar a CSV", key="export_btn"):
                @st.cache_data
                def convert_df_to_csv(df):
                    return df.to_csv(index=False).encode('utf-8')
                
                csv = convert_df_to_csv(df)
                st.download_button(
                    "Descargar CSV",
                    data=csv,
                    file_name="facturas_filtradas.csv",
                    mime="text/csv",
                    key="download_btn"
                )

        # Aplicar filtros básicos
        df_filtrado = df.copy()
        if 'Estatus' in df.columns and 'estatus_filtro' in locals():
            df_filtrado = df_filtrado[df_filtrado['Estatus'].isin(estatus_filtro)]
        if 'Fecha' in df.columns and 'fecha_range' in locals() and len(fecha_range) == 2:
            df_filtrado = df_filtrado[
                (df_filtrado['Fecha'] >= pd.to_datetime(fecha_range[0])) & 
                (df_filtrado['Fecha'] <= pd.to_datetime(fecha_range[1]))
            ]

        # Página de Resumen General
        if menu == "Resumen General":
            st.markdown("## 📊 Resumen General")
            
            # Métricas clave en tarjetas estilizadas
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.markdown('<div class="metric-label">Total Facturas</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="metric-value">{len(df)}</div>', unsafe_allow_html=True)
                st.markdown('<div style="text-align:center;color:#6c757d;">Registros cargados</div>', unsafe_allow_html=True)
            
            with col2:
                if 'Estatus' in df.columns:
                    vigentes = len(df[df['Estatus'].astype(str).str.contains('Vigente', case=False)])
                    st.markdown('<div class="metric-label">Facturas Vigentes</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="metric-value" style="color:#28a745;">{vigentes}</div>', unsafe_allow_html=True)
                    st.markdown('<div style="text-align:center;color:#6c757d;">Activas en el sistema</div>', unsafe_allow_html=True)
            
            with col3:
                if 'Estatus' in df.columns:
                    canceladas = len(df[df['Estatus'].astype(str).str.contains('Cancelado', case=False)])
                    st.markdown('<div class="metric-label">Facturas Canceladas</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="metric-value" style="color:#dc3545;">{canceladas}</div>', unsafe_allow_html=True)
                    st.markdown('<div style="text-align:center;color:#6c757d;">Registros anulados</div>', unsafe_allow_html=True)
            
            with col4:
                if 'Método de Pago' in df.columns:
                    ppd_count = len(df[df['Método de Pago'].astype(str).str.contains('PPD', case=False)])
                    st.markdown('<div class="metric-label">Facturas PPD</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="metric-value" style="color:#fd7e14;">{ppd_count}</div>', unsafe_allow_html=True)
                    st.markdown('<div style="text-align:center;color:#6c757d;">Pago en parcialidades</div>', unsafe_allow_html=True)
            
            st.markdown("---")
            
            # Gráficos interactivos con Plotly
            if 'Método de Pago' in df.columns:
                st.markdown("### 📈 Distribución por Método de Pago")
                metodo_counts = df['Método de Pago'].value_counts().reset_index()
                metodo_counts.columns = ['Método', 'Cantidad']
                
                fig = px.pie(
                    metodo_counts,
                    values='Cantidad',
                    names='Método',
                    color_discrete_sequence=px.colors.qualitative.Pastel,
                    hole=0.3
                )
                fig.update_traces(
                    textposition='inside', 
                    textinfo='percent+label',
                    marker=dict(line=dict(color='#ffffff', width=1))
                )
                fig.update_layout(
                    showlegend=True,
                    legend=dict(
                        orientation="h",
                        yanchor="bottom",
                        y=-0.2,
                        xanchor="center",
                        x=0.5
                    )
                )
                st.plotly_chart(fig, use_container_width=True)
            
            if 'Mes' in df.columns:
                st.markdown("### 📅 Evolución Mensual")
                mes_counts = df['Mes'].value_counts().sort_index().reset_index()
                mes_counts.columns = ['Mes', 'Cantidad']
                
                fig = px.bar(
                    mes_counts,
                    x='Mes',
                    y='Cantidad',
                    color='Cantidad',
                    color_continuous_scale='Blues',
                    text='Cantidad'
                )
                fig.update_layout(
                    xaxis_title="Mes",
                    yaxis_title="Número de Facturas",
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)'
                )
                fig.update_traces(
                    marker_line_color='rgb(8,48,107)',
                    marker_line_width=1,
                    opacity=0.8
                )
                st.plotly_chart(fig, use_container_width=True)

        # Página de Facturas Emitidas
        elif menu == "Facturas Emitidas":
            st.markdown("## 📄 Facturas Emitidas")
            
            # Filtros adicionales en columnas
            col1, col2 = st.columns(2)
            with col1:
                if 'Método de Pago' in df.columns:
                    metodo_pago = st.multiselect(
                        "Filtrar por Método de Pago",
                        options=df['Método de Pago'].unique(),
                        help="Seleccione los métodos de pago a visualizar",
                        key="metodo_pago_filter"
                    )
                    if metodo_pago:
                        df_filtrado = df_filtrado[df_filtrado['Método de Pago'].isin(metodo_pago)]
            
            with col2:
                if 'Forma de Pago' in df.columns:
                    forma_pago = st.multiselect(
                        "Filtrar por Forma de Pago",
                        options=df['Forma de Pago'].unique(),
                        help="Seleccione las formas de pago a visualizar",
                        key="forma_pago_filter"
                    )
                    if forma_pago:
                        df_filtrado = df_filtrado[df_filtrado['Forma de Pago'].isin(forma_pago)]
            
            # Mostrar resultados en tabla estilizada
            columnas = ['UUID', 'Fecha', 'Método de Pago', 'Forma de Pago', 'Estatus', 'Total']
            if 'Mes' in df.columns:
                columnas.append('Mes')
            
            st.markdown(f"**📋 Mostrando {len(df_filtrado)} de {len(df)} facturas**")
            
            # Usar st.data_editor para mejor interactividad
            st.dataframe(
                df_filtrado[columnas].sort_values('Fecha', ascending=False),
                height=600,
                column_config={
                    "Fecha": st.column_config.DateColumn(
                        "Fecha", 
                        format="DD/MM/YYYY",
                        help="Fecha de emisión de la factura"
                    ),
                    "Total": st.column_config.NumberColumn(
                        "Total", 
                        format="$%.2f",
                        help="Monto total de la factura"
                    ),
                    "UUID": st.column_config.TextColumn(
                        "UUID",
                        help="Identificador único de la factura"
                    )
                },
                use_container_width=True,
                hide_index=True
            )

        # Página de Complementos de Pago
        elif menu == "Complementos de Pago":
            st.markdown("## 💳 Complementos de Pago")
            
            if 'UUIDs_Relacionados' in df.columns:
                # Filtrar solo complementos de pago (que tienen relaciones)
                df_complementos = df_filtrado[df_filtrado['UUIDs_Relacionados'].notna()]
                
                if not df_complementos.empty:
                    st.markdown("### Relación de Complementos")
                    
                    # Mostrar tabla de relaciones con pestañas
                    tab1, tab2 = st.tabs(["📋 Tabla de Datos", "📈 Visualización"])
                    
                    with tab1:
                        st.dataframe(
                            df_complementos[[
                                'UUID', 'Fecha', 'UUIDs_Relacionados', 'Total', 'Estatus'
                            ]].rename(columns={
                                'UUID': 'Complemento UUID',
                                'UUIDs_Relacionados': 'Facturas Relacionadas'
                            }),
                            height=500,
                            use_container_width=True,
                            column_config={
                                "Facturas Relacionadas": st.column_config.ListColumn(
                                    "Facturas Relacionadas",
                                    help="UUIDs de las facturas asociadas a este complemento"
                                )
                            }
                        )
                    
                    with tab2:
                        if 'Mes_XML' in df_complementos.columns:
                            st.markdown("#### Complementos por Mes")
                            complementos_por_mes = df_complementos['Mes_XML'].value_counts().sort_index().reset_index()
                            complementos_por_mes.columns = ['Mes', 'Cantidad']
                            
                            fig = px.bar(
                                complementos_por_mes,
                                x='Mes',
                                y='Cantidad',
                                color='Cantidad',
                                color_continuous_scale='greens',
                                text='Cantidad'
                            )
                            fig.update_layout(
                                xaxis_title="Mes",
                                yaxis_title="Número de Complementos",
                                plot_bgcolor='rgba(0,0,0,0)',
                                paper_bgcolor='rgba(0,0,0,0)'
                            )
                            st.plotly_chart(fig, use_container_width=True)
                else:
                    st.markdown('<div class="warning-box">⚠️ No se encontraron complementos de pago en los datos filtrados</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="warning-box">⚠️ No se encontró información de relaciones en los datos</div>', unsafe_allow_html=True)

        # Página de Gestión PPD/PUE
        elif menu == "Gestión PPD/PUE":
            st.markdown("## 🔄 Gestión de PPD y PUE")
            
            if 'Método de Pago' in df.columns:
                # Detectar PPD sin complemento
                df_ppd = df_filtrado[
                    (df_filtrado['Método de Pago'].astype(str).str.contains('PPD', case=False))
                ]
                
                if 'UUIDs_Relacionados' in df.columns:
                    # Obtener todos los UUIDs que están en relaciones
                    uuids_relacionados = set()
                    for lista in df['UUIDs_Relacionados'].dropna():
                        if isinstance(lista, str):
                            uuids_relacionados.update(lista.split('|'))
                        elif isinstance(lista, list):
                            uuids_relacionados.update(lista)
                    
                    # PPD sin complemento
                    ppd_sin_complemento = df_ppd[~df_ppd['UUID'].isin(uuids_relacionados)]
                    
                    st.markdown("### Facturas PPD sin complemento")
                    if not ppd_sin_complemento.empty:
                        st.markdown(f'<div class="warning-box">⚠️ Hay {len(ppd_sin_complemento)} facturas PPD sin complemento registrado</div>', unsafe_allow_html=True)
                        
                        # Mostrar con expansor para no saturar la vista
                        with st.expander("🔍 Ver detalles", expanded=False):
                            st.dataframe(
                                ppd_sin_complemento[[
                                    'UUID', 'Fecha', 'Total', 'Estatus'
                                ]],
                                height=300,
                                use_container_width=True
                            )
                    else:
                        st.markdown('<div class="success-box">✅ Todas las facturas PPD tienen complemento registrado</div>', unsafe_allow_html=True)
                    
                    # Búsqueda específica con mejor diseño
                    st.markdown("### 🔍 Buscar complemento para factura PPD")
                    
                    col1, col2 = st.columns([3,1])
                    with col1:
                        uuid_buscar = st.text_input(
                            "Ingrese UUID de factura PPD:",
                            placeholder="Ej: 123e4567-e89b-12d3-a456-426614174000",
                            label_visibility="collapsed",
                            key="uuid_search_input"
                        )
                    with col2:
                        st.write("")  # Espacio vacío para alinear
                        buscar_btn = st.button("Buscar", key="search_btn")
                    
                    if uuid_buscar and buscar_btn:
                        complemento = df[
                            df['UUIDs_Relacionados'].apply(
                                lambda x: uuid_buscar in (x.split('|') if isinstance(x, str) else (uuid_buscar in x if isinstance(x, list) else False))
                            )
                        ]
                        if not complemento.empty:
                            st.markdown('<div class="success-box">✅ Complemento encontrado</div>', unsafe_allow_html=True)
                            st.dataframe(complemento, use_container_width=True)
                        else:
                            st.markdown('<div class="danger-box">⚠️ No se encontró complemento para esta factura</div>', unsafe_allow_html=True)
                
                # Análisis de PUE con mejor visualización
                st.markdown("### Facturas PUE con complementos")
                if 'UUIDs_Relacionados' in df.columns:
                    df_pue = df_filtrado[
                        (df_filtrado['Método de Pago'].astype(str).str.contains('PUE', case=False))
                    ]
                    pue_con_complementos = df_pue[df_pue['UUID'].isin(uuids_relacionados)]
                    if not pue_con_complementos.empty:
                        st.markdown(f"**📌 {len(pue_con_complementos)} facturas PUE con complementos encontradas**")
                        
                        # Agrupar por mes para visualización
                        if 'Mes' in pue_con_complementos.columns:
                            pue_por_mes = pue_con_complementos.groupby('Mes').size().reset_index(name='Cantidad')
                            
                            fig = px.line(
                                pue_por_mes,
                                x='Mes',
                                y='Cantidad',
                                markers=True,
                                title="Facturas PUE con complementos por mes",
                                line_shape='spline'
                            )
                            fig.update_layout(
                                xaxis_title="Mes",
                                yaxis_title="Número de Facturas",
                                plot_bgcolor='rgba(0,0,0,0)',
                                paper_bgcolor='rgba(0,0,0,0)'
                            )
                            fig.update_traces(
                                line=dict(width=3, color='#4361ee'),
                                marker=dict(size=8, color='#f72585')
                            )
                            st.plotly_chart(fig, use_container_width=True)
                        
                        st.dataframe(pue_con_complementos, use_container_width=True)
                    else:
                        st.markdown('<div class="info-box">ℹ️ No se encontraron facturas PUE con complementos</div>', unsafe_allow_html=True)

else:
    # Pantalla de bienvenida cuando no hay archivo cargado
    st.markdown("""
    <div class="welcome-container">
        <div class="welcome-icon">
            <svg xmlns="http://www.w3.org/2000/svg" width="80" height="80" fill="currentColor" viewBox="0 0 16 16">
                <path d="M14 1a1 1 0 0 1 1 1v12a1 1 0 0 1-1 1H2a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1h12zM2 0a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V2a2 2 0 0 0-2-2H2z"/>
                <path d="M5.255 5.786a.237.237 0 0 0 .241.247h.825c.138 0 .248-.113.266-.25.09-.656.54-1.134 1.342-1.134.686 0 1.314.343 1.314 1.168 0 .635-.374.927-.965 1.371-.673.489-1.206 1.06-1.168 1.987l.003.217a.25.25 0 0 0 .25.246h.811a.25.25 0 0 0 .25-.25v-.105c0-.718.273-.927 1.01-1.486.609-.463 1.244-.977 1.244-2.056 0-1.511-1.276-2.241-2.673-2.241-1.267 0-2.655.59-2.75 2.286zm1.557 5.763c0 .533.425.927 1.01.927.609 0 1.028-.394 1.028-.927 0-.552-.42-.94-1.029-.94-.584 0-1.009.388-1.009.94z"/>
            </svg>
        </div>
        <h2 class="welcome-title">Bienvenido al Facturador Inteligente</h2>
        <p class="welcome-subtitle">Carga tu archivo Excel para comenzar a analizar tus facturas</p>
        <div style="margin-top:30px">
            <svg xmlns="http://www.w3.org/2000/svg" width="100" height="100" viewBox="0 0 24 24" fill="none" stroke="#4361ee" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
                <polyline points="7 10 12 15 17 10"></polyline>
                <line x1="12" y1="15" x2="12" y2="3"></line>
            </svg>
        </div>
        <p style="margin-top:20px;color:#6c757d;font-size:0.9rem;">Soporta archivos .xls con columnas: UUID, Fecha, Método de Pago, etc.</p>
    </div>
    """, unsafe_allow_html=True)
