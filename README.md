app: https://plataforma-delivery-casanareyopal.streamlit.app/catalogo   <br>

🛍️ Servicio delivery<br>
Una aplicación de e-commerce moderna y elegante desarrollada con Streamlit, que ofrece una experiencia de compra premium, gestión de carrito y procesamiento de pagos seguro.<br><br>

Interactúa con el proyecto desplegado aquí:<br>

✨ Características Principales<br>
•  	🔐 Autenticación OAuth con Google: Inicio de sesión seguro y sin fricciones<br>
•	🛒 Carrito de Compras Inteligente: Gestión de productos con persistencia en tiempo real<br>
•	💳 Procesamiento de Pagos: Integración completa con Stripe para pagos seguros<br>
•	📱 Diseño Responsive: Interfaz moderna y adaptada para todos los dispositivos<br>
•	🔥 Base de Datos Firebase: Almacenamiento seguro de usuarios, productos y órdenes<br>
•	📊 Gestión de Inventario: Control automático de stock tras cada compra<br>
•	🎨 UI/UX Premium: Diseño elegante con CSS personalizado<br>
🛠️ Tecnologías Utilizadas<br>
•	Frontend: Streamlit, HTML/CSS personalizado<br>
•	Backend: Python<br>
•	Base de Datos: Firebase Firestore<br>
•	Autenticación: Google OAuth 2.0<br>
•	Pagos: Datafono virtual personalizado<br>
•	Almacenamiento: Firebase Storage<br>
Deployment: Streamlit Cloud<br>
•	📋 Requisitos Previos<br>
•	Python 3.8+<br>
•	Cuenta de Google Cloud Platform<br>
•	Cuenta de Firebase<br>
•	Cuenta de Stripe<br><br>

📁 Estructura del Proyecto<br>
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
└── README.md            # Este archivo<br><br>
🔧 Configuración Detallada<br>
Firebase Setup<br>
1.	Crear proyecto en Firebase Console<br>
2.	Habilitar Authentication (Google)<br>
3.	Configurar Firestore Database<br>
4.	Crear las siguientes colecciones:<br>
5.	usuarios: Información de usuarios<br>
6.	products: Catálogo de productos<br>
7.	carts: Carritos de compra<br>
8.	orders: Órdenes completadas<br><br>
Google OAuth Setup<br>
1.	Ir a Google Cloud Console<br>
2.	Crear credenciales OAuth 2.0<br>
3.	Configurar URIs de redirección:<br>
http://localhost:8501<br><br>

🎯 Funcionalidades<br>
Autenticación<br>
•	Login con Google OAuth 2.0<br>
•	Creación automática de usuarios<br>
•	Gestión de sesiones segura<br><br>
Catálogo<br>
•	Visualización de productos con imágenes<br>
•	Filtrado por categorías<br>
•	Información detallada de stock<br><br>
Carrito de Compras<br>
•	Agregar/quitar productos<br>
•	Persistencia en Firebase<br>
•	Cálculo automático de totales<br><br>

Gestión de Órdenes<br>
•	Guardado automático en Firebase<br>
•	Número de orden único<br><br>
🚀 Deployment<br>
Streamlit Cloud<br>
•	Conectar repositorio GitHub<br>
•	Configurar variables de entorno<br>
•	Subir archivos de configuración<br>
•	Desplegar aplicación<br>
🛡️ Seguridad<br>
✅ Autenticación OAuth 2.0<br>
✅ Validación de datos server-side<br>
✅ Encriptación de datos sensibles<br>
✅ Manejo seguro de tokens<br>
✅ Validación de pagos con woompy<br>
📈 Próximas Mejoras<br>
	Mejorar la visualización para que las imágenes.<br>
	Análisis de ventas<br>
	Tener una subcategoría de productos<br>
 





