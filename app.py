import streamlit as st

# interartuar con el sistema operativo y trabajar con expresiones iregulares
import os, re

# permite codificar parametros de URL
from urllib.parse import urlencode

# interactuar con los servicios de firebase desde Python
import firebase_admin

# acceder a la base de datos de firebase
from firebase_admin import credentials, firestore

# carga las variables del entorno desde el archivo .env
from dotenv import load_dotenv

# hacer peticiones HTTP
import requests

# para trabajar con fechas y horas
from datetime import datetime


load_dotenv()  # ejecuta la funcion para cargar las variables de entorno defineidas en el archivo .env al entorno de ejecucion


# configurar la pagina
st.set_page_config(
    page_title="Mi Aplicación de Streamlit",
    page_icon="🛵",
    layout="wide",
    initial_sidebar_state="expanded",
)

# css personalizado
with open("estilos/css_login.html", "r") as file:  # habre ek archivo css_login.html
    # lee su contenido
    html_content = file.read()  # gurada su contenido en la variable html_content
# aplica el contenido HTML como mardonw
st.markdown(html_content, unsafe_allow_html=True)


# se ejeecuta una ves por sesion de usuario
if "has_run" not in st.session_state:
    ##marca quw la aplicacion ya se esta ejecutando
    st.session_state.has_run = True
    # ruta al archivo de clave del servicio de firebase
    service_account_key_path = "serviceAccountKey.json"
    # nombre de la coleccion de usuarios de firebase
    collection_name = "usuarios"
    # guarda el estado de sesion a la que el usuario de puede dirigir
    st.session_state.redirect_uri = "http://localhost:8501"

    # --- Inicializacion de firebase ADMIM SDK---

    # carga las credenciales del servicio de firebase a partir del adjunto serviceAccountKey.json
    if not firebase_admin._apps:
        cred = credentials.Certificate(service_account_key_path)
        # se inicializa la app de firebase con las credenciales
        firebase_admin.initialize_app(cred)
    st.session_state.db = (
        firestore.client()
    )  # se inicializa la base  de datos de firebase

    # inicia el cliente de google
    # inicia el cliente de google
    # st.session_state.google_client_id = os.environ.get(
    #     "GOOGLE_CLIENT_ID"
    # )  # cliente ID de google
    # st.session_state.google_client_secret = os.environ.get(
    #     "GOOGLE_SECRET_ID"
    # )  # secreto del cliente de google

    st.session_state.google_client_id = st.secrets['GOOGLE_CLIENT_ID']
    st.session_state.google_client_secret = st.secrets['GOOGLE_SECRET_ID']
    # Inicializa el carrito de compras
    st.session_state.cart = []  # lista vacia para el carrito de compras

# Autenticación con Google
def google_auth():
    # url de autenticacion de google
    auth_url = "https://accounts.google.com/o/oauth2/v2/auth"
    params = {
        "client_id": st.session_state.google_client_id,  # se obtiene el ID del cliente de google
        "redirect_uri": st.session_state.redirect_uri,  # se obtiene la URL de redireccionamiento
        "response_type": "code",  # tipo de respuesta
        "scope": "openid email profile",  # alcance de la solicitud
        "access_type": "offline",  # acceso offline para obtener un token actualizado
    }

    #
    google_auth_url = f"{auth_url}?{urlencode(params)}"  # se construye la URL de autenticacion de google
    return google_auth_url  # retorna la URL de autenticacion de google


# intercambiar el de autorizacion por un token de acceso
def exchange_code_for_token(auth_code):
    token_url = "https://oauth2.googleapis.com/token"  # url para intercambiar el codigo de autorizacion por un token de acceso
    data = {
        "client_id": st.session_state.google_client_id,  # ID del cliente de google
        "client_secret": st.session_state.google_client_secret,
        "redirect_uri": st.session_state.redirect_uri,  # url de redireccionamiento
        "code": auth_code,  # codigo de autorizacion
        "grant_type": "authorization_code",  # tipo de concesion
    }

    response = requests.post(
        token_url, data=data
    )  # se hace una peticion POST a la URL de token con los datos
    if response.status_code == 200:  # si la respuesta es exitosa
        return response.json()  # recorta la respuesta en formato JSON
    else:
        st.error(
            f"Error al obtener el token: {response.text}"
        )  # si hay un error, muestra el mensaje de error
        return None  # retorna None si hay un error


