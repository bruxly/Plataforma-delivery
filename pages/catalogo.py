import streamlit as st
import stripe
import os
from datetime import datetime
from PIL import Image
from io import BytesIO
import urllib.parse
import hashlib



#DEV_MODE = True  # Cambia a False en producción


# verifica si la clave login no esta presente en el estado de inicio de Stremalit, indica que el usuario no iniciado sesion correctamente
if "login" not in st.session_state:
    # si el usuario no ha iniciado sesion,lo redirige automaticamente a la pagina principal de login
    st.switch_page("app.py")

# CSS personalizado para el fondo de la aplicasción
with open("estilos/css_catalogo.html", "r") as file:
    ##lee el contenido del archivo css_catalogo.html
    # y lo asigna a la variable html_content
    html_content = file.read()
st.markdown(html_content, unsafe_allow_html=True)

# configuracion de Stripe
##########################
##########################
stripe.api_key = os.environ.get("STRIPE_API_KEY")
##########################
##########################


# funciones de firestore
def get_products():
    """Obtiene productos desde Firestore"""
    try:
        products_ref = st.session_state.db.collection('products')
        docs = products_ref.stream()
        
        products = []
        for doc in docs:
            product = doc.to_dict()
            product['id'] = doc.id
            products.append(product)
        
        # Si no hay productos, crear algunos de ejemplo
        if not products:
        # 🧩 Productos locales (puedes editarlos)
            sample_products = [
                
                #el corral
                
                {
                    "name": "Todoterreno Clasica en combo",
                    "price": 43900,
                    "image": "https://i.imgur.com/l4Nb5BG.jpeg",
                    "description": "dos carnes de 125g cada una",
                    "category": "El corral",
                },
            
                {
                    "name": "Todoterreno Tocineta en Combo",
                    "price": 45900,
                    "image": "https://i.imgur.com/xgFtkGx.jpeg",
                    "description": "dos carnes de 125g cada una",
                    "category": "El corral",
                },

                {
                    "name": "Todoterreno Clasica",
                    "price": 35900,
                    "image": "https://i.imgur.com/7i5h1T4.jpeg",
                    "description": "dos carnes de 125g cada una",
                    "category": "El corral",
                },

                {
                    "name": "Todoterreno Callejera",
                    "price": 37900,
                    "image": "https://i.imgur.com/PsjQLna.jpeg",
                    "description": "dos carnes de 125g cada una",
                    "category": "El corral",
                },
                {
                    "name": "Todoterreno Tocineta",
                    "price": 37900,
                    "image": "https://i.imgur.com/XTBJnYc.jpeg",
                    "description": "dos carnes de 125g cada una",
                    "category": "El corral",
                },

                {
                    "name": "Corralita",
                    "price": 22900,
                    "image": "https://i.imgur.com/a3H6uCS.jpeg",
                    "description": "Carne de 90g,tomate y cebolla en rodajas",
                    "category": "El corral",
                },

                {
                    "name": "Corral",
                    "price": 23900,
                    "image": "https://i.imgur.com/l9VNcfu.jpeg",
                    "description": "Carne de 125g,tomate y cebolla en rodajas",
                    "category": "El corral",
                },

                {
                    "name": "Corral Pollo",
                    "price": 25900,
                    "image": "https://i.imgur.com/dK9p11X.jpeg",
                    "description": "Pechuga de pollo de 154g con salsa bbq.",
                    "category": "El corral",
                },

                
                {
                    "name": "Callejero En Combo",
                    "price": 28900,
                    "image": "https://i.imgur.com/3bJtjzW.png",
                    "description": "Con salchicha de 115g a la parrilla.",
                    "category": "El corral",
                },

                {
                    "name": "Hawaiano Combo",
                    "price": 32900,
                    "image": "https://i.imgur.com/pfkNBGy.jpeg",
                    "description": "Con salchicha a la parrilla, queso,piña y salsas",
                    "category": "El corral",
                },
                #EL CARRIEL
                {
                    "name": "El Carriel",
                    "price": 32000,
                    "image": "https://i.imgur.com/xAvOav3.png",
                    "description": "Un Kilo bien chimba de arroz paisa con chicharron te alcanza pa' 2 personas o 3 si necesitas 😉🌾",
                    "category": "El carriel",
                },
                #EL CARRIEL
                {
                    "name": "El Carriel",
                    "price": 18000,
                    "image": "https://i.imgur.com/tHviOSw.jpeg",
                    "description": "Personal con papitas, Porción personal de arroz paisa con papitas y limonada",
                    "category": "El carriel",
                },
            #    

                #MAGDALENA
                {
                    "name": "Magdalena",
                    "price": 48000,
                    "image": "https://i.imgur.com/VX1OoNT.png",
                    "description": "💌 Mulata 🧋 Torta a elección: chocolate, zanahoria o naranja 🎂",
                    "category": "magdalena",
                },
                #MAGDALENA
                {
                    "name": "Magdalena",
                    "price": 78000,
                    "image": "https://i.imgur.com/05RR79d.png",
                    "description": "Me Latte 🧋Elixir de frutas 🍓Sándwich Llanero 🥪",
                    "category": "magdalena",
                },

                #MAGDALENA
                {
                    "name": "Magdalena",
                    "price": 59000,
                    "image": "https://i.imgur.com/lZGVX0C.png",
                    "description": "Antojo ácido 🥭🧋Mini fresas🍓Sandwich de pollo Napoleón",
                    "category": "magdalena",
                },

                #MAGDALENA
                {
                    "name": "Magdalena",
                    "price": 52000,
                    "image": "https://i.imgur.com/XPuJn5F.png",
                    "description": "Cherrymocca🧋Sándwich Marco polo🥪",
                    "category": "magdalena",
                },

                #MAGDALENA
                {
                    "name": "Magdalena",
                    "price": 46000,
                    "image": "https://i.imgur.com/JHY6d7o.png",
                    "description": "Smoothie frutos rojos 🥤Torta de chocolate, zanahoria o naranja🎂",
                    "category": "magdalena",
                },

                #MAGDALENA
                {
                    "name": "Magdalena",
                    "price": 65000,
                    "image": "https://i.imgur.com/IaUeplo.png",
                    "description": "Me Latte🧋Mini Elixir ✨Sándwich de pollo Napoleón🥪",
                    "category": "magdalena",
                },

            
                #MAGDALENA
                {
                    "name": "Magdalena",
                    "price": 23000,
                    "image": "https://i.imgur.com/MaI4Nox.png",
                    "description": "Con crema chantilly, topping de chocolate o lecherita.",
                    "category": "magdalena",
                },

            
                #MAGDALENA
                {
                    "name": "Magdalena",
                    "price": 23000,
                    "image": "https://i.imgur.com/ldV1vj7.png",
                    "description": "Fressas con durazno🍓🍑Con crema chantilly, topping de chocolate o lecherita.",
                    "category": "magdalena",
                },

                #MAGDALENA
                {
                    "name": "Magdalena",
                    "price": 18000,
                    "image": "https://i.imgur.com/HsqYXky.png",
                    "description": "Delicioso Bowl fresas con helado.",
                    "category": "magdalena",
                },

                #MAGDALENA
                {
                    "name": "Magdalena",
                    "price": 25000,
                    "image": "https://i.imgur.com/e897HRS.png",
                    "description": "Mini fresas kiwi X3, durazno con chantilly y topping de chocolate.",
                    "category": "magdalena",
                },





                # QUBANO
                {
                    "name": "Qbano",
                    "price": 30600,
                    "image": "https://i.imgur.com/tyul788.jpeg",
                    "description": "Sándwich Ropa Vieja En Combo",
                    "category": "Qbano",
                },
                {
                    "name": "Qbano",
                    "price": 24600,
                    "image": "https://i.imgur.com/4EXltWq.jpeg",
                    "description": "Sándwich Especial Combo",
                    "category": "Qbano",
                },
                {
                    "name": "Qbano",
                    "price": 27600,
                    "image": "https://i.imgur.com/1UhLhOe.jpeg",
                    "description": "Sándwich Súper Especial Combo",
                    "category": "Qbano",
                },
                {
                    "name": "Qbano",
                    "price": 29600,
                    "image": "https://i.imgur.com/NVfqHoc.jpeg",
                    "description": "Sándwich Roast Beef Combo",
                    "category": "Qbano",
                },

            

                {
                    "name": "Qbano",
                    "price": 29600,
                    "image": "https://i.imgur.com/0U7wPHo.jpeg",
                    "description": "Sándwich Cordero Combo",
                    "category": "Qbano",
                },

                {
                    "name": "Qbano",
                    "price": 29600,
                    "image": "https://i.imgur.com/2IRMt6B.jpeg",
                    "description": "Sándwich Pollo Combo",
                    "category": "Qbano",
                },
                
                #comida china
                {
                    "name": "Combo Pollo",
                    "price": 39000,
                    "image": "https://i.imgur.com/UajBfHQ.jpeg",
                    "description": "1/4 de pollo, papas y arroz.",
                    "category": "comida china",
                },
                #comida china
                {
                    "name": "Media Valenciana",
                    "price": 39000,
                    "image": "https://i.imgur.com/2ZXIdcA.jpeg",
                    "description": "1/4 de pollo, arroz chino.",
                    "category": "comida china",
                },
                #comida china
                {
                    "name": "Combo Chop Suey",
                    "price": 39000,
                    "image": "https://i.imgur.com/7iCQYxg.jpeg",
                    "description": "papas,chop suey y arroz chino.",
                    "category": "comida china",
                },
                

                #supermercados
                
                {
                    "name": "Los Ocobos",
                    "price": 11400,
                    "image": "https://i.imgur.com/IGHnkaE.jpeg",
                    "description": "Aceite 900ml",
                    "category": "supermercado",
                },
                

                {
                    "name": "Los Ocobos",
                    "price": 14500,
                    "image": "https://i.imgur.com/BTWJj1W.jpeg",
                    "description": "Cubeta de huevos",
                    "category": "supermercado",
                },

                
                {
                    "name": "Los Ocobos",
                    "price": 6100,
                    "image": "https://i.imgur.com/alzkciX.jpeg",
                    "description": "Salchicha Zenú, 5 und",
                    "category": "supermercado",
                },

                {
                    "name": "Los Ocobos",
                    "price": 2200,
                    "image": "https://i.imgur.com/vUyo1uM.jpeg",
                    "description": "Arroz 460g ",
                    "category": "supermercado",
                },
                {
                    "name": "Los Ocobos",
                    "price": 6800,
                    'image':'https://i.imgur.com/CdWQwAS.jpeg',
                    "description": "DON CAT 500g",
                    "category": "supermercado",
                },

                {
                    "name": "Los Ocobos",
                    "price": 8500,
                    "image": "https://i.imgur.com/8mYeRbM.png",
                    "description": "Coca-cola 2.5lts",
                    "category": "supermercado",
                },
                
                #Tiendas D1
                {
                    "name": "Tiendas D1",
                    "price": 3050,
                    "image": "https://i.imgur.com/zqm2ji5.png",
                    "description": "Deslactosada 900ml",
                    "category": "tiendas D1",
                },
                #Tiendas D1
                {
                    "name": "Tiendas D1",
                    "price": 3350,
                    "image": "https://i.imgur.com/toiCwNd.png",
                    "description": "Leche Entera 900ml",
                    "category": "tiendas D1",
                },
                #Tiendas D1

                {
                    "name": "Tiendas D1",
                    "price": 8300,
                    "image": "https://i.imgur.com/IEdmQX3.png",
                    "description": "En Polvo Entera 350g",
                    "category": "tiendas D1",
                },
                #Tiendas D1
                {
                    "name": "Tiendas D1",
                    "price": 1200,
                    "image": "https://i.imgur.com/86A2hwi.png",
                    "description": "Leche Entera 200ml",
                    "category": "tiendas D1",
                },
                #Tiendas D1
                {
                    "name": "Tiendas D1",
                    "price": 1990,
                    "image": "https://i.imgur.com/PNtDPaH.png",
                    "description": "Arepa Minitela 600g",
                    "category": "tiendas D1",
                },
                #Tiendas D1
                {
                    "name": "Tiendas D1",
                    "price": 1890,
                    "image": "https://i.imgur.com/BB48JmZ.png",
                    "description": "Arepa Blanca 500g",
                    "category": "tiendas D1",
                },
                #Tiendas D1
                {
                    "name": "Tiendas D1",
                    "price": 9300,
                    "image": "https://i.imgur.com/gnC8O4x.png",
                    "description": "Salchicha Camprestre 400g",
                    "category": "tiendas D1",
                },
                #Tiendas D1
                {
                    "name": "Tiendas D1",
                    "price": 7990,
                    "image": "https://i.imgur.com/FuUuoUV.png",
                    "description": "Chorizo Santarrosano 225g",
                    "category": "tiendas D1",
                },
                #Tiendas D1
                {
                    "name": "Tiendas D1",
                    "price": 7990,
                    "image": "https://i.imgur.com/v7J7Klr.png",
                    "description": "Chorizo Antioqueño 225g",
                    "category": "tiendas D1",
                },
                #Tiendas D1
                {
                    "name": "Tiendas D1",
                    "price": 5490,
                    "image": "https://i.imgur.com/hSNhJGd.png",
                    "description": "Queso Mozzarella Bufala 100g",
                    "category": "tiendas D1",
                },
                #Tiendas D1
                {
                    "name": "Tiendas D1",
                    "price": 8750,
                    "image": "https://i.imgur.com/LzbTraU.png",
                    "description": "Queso Campesino Bloque 350g",
                    "category": "tiendas D1",
                },
                #Tiendas D1
                {
                    "name": "Tiendas D1",
                    "price": 3300,
                    "image": "https://i.imgur.com/2FRw5OC.png",
                    "description": "Queso Crema 200g",
                    "category": "tiendas D1",
                },
                #Tiendas D1
                {
                    "name": "Tiendas D1",
                    "price": 13650,
                    "image": "https://i.imgur.com/1Z4zfQQ.png",
                    "description": "Queso Parmesano Alpina 120g",
                    "category": "tiendas D1",
                },
                #Tiendas D1
                {
                    "name": "Tiendas D1",
                    "price": 3400,
                    "image": "https://i.imgur.com/Iohkn2c.png",
                    "description": "Vinagre de Limpieza 1 Litro",
                    "category": "tiendas D1",
                },
                #Tiendas D1
                {
                    "name": "Tiendas D1",
                    "price": 4990,
                    "image": "https://i.imgur.com/6oH9v21.png",
                    "description": "Toalla de Papel Green 3h 80 Hojas",
                    "category": "tiendas D1",
                },
                #Tiendas D1
                {
                    "name": "Tiendas D1",
                    "price": 2200,
                    "image": "https://i.imgur.com/A1hnmlq.png",
                    "description": "Esponja Multiusos 2 und",
                    "category": "tiendas D1",
                },

                #TIENDAS D1 JABONES
                {
                    "name": "Tiendas D1",
                    "price": 4990,
                    "image": "https://i.imgur.com/B9i9eMg.png",
                    "description": "Jabón Líquido Aloe Vera 1000ml",
                    "category": "tiendas D1",
                },
                #TIENDAS D1 JABONES
                {
                    "name": "Tiendas D1",
                    "price": 4450,
                    "image": "https://i.imgur.com/XRVq0dJ.png",
                    "description": "Jabón Liquido King 1000ml",
                    "category": "tiendas D1",
                },
                #TIENDAS D1 JABONES
                {
                    "name": "Tiendas D1",
                    "price": 12600,
                    "image": "https://i.imgur.com/NK302TQ.png",
                    "description": "Jabón Liquido King 3 litros",
                    "category": "tiendas D1",
                },
                #TIENDAS D1 JABONES
                {
                    "name": "Tiendas D1",
                    "price": 8990,
                    "image": "https://i.imgur.com/wel8N6J.png",
                    "description": "Suavisante Floral 3 litros",
                    "category": "tiendas D1",
                },
                #TIENDAS D1 JABONES
                {
                    "name": "Tiendas D1",
                    "price": 3850,
                    "image": "https://i.imgur.com/cXarf1W.png",
                    "description": "Quitamanchas Liquido 1 Litro",
                    "category": "tiendas D1",
                },
                #TIENDAS D1 JABONES
                {
                    "name": "Tiendas D1",
                    "price": 2900,
                    "image": "https://i.imgur.com/Zus88nZ.png",
                    "description": "Ropa Color",
                    "category": "tiendas D1",
                },
                #TIENDAS D1 JABONES
                {
                    "name": "Tiendas D1",
                    "price": 3500,
                    "image": "https://i.imgur.com/uk04WVV.png",
                    "description": "Detergente Multiusos 900g",
                    "category": "tiendas D1",
                    
                },
                #TIENDAS D1 JABONES
                {
                    "name": "Tiendas D1",
                    "price": 2550,
                    "image": "https://i.imgur.com/msG0WSF.png",
                    "description": "Crema Lavaloza King 500g",
                    "category": "tiendas D1", 
                },
                #TIENDAS D1 JABONES
                {
                    "name": "Tiendas D1",
                    "price": 2600,
                    "image": "https://i.imgur.com/t2ugmq4.jpg",
                    "description": "Lavaloza King 500g",
                    "category": "tiendas D1", 
                },
                #TIENDAS D1 GASEOSAS
                {
                    "name": "Tiendas D1",
                    "price": 5650,
                    "image": "https://i.imgur.com/z3iXdbD.jpeg",
                    "description": "Coca-Cola Zero 1750ml",
                    "category": "tiendas D1", 
                },

                #TIENDAS D1 GASEOSAS
                {
                    "name": "Tiendas D1",
                    "price": 13750,
                    "image": "https://i.imgur.com/f7kFe65.jpeg",
                    "description": "Coca-Cola Zero 2x2.5L",
                    "category": "tiendas D1", 
                },
                #TIENDAS D1 GASEOSAS
                {
                    "name": "Tiendas D1",
                    "price": 14450,
                    "image": "https://i.imgur.com/fshZ1Cx.jpeg",
                    "description": "Coca-Cola 2x2.5L",
                    "category": "tiendas D1", 
                },
                
            
                #TIENDAS D1 GASEOSAS
                {
                    "name": "Tiendas D1",
                    "price": 2990,
                    "image": "https://i.imgur.com/0Quuyks.png",
                    "description": "Gaseosa Cola Negra 1700ml",
                    "category": "tiendas D1", 
                },
                #TIENDAS D1 GASEOSAS
                {
                    "name": "Tiendas D1",
                    "price": 5950,
                    "image": "https://i.imgur.com/2SKowfM.jpeg",
                    "description": "Pony Malta 2 Litros",
                    "category": "tiendas D1", 
                },
                #TIENDAS D1 GASEOSAS
                {
                    "name": "Tiendas D1",
                    "price": 1300,
                    "image": "https://i.imgur.com/oJXFpvw.jpeg",
                    "description": "Pony Malta 200 ml",
                    "category": "tiendas D1", 
                },
                #TIENDAS D1 ARENAS PARA GATOS
                {
                    "name": "Tiendas D1",
                    "price": 14850,
                    "image": "https://i.imgur.com/SYwZkz9.jpeg",
                    "description": "Arena Para Gatos 4500g",
                    "category": "tiendas D1", 
                },
                #TIENDAS D1 COMIDAS PARA GATOS
                {
                    "name": "Tiendas D1",
                    "price": 6250,
                    "image": "https://i.imgur.com/Gcoj65q.png",
                    "description": "Alimento Para Gatos 1000g",
                    "category": "tiendas D1", 
                },
                #TIENDAS D1 COMIDAS PARA GATOS
                {
                    "name": "Tiendas D1",
                    "price": 10950,
                    "image": "https://i.imgur.com/HoYUpfp.jpeg",
                    "description": "Alimento Para Gatos 1000g",
                    "category": "tiendas D1", 
                },


                #cobijas y cortinas
                {
                    "name": "Sabanas",
                    "price": 70000.00,
                    "image": "https://i.imgur.com/l8UwyeX.jpeg",
                    "description": "Medidas 1*40 cama doble",
                    "category": "cobijas y cortinas",
                },

                {
                    "name": "Sabanas",
                    "price": 70000.00,
                    "image": "https://i.imgur.com/2mOIbYN.png",
                    "description": "Medidas 1*40 cama doble",
                    "category": "cobijas y cortinas",
                },

                {
                    "name": "Sabanas",
                    "price": 70000.00,
                    "image": "https://i.imgur.com/Z6aagAl.jpeg",
                    "description": "Medidas 1*40 cama doble",
                    "category": "cobijas y cortinas",
                },
                #sabanas
                {
                    "name": "Sabanas",
                    "price": 70000.00,
                    "image": "https://i.imgur.com/lrQu2L7.jpeg",
                    "description": "Medidas 1*40 cama doble",
                    "category": "cobijas y cortinas",
                },
                #sabanas
                {
                    "name": "Sabanas",
                    "price": 70000.00,
                    "image": "https://i.imgur.com/uAgl7a3.jpeg",
                    "description": "Medidas 1*40 cama doble",
                    "category": "cobijas y cortinas",
                },
                #sabanas
                {
                    "name": "Sabanas",
                    "price": 70000.00,
                    "image": "https://i.imgur.com/CkgTyHn.jpeg",
                    "description": "Medidas 1*40 cama doble",
                    "category": "cobijas y cortinas",
                },
                #sabanas
                {
                    "name": "Sabanas",
                    "price": 70000.00,
                    "image": "https://i.imgur.com/OtQ8AwC.jpeg",
                    "description": "Medidas 1*40 cama doble",
                    "category": "cobijas y cortinas",
                },
                #sabanas
                {
                    "name": "Sabanas",
                    "price": 70000.00,
                    "image": "https://i.imgur.com/Mfb4TJz.jpeg",
                    "description": "Medidas 1*40 cama doble",
                    "category": "cobijas y cortinas",
                },
                #sabanas
                {
                    "name": "Sabanas",
                    "price": 70000.00,
                    "image": "https://i.imgur.com/PGUS60t.jpeg",
                    "description": "Medidas 1*40 cama doble",
                    "category": "cobijas y cortinas",
                },
                #sabanas
                {
                    "name": "Sabanas",
                    "price": 85000.00,
                    "image": "https://i.imgur.com/Lmpcch4.jpeg",
                    "description": "Medidas 1*60",
                    "category": "cobijas y cortinas",
                },
                #sabanas
                {
                    "name": "Sabanas",
                    "price": 85000.00,
                    "image": "https://i.imgur.com/fT7vokK.jpeg",
                    "description": "Medidas 1*60",
                    "category": "cobijas y cortinas",
                },
                #sabanas
                {
                    "name": "Sabanas",
                    "price": 85000.00,
                    "image": "https://i.imgur.com/4srDLKY.jpeg",
                    "description": "Medidas 1*60",
                    "category": "cobijas y cortinas",
                },

                #sabanas
                {
                    "name": "Sabanas",
                    "price": 85000.00,
                    "image": "https://i.imgur.com/4lFRmLs.jpeg",
                    "description": "Medidas 1*60",
                    "category": "cobijas y cortinas",
                },
                #sabanas
                {
                    "name": "Sabanas",
                    "price": 85000.00,
                    "image": "https://i.imgur.com/cPKUoOt.jpeg",
                    "description":"Medidas 1*60",
                    "category": "cobijas y cortinas",
                },
                #sabanas
                {
                    "name": "Sabanas",
                    "price": 85000.00,
                    "image": "https://i.imgur.com/DVyzfIY.jpeg",
                    "description": "Medidas 1*60",
                    "category": "cobijas y cortinas",
                },
                #sabanas
                {
                    "name": "Sabanas",
                    "price": 85000.00,
                    "image": "https://i.imgur.com/QmBsDzU.jpeg",
                    "description": "Medidas 1*60",
                    "category": "cobijas y cortinas",
                },
                #sabanas
                {
                    "name": "Sabanas",
                    "price": 85000.00,
                    "image": "https://i.imgur.com/KdsDNmJ.jpeg",
                    "description": "Medidas 1*60",
                    "category": "cobijas y cortinas",
                },
                #cubrelecho
                {
                    "name": "Cubrelecho",
                    "price": 130000.00,
                    "image": "https://i.imgur.com/KdsDNmJ.jpeg",
                    "description": "Doble fax cama doble",
                    "category": "cobijas y cortinas",
                },
                #cubrelecho
                {
                    "name": "Cubrelecho",
                    "price": 130000.00,
                    "image": "https://i.imgur.com/TmCQlTN.jpeg",
                    "description": "Doble fax cama doble",
                    "category": "cobijas y cortinas",
                },
                #cubrelecho
                {
                    "name": "Cubrelecho",
                    "price": 130000.00,
                    "image": "https://i.imgur.com/5MMhfSs.jpeg",
                    "description": "Doble fax cama doble",
                    "category": "cobijas y cortinas",
                },
                #cubrelecho
                {
                    "name": "Cubrelecho",
                    "price": 130000.00,
                    "image": "https://i.imgur.com/D35igbw.jpeg",
                    "description": "Doble fax cama doble",
                    "category": "cobijas y cortinas",
                },
                #cubrelecho
                {
                    "name": "Cubrelecho",
                    "price": 130000.00,
                    "image": "https://i.imgur.com/XZq06Uo.jpeg",
                    "description": "Doble fax cama doble",
                    "category": "cobijas y cortinas",
                },
                #cubrelecho
                {
                    "name": "Cubrelecho",
                    "price": 130000.00,
                    "image": "https://i.imgur.com/IpWOowz.jpeg",
                    "description": "Doble fax cama doble",
                    "category": "cobijas y cortinas",
                },
            
                #cubrelecho
                {
                    "name": "Cubrelecho",
                    "price": 130000.00,
                    "image": "https://i.imgur.com/wKu5z8j.jpeg",
                    "description": "Doble fax cama doble",
                    "category": "cobijas y cortinas",
                },
                #cortinas
                {
                    "name": "Cortinas",
                    "price": 70000.00,
                    "image": "https://i.imgur.com/8NsXakw.jpeg",
                    "description": "gran variedad de colores",
                    "category": "cobijas y cortinas",
                },


                #PLOMEROS
                {
                    "name": "Plomeros",
                    "price": 0.00,
                    "image": "https://i.imgur.com/EHKPRbc.jpeg",
                    "description": "Impermeabilización Canales y Techos",
                    "category": "plomeria",
                },
                #PLOMEROS
                {
                    "name": "Plomeros",
                    "price": 0.00,
                    "image": "https://i.imgur.com/LRTnmuS.jpeg",
                    "description": "Mantenimiento de Tuberias",
                    "category": "plomeria",
                },
                #PLOMEROS

                {
                    "name": "Plomeros",
                    "price": 0.00,
                    "image": "https://i.imgur.com/rWeKPRu.jpeg",
                    "description": "Construimos tu Vivienda desde Cero",
                    "category": "plomeria",
                }
                
                # Puedes añadir más productos aquí
            ]

            # Agregar productos de ejemplo a Firestore
            for product in sample_products:
                st.session_state.db.collection('products').add(product)
                
            return sample_products
        return products

    except Exception as e:
            st.error(f"Error al obtener productos: {str(e)}")
            return []

    

