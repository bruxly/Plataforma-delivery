# Plataforma-delivery
Ventas online interactivo 

🛍️ Servicio delivery
Una aplicación de e-commerce moderna y elegante desarrollada con Streamlit, que ofrece una experiencia de compra premium, gestión de carrito y procesamiento de pagos seguro.

Interactúa con el proyecto desplegado aquí:

✨ Características Principales
•	🔐 Autenticación OAuth con Google: Inicio de sesión seguro y sin fricciones
•	🛒 Carrito de Compras Inteligente: Gestión de productos con persistencia en tiempo real
•	💳 Procesamiento de Pagos: Integración completa con Stripe para pagos seguros
•	📱 Diseño Responsive: Interfaz moderna y adaptada para todos los dispositivos
•	🔥 Base de Datos Firebase: Almacenamiento seguro de usuarios, productos y órdenes
•	📊 Gestión de Inventario: Control automático de stock tras cada compra
•	🎨 UI/UX Premium: Diseño elegante con CSS personalizado
🛠️ Tecnologías Utilizadas
•	Frontend: Streamlit, HTML/CSS personalizado
•	Backend: Python
•	Base de Datos: Firebase Firestore
•	Autenticación: Google OAuth 2.0
•	Pagos: Datafono virtual personalizado
•	Almacenamiento: Firebase Storage
Deployment: Streamlit Cloud
•	📋 Requisitos Previos
•	Python 3.8+
•	Cuenta de Google Cloud Platform
•	Cuenta de Firebase
•	Cuenta de Stripe

📁 Estructura del Proyecto
fashion-store/
├── app.py                 # Página principal y autenticación
├── pages/
│   ├── catalogo.py       # Catálogo de productos
│   └── compraok.py       # Confirmación de compra
├── estilos/
│   ├── css_login.html    # Estilos para login
│   ├── css_catalogo.html # Estilos para catálogo
│   └── css_compra.html   # Estilos para compra
├── serviceAccountKey.json # Credenciales Firebase
├── requirements.txt      # Dependencias Python
├── .env                  # Variables de entorno
└── README.md            # Este archivo
🔧 Configuración Detallada
Firebase Setup
1.	Crear proyecto en Firebase Console
2.	Habilitar Authentication (Google)
3.	Configurar Firestore Database
4.	Crear las siguientes colecciones:
5.	usuarios: Información de usuarios
6.	products: Catálogo de productos
7.	carts: Carritos de compra
8.	orders: Órdenes completadas
Google OAuth Setup
1.	Ir a Google Cloud Console
2.	Crear credenciales OAuth 2.0
3.	Configurar URIs de redirección:
http://localhost:8501

🎯 Funcionalidades
Autenticación
•	Login con Google OAuth 2.0
•	Creación automática de usuarios
•	Gestión de sesiones segura
Catálogo
•	Visualización de productos con imágenes
•	Filtrado por categorías
•	Información detallada de stock
Carrito de Compras
•	Agregar/quitar productos
•	Persistencia en Firebase
•	Cálculo automático de totales

Gestión de Órdenes
•	Guardado automático en Firebase
•	Número de orden único
🚀 Deployment
Streamlit Cloud
•	Conectar repositorio GitHub
•	Configurar variables de entorno
•	Subir archivos de configuración
•	Desplegar aplicación
🛡️ Seguridad
✅ Autenticación OAuth 2.0
✅ Validación de datos server-side
✅ Encriptación de datos sensibles
✅ Manejo seguro de tokens
✅ Validación de pagos con woompy
📈 Próximas Mejoras
	Mejorar la visualización para que las imágenes.
	Análisis de ventas
	Tener una subcategoría de productos
 