# obtener los datos del usuario a partir del token de acceso
def get_user_info(access_token):
    user_info_url = "https://www.googleapis.com/oauth2/v2/userinfo"  # url  para obtener la informacion del usuario
    headers = {
        "Authorization": f"Bearer {access_token}"  # se agrega el token de acceso en los encabezados de la peticion
    }

    response = requests.get(
        user_info_url, headers=headers
    )  # se hace una peticion GET a la URL de informacion del usuario

    if response.status_code == 200:  # si la respuesta es exitosa
        return response.json()  # retorn la respuesta en json
    else:
        st.error(
            f"Error al obtener la informacion del usuario: {response.text}"
        )  # si hay un error, muestra el mensaje de error
        return None  # retorna None si hay un error


# gardar el usuario en la base de datos de firebase
def verificar_o_crear_usuario(code):
    try:
        ##1. Intercambiar el codigo de autorizacion por un token de acceso
        tokens = exchange_code_for_token(code)
        if not tokens:
            return None  # si no se obtienen tokens, se retorna None

        access_token = tokens.get("access_token")  # se obtiene eltoken de acceso
        if not access_token:
            st.error(
                "No se pudo obtener el token de acceso"
            )  # si no se obtiene el token de acceso, muestra un mensaje de error
            return None

        # 2.Obtener la informacion del usuario de google
        user_info = get_user_info(access_token)  #
        if not user_info:
            return None  # si se obtiene la informacion del usaurio, se retorna None

        # 3. Obtener datos obligatorios del usario
        google_id = user_info.get("id")
        email = user_info.get("email")
        nombre = user_info.get("name")
        foto = user_info.get("picture")

        # verificar que los datos obligatorios esten presentes
        if not all([google_id, email, nombre, foto]):
            st.error(
                "Faltan datos obligatorios del usuario"
            )  # si faltan datos obligatorios, muestra un mensaje de error
            return None

        # 4. Verificar si el usuario ya esxite en la base de datos de firebase
        doc_ref = st.session_state.db.collection("usuarios").document(google_id)
        doc = doc_ref.get()

        if (
            doc.exists
        ):  # si el usuario existe cargar los datos del ultimo inicio de sesion
            usuario_data = doc.to_dict()
            usuario_data["last_login"] = (
                datetime.now()
            )  # agrega la fecha y hora del ultimo inicio de sesion
            usuario_data["uid"] = google_id  # agrega el ID del usuario

            # Actualizar el ultimo login en firebase
            doc_ref.update(
                {"last_login": datetime.now()}
            )  # actualiza la fecha y la hora del ultimo inicio de sesion
            return usuario_data
        else:
            # 5. usuario nuevo, guardar en firebase
            nuevo_usuario = {
                "uid": google_id,
                "email": email,
                "nombre": re.sub(
                    r"\s*\(.*?\)", "", nombre
                ).strip(),  # se elimina el texto entre parentesis y los espacios al inicio y al final del nombre
                "foto": foto,
                "verified_email": user_info.get(
                    "verified_email", False
                ),  # verifica si el correo electronico esta verificado
                "locale": user_info.get(
                    "locale", "es"
                ),  # obtiene el idioma del usuario por defecto en español
                "created_at": datetime.now(),  # fecha y hora de creacion del usuario
                "last_login": datetime.now(),  # fecha y hora del ultimo inicio de sesion
            }

            # Guardar en firebase
            doc_ref.set(nuevo_usuario)
            return nuevo_usuario
    except Exception as e:
        st.error(f"Error al verificar el usuario en Firebase: {str(e)}")  #
        return None  # retorna none si hay error

    # funcion para simular el boton de Google