def add_to_cart(product_id, user_id):
    """Agrega producto al carrito"""
    try:
        cart_ref = st.session_state.db.collection("carts").document(user_id)
        cart_doc = cart_ref.get()

        if cart_doc.exists:
            cart_data = cart_doc.to_dict()
            items = cart_data.get("items", [])

            # Verificar si el producto ya está en el carrito
            product_exists = False
            for item in items:
                if item["product_id"] == product_id:
                    item["quantity"] += 1
                    product_exists = True
                    break

            if not product_exists:
                items.append(
                    {
                        "product_id": product_id,
                        "quantity": 1,
                        "added_at": datetime.now()
                    }
                )

            cart_ref.update({"items": items})
        else:
            cart_ref.set(
                {
                    "items": [
                        {
                            "product_id": product_id,
                            "quantity": 1,
                            "added_at": datetime.now()
                        }
                    ],
                    "created_at": datetime.now()
                }
            )

        return True

    except Exception as e:
        st.error(f"Error al agregar al carrito: {str(e)}")
        return False


# Funciones de Stripe
def create_checkout_session(items, user_email):
    """Crea una sesión de pago con Stripe"""
    try:
        line_items = []
        for item in items:
            line_items.append({
                'price_data': {
                    'currency': 'brl',
                    'product_data': {
                        'name': item['name'],
                        'images': [item['image']],
                    },
                    'unit_amount': int(item['price'] * 100),
                },
                'quantity': item['quantity'],
            })
        
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
            success_url='https://xperience-ecommerce.streamlit.app?payment=success&session_id={CHECKOUT_SESSION_ID}',
            cancel_url='https://xperience-ecommerce.streamlit.app?payment=cancelled&session_id={CHECKOUT_SESSION_ID}',
            customer_email=user_email,
            metadata={
                'user_id': st.session_state['usuario']['uid'],
                'user_name': st.session_state['usuario']['nombre']
            }
        )
        
        return checkout_session.url, checkout_session.id
    
    except Exception as e:
        st.error(f"Error al crear sesión de pago: {str(e)}")
        return None



# Función para guardar carrito en Firestore
def save_cart_to_firestore(session_id, user_id, cart_items):
    """Guarda el carrito en Firestore antes de ir a Stripe"""
    try:
        cart_data = {
            "session_id": session_id,
            "user_id": user_id,
            "items": cart_items,
            "created_at": datetime.now(),
            "status": "pending_payment",
        }

        # Guardar en la colección 'temp_carts' para recuperar después
        st.session_state.db.collection("carts").document(session_id).set(cart_data)

    except Exception as e:
        st.error(f"Error al guardar carrito: {str(e)}")

def clear_user_cart(session_id):
    """Limpia el carrito del usuario después de la compra"""
    try:
        cart_ref = st.session_state.db.collection('carts').document(session_id)
        cart_ref.delete()        
    except Exception as e:
        st.error(f"Sin datos en el carrito: {str(e)}")


def create_stripe_button(cart, user_email, user_uid):
    checkout_url, session_id = create_checkout_session(cart, user_email)
    
    if checkout_url and session_id:
        if 'stripe_session_id' in st.session_state: clear_user_cart(st.session_state['stripe_session_id'])
        st.session_state['stripe_session_id'] = session_id
        save_cart_to_firestore(session_id, user_uid, cart)
        
        # Estilo idéntico al botón morado de la imagen
        button_html = f"""
        <style>
        .payment-container a {{
            text-decoration: none;
            color: inherit;
        }}
        
        .payment-container button {{
            background: linear-gradient(45deg, #667eea, #764ba2);
            color: white;
            border: none;
            border-radius: 25px;
            padding: 0.75rem 2rem;
            transition: all 0.3s ease;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            outline: none;
            box-sizing: border-box;
            margin: 0.5rem 0;
            width: auto;
            vertical-align: middle;
            font-size: 1rem;
            line-height: 1.2;
        }}
        
        .payment-container button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }}
        
        .payment-container button:active {{
            transform: translateY(0);
        }}
        </style>
        
        <div class="payment-container" style="display: flex; justify-content: flex-start; margin: 0.25rem 0px;">
            <a href="{checkout_url}" target="_blank">
                <button>
                    💳 Proceder al Pago
                </button>
            </a>
        </div>
        """
        return button_html
    return None