def google_login_button():
    google_svg = """<svg class="google-icon" viewBox="0 0 24 24">
        <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
        <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
        <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/>
        <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
    </svg>
    """

    button_html = f"""<button class="google-login-btn">{google_svg}Continue with Google</button>"""
    return f"""<a href="{google_auth()}" target="_self" style="text-decoration: none;">{button_html}</a>"""


# funcion para recupoerar el usuario basado em session_id
def get_user_from_firestore(session_id):
    try:
        # buscar  el documento del carrito por session_id
        cart_doc = st.session_state.db.collection("carts").document(session_id).get()

        if cart_doc.exists:
            cart_data = (
                cart_doc.to_dict()
            )  # si el documento existe se convierte a un diccionario
            user_id = cart_data.get("user_id")  #

            if user_id:
                # buscar el usuario en la collecion de usuarios
                user_doc = (
                    st.session_state.db.collection("usuarios").document(user_id).get()
                )

                # busca el usuario en la colleccion y si lo encuentra devuelve los datos, si no lo encuentra muestra un error
                if user_doc.exists:
                    user_data = user_doc.to_dict()
                    return user_data
                else:
                    st.error("Usuario no encontrado en la base de datos.")
                    return None

            else:
                st.error("No se encontro el ID del usuario en el carrito.")
                return None
        else:
            st.error("No se encontró el carrito para esa session_id")
            return None

    except Exception as e:
        st.error(f"Error al recuperar el usuario: {str(e)}")
        return None


# --- Lógica principal de la pagina ---

# inicializo la varibale de usaurio, asegurando que siempre exista y evitando errores al exceder a ella mas adelante en la aplicacion
if "usuario" not in st.session_state:
    st.session_state.usuario = None


# Captura los prametros de la URL despues de la rediccion.
query_params = st.query_params  # captura los parametros de la URL
code = query_params.get("code")
state = query_params.get("state")

if "payment" in query_params:
    if query_params["payment"] == "success":  # si el pago fue exitoso
        st.session_state["stripe_session_id"] = query_params.get(
            "session_id"
        )  # se guarda el ID de la sesion de stripe
        st.session_state["payment_success"] = True  # se guarda el estado del pago como verdadero
        
        st.session_state.usuario = get_user_from_firestore(
            st.session_state["stripe_session_id"]
        )  # se obtiene el usuario
        st.session_state.login = True  # se guarda el estado deinicio de sesion como verdadero
        
        st.query_params.clear()  # se limpia los parametros de la URL
        st.switch_page("pages/compraok.py")  # se cambia a la pagina de compra exitosa

    elif query_params["payment"] == "cancelled":
        st.warning("⚠️ El pago fue cancelado. Puedes continuar comprando.")
        st.query_params.clear()
        st.rerun()  # fuerza la aplicacion a reiniciarse desde elprincipio, despues de limpiar parametros o cambiar de estado

if not st.session_state.usuario:
    if not code:
        # codigo principal
        st.markdown(f"""
           
        <div class ='main-container'>
            <div class = 'login-card'>
                <div class='brand-logo'>DOMIRAY SAS</div>
                <div class='brand-subtitle'>Servicios de mensajeria y domicilios</div>
                <div class='decoration-line'></div>
                <div class='welcome-message'>Los mejores sabores, productos<br> y servicios de Casanare en una sola app.<br> ¡Descubre tu nueva forma de pedir! </div> 
                """
                + google_login_button()+
                """
                <div class="legal-text"> By continuing, you agree to our <a href="#">Terms of Service</a></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        with st.spinner("Verificando autenticación, espere por favor..."):
            st.session_state.usuario = verificar_o_crear_usuario(code)
            st.query_params.clear()
            st.rerun()
else:
    with st.spinner("Todo listo! Redireccionando a la plataforma..."):
        st.session_state.login = True
        st.switch_page("pages/catalogo.py")