# --- LÓGICA PRINCIPAL DE LA PÁGINA ---
st.markdown(
    '<div class="main-header"><h1>🛵 Domicilios las 24 horas</h1><p>Bienvenido/a aqui encuentras todo en solo lugar</p></div>',
    unsafe_allow_html=True
)



# Sidebar con información del usuario y carrito
with st.sidebar:
    st.markdown(f"### 👤 {st.session_state['usuario']['nombre']}")

    if st.button("🚪 Cerrar Sesión"):
        st.session_state.clear()
        st.rerun()

    st.markdown("---")

    # Carrito de compras
    st.markdown("### 🛒 Carrito")
    if st.session_state.cart:
        total = 0
        for item in st.session_state.cart:
            st.markdown(f"""
            <div class="cart-item">
                <strong>{item['name']}</strong><br>
                ${item['price']:.2f} x {item['quantity']}
            </div>
            """,unsafe_allow_html=True)
            total += item["price"] * item["quantity"]

        st.markdown(f"**Total: ${total:.2f}**")

        stripe_button = create_stripe_button(
            st.session_state.cart, 
            st.session_state['usuario']['email'], 
            st.session_state['usuario']['uid']
        )

        if stripe_button:
            st.markdown(stripe_button, unsafe_allow_html=True)
        else:
            st.error("Error al crear la sesión de pago")

    else:
        st.info("Tu carrito está vacío")   

# Contenido principal - Catálogo de productos
st.markdown("## 🛍️ Catálogo de Productosy Servicios")

    # Filtros
col1, col2 = st.columns([1, 3])
with col1:
    categories = [
            "comida china",
            "El corral",
            'El carriel',
            "Qbano",
            'magdalena',
            "supermercado",
            "tiendas D1",
            "cobijas y cortinas",
            "plomeria"
            
    ]
    selected_category = st.selectbox("Categoría", categories,index=0)
if 'productos' not in st.session_state:
    with st.spinner("🛵 Cargando productos disponibles..."):
        st.session_state['productos'] = get_products()

products = st.session_state['productos']
if selected_category != "todos":
    products = [p for p in products if p.get('category') == selected_category]


    # Mostrar productos en grid
if products:
    # Crear grid de productos
    cols = st.columns(3)

    for idx, product in enumerate(products):
        with cols[idx % 3]:
            

            # Construimos el mensaje dinámico
            mensaje = f"Hola, estoy interesado en el producto: {product['name']} {product['description']} con precio ${product['price']:.2f}. mi dirección es: "
            mensaje_url = urllib.parse.quote(mensaje)

            
            st.markdown(f"""
                <div class="product-card" style="text-align:center;">
                    <img src="{product['image']}" style="width: 100%; height: 200px; object-fit: cover; border-radius: 10px;">
                    <h3 style="margin: 1rem 0 0.5rem 0; color: #333;">{product['name']}</h3>
                    <p style="color: #666; margin-bottom: 1rem;">{product['description']}</p>
                    <div style="display: flex; justify-content: center; align-items: center; gap: 10px; margin-bottom: 1rem;">
                        <div class="price-tag" style="background-color:#FF5C5C;padding:0.5rem 1rem;border-radius:12px;display:inline-block;">
                            ${product['price']:.2f}
                        </div>
                        <a href="https://wa.me/573009135244?text={mensaje_url}" target="_blank" style="text-decoration:none;">
                            <button style="background-color:#FF5C5C;padding:0.5rem 1rem;border-radius:12px;display:inline-block;border:none;color:white;cursor:pointer;">
                                Chat
                            </button>
                        </a>
                    </div>
                </div>
            """, unsafe_allow_html=True)

            col4, col5, col6 = st.columns([0.5,2,0.5])
            with col5:
                st.markdown(
                    f"""
                   <button style="
                        background: linear-gradient(45deg, #667eea, #764ba2);
                        color: white;
                        border: none;
                        border-radius: 25px;
                        padding: 0.75rem 2rem;
                        font-weight: bold;
                        cursor: pointer;
                    ">
                        Pagar el producto
                    </button>

                        """,
                        unsafe_allow_html=True
                    )


    


           

# Footer
st.markdown("---")
st.markdown(
    """
    <div style="text-align: center; padding: 2rem;">
        <p>🛵 DOMIRAY SAS - Empresa de domicilios Casanareña</p>
        <p>Esta app fue desarrollada por Rodrigo Patiño usando Streamlit, Firebase y Stripe</p>
    </div>
    """,
    unsafe_allow_html=True
)







