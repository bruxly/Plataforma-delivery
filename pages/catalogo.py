import streamlit as st
import stripe
import os
from datetime import datetime
from PIL import Image
from io import BytesIO
import urllib.parse
import hashlib



DEV_MODE = True  # Cambia a False en producción


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
    #global DEV_MODE
    products_ref = st.session_state.db.collection("products")

    if DEV_MODE:
        # 🧹 Elimina productos existentes
        for doc in products_ref.stream():
            doc.reference.delete()

            # 🧩 Productos locales (puedes editarlos)
        sample_products = [

            #la tribu
            {
                "name": "La tribu",
                "price": 20000,
                "image": "https://i.imgur.com/JMWsAMd.jpeg",
                "description": "cod:01. 10 piezas de alitas, papa francesa, ensalada y cascajos verdes",
                "category": "Comidas Rapidas", 
                "subcategory": "La tribu",
            },
            #la tribu
            {
                "name": "La tribu",
                "price": 24000,
                "image": "https://i.imgur.com/dAkTO5v.jpeg",
                "description": "cod:02. 250 gr de carne, papa francesa, plátano chip y ensalada DM ",
                "category": "Comidas Rapidas", 
                "subcategory": "La tribu",       
            },

            #la tribu
            {
                "name": "La tribu",
                "price": 30000,
                "image": "https://i.imgur.com/F27p0hz.jpeg",
                "description": "cod:03. Pechuga en salsa camarones, toxineta,queso gratinado,papa francesa,modedas verdes y aguacate  ",
                "category": "Comidas Rapidas", 
                "subcategory": "La tribu",       
            },
            #la tribu
            {
                "name": "La tribu",
                "price": 17000,
                "image": "https://i.imgur.com/WpAu4Hk.jpeg",
                "description": "cod:04. Mazorcada tradicional,carne,pollo,salchicha,chorizo,papa francesa y maiz.",
                "category": "Comidas Rapidas", 
                "subcategory": "La tribu",       
            },
             #la tribu
            {
                "name": "La tribu",
                "price": 27000,
                "image": "https://i.imgur.com/8RAX5Xi.jpeg",
                "description": "cod:05. Costillas BBQ, plátano chips, carne, pollo, salchicha, chorizo, queso gratinado y papa francesa.",
                "category": "Comidas Rapidas", 
                "subcategory": "La tribu",       
            },
            #la tribu
            {
                "name": "La tribu",
                "price": 15000,
                "image": "https://i.imgur.com/fUhVmxi.jpeg",
                "description": "cod:06. Carne, pollo, salchicha, chorizo, queso gratinado, papa francesa y papa fosforito.",
                "category": "Comidas Rapidas", 
                "subcategory": "La tribu",      
            },
             #la tribu
            {
                "name": "La tribu",
                "price": 10000,
                "image": "https://i.imgur.com/knXC1RY.jpeg",
                "description": "cod:07. Choriperro.",
                "category": "Comidas Rapidas", 
                "subcategory": "La tribu",       
            },
             #la tribu
            {
                "name": "La tribu",
                "price": 21500,
                "image": "https://i.imgur.com/BPtYSRR.jpeg",
                "description": "cod:08. Hamburguesa BBQ 150 g de carne, queso de doble crema, costilla bbq, huevo, tocineta y papas a la francesa.",
                "category": "Comidas Rapidas", 
                "subcategory": "La tribu",       
            },
             #la tribu
            {
                "name": "La tribu",
                "price": 24000,
                "image": "https://i.imgur.com/KGtDc8f.jpeg",
                "description": "cod:09. Costillas BBQ 250 g de costilla bbq, papa francesa, ensalada y salsa de la casa.",
                "category": "Comidas Rapidas", 
                "subcategory": "La tribu",       
            },
             #la tribu
            {
                "name": "La tribu",
                "price": 14000,
                "image": "https://i.imgur.com/FnxomFP.jpeg",
                "description": "cod:10. Hot dog Ranchero.",
                "category": "Comidas Rapidas", 
                "subcategory": "La tribu",       
            },
             #la tribu
            {
                "name": "La tribu",
                "price": 0,
                "image": "https://i.imgur.com/GhQ7CK1.jpeg",
                "description": "cod:11. ",
                "category": "Comidas Rapidas", 
                "subcategory": "La tribu",       
            },
            #la tribu
            {
                "name": "La tribu",
                "price": 0,
                "image": "https://i.imgur.com/OKhW7Vj.jpeg",
                "description": "cod:12.",
                "category": "Comidas Rapidas", 
                "subcategory": "La tribu",       
            },
            #la tribu
            {
                "name": "La tribu",
                "price": 0,
                "image": "https://i.imgur.com/ukNamRy.jpeg",
                "description": "cod:13",
                "category": "Comidas Rapidas", 
                "subcategory": "La tribu",       
            },
            #la tribu
            {
                "name": "La tribu",
                "price": 0,
                "image": "https://i.imgur.com/2T3Ec7T.jpeg",
                "description": "cod:14",
                "category": "Comidas Rapidas", 
                "subcategory": "La tribu",       
            },
            #la tribu
            {
                "name": "La tribu",
                "price": 0,
                "image": "https://i.imgur.com/YRt67vg.jpeg",
                "description": "cod:15",
                "category": "Comidas Rapidas", 
                "subcategory": "La tribu",       
            },
            #Punky chicarron
            {
                "name": "Punky",
                "price": 30000,
                "image": "https://i.imgur.com/zf5R5oc.jpeg",
                "description": "cod:01 Calentao de arroz y frijol,aguacate,patacón,hogao y chicarron 150g",
                "category": "Comidas Rapidas",
                "subcategory": "Punky Chicarron",       
            },
            #Punky 
            {
                "name": "Punky",
                "price": 26000,
                "image": "https://i.imgur.com/vL3LUTA.jpeg",
                "description": "cod:02 Lomo de cerdo,chirrarron carnudo,queso,vegetales,piña, chips de plátano",
                "category": "Punky Chicarron",       
            },
            #Punky 
            {
                "name": "Punky",
                "price": 45000,
                "image": "https://i.imgur.com/vKPXMAS.jpeg",
                "description": "cod:03 Corte 100 una costilla entera con chirraron,patacón,hogao,guacamole y suero",
                "category": "Comidas Rapidas",
                "subcategory": "Punky Chicarron",       
            },
             #Punky 
            {
                "name": "Punky",
                "price": 27000,
                "image": "https://i.imgur.com/dNBreze.jpeg",
                "description": "cod:04 Chuleta lomo apanado, arroz, aguacate, maduro y hogao",
                "category": "Comidas Rapidas",
                "subcategory": "Punky Chicarron",       
            },

            #Punky 
            {
                "name": "Punky",
                "price": 35000,
                "image": "https://i.imgur.com/3JKCVmx.jpeg",
                "description": "cod:05 frijol, arroz, maduro, aguacate, chicarron y huevo frito ",
                "category": "Comidas Rapidas",
                "subcategory": "Punky Chicarron",       
            },
            #Punky 
            {
                "name": "Punky",
                "price": 32000,
                "image": "https://i.imgur.com/m2pIO58.jpeg",
                "description": "cod:06 Cazuela frijol, plátano, aguacate, chorizo y chicarron",
                "category": "Comidas Rapidas",
                "subcategory": "Punky Chicarron",       
            },
            #Punky 
            {
                "name": "Punky",
                "price": 33000,
                "image": "https://i.imgur.com/315Q4G5.jpeg",
                "description": "cod:07 Costillas en salsa BBQ artesanal, acompañadas de papa, yuca o plátano, guacamole y suero.",
                "category": "Comidas Rapidas",
                "subcategory": "Punky Chicarron",       
            },

            #Punky 
            {
                "name": "Punky",
                "price": 26000,
                "image": "https://i.imgur.com/h91sd9n.jpeg",
                "description": "cod:07 Chicharron carnudo 200g, papa, yuca o platano, guacamole y suero.",
                "category": "Comidas Rapidas",
                "subcategory": "Punky Chicarron",       
            },
            
            #vaquita costeña
            {
                "name": "Vaquita Costeña",
                "price": 0,
                "image": "https://i.imgur.com/eNn0Blr.jpeg",
                "description": "cod:01. Vaquita Quesuda papa francesa, cerdo, pollo, ranchera, maiz, queso, cabello de angel, lechuga..",
                "category": "Comidas Rapidas",
                "subcategory": "Vaquita Costeña",          
            },
            #vaquita costeña
            {
                "name": "Vaquita Costeña",
                "price": 0,
                "image": "https://i.imgur.com/EdvytEF.jpeg",
                "description": "cod:02. Picada Mixta papa francesa, carne, pollo, chorizo, butifarra, maíz, cabello de ángel, lechuga, queso costeño.",
                "category": "Comidas Rapidas",
                "subcategory": "Vaquita Costeña",      
            },
            
            
            #el corral
                
            {
                "name": "Todoterreno Clasica en combo",
                "price": 43900,
                "image": "https://i.imgur.com/l4Nb5BG.jpeg",
                "description": "cod:01. dos carnes de 125g cada una",
                "category": "Comidas Rapidas",
                "subcategory": "El Corral", 
            },
            #el corral
            {
                "name": "Todoterreno Tocineta en Combo",
                "price": 45900,
                "image": "https://i.imgur.com/xgFtkGx.jpeg",
                "description": "cod:02. dos carnes de 125g cada una",
                "category": "Comidas Rapidas",
                "subcategory": "El Corral",
            },
            #el corral
            {
                "name": "Todoterreno Clasica",
                "price": 35900,
                "image": "https://i.imgur.com/7i5h1T4.jpeg",
                "description": "cod:03. dos carnes de 125g cada una",
                "category": "Comidas Rapidas",
                "subcategory": "El Corral",
            },
            #el corral
            {
                "name": "Todoterreno Callejera",
                "price": 37900,
                "image": "https://i.imgur.com/PsjQLna.jpeg",
                "description": "cod:04. dos carnes de 125g cada una",
                "category": "Comidas Rapidas",
                "subcategory": "El Corral",
            },
            #el corral
            {
                "name": "Todoterreno Tocineta",
                "price": 37900,
                "image": "https://i.imgur.com/XTBJnYc.jpeg",
                "description": "cod:05. dos carnes de 125g cada una",
                "category": "Comidas Rapidas",
                "subcategory": "El Corral",
            },
            #el corral
            {
                "name": "Corralita",
                "price": 22900,
                "image": "https://i.imgur.com/a3H6uCS.jpeg",
                "description": "cod:06. Carne de 90g,tomate y cebolla en rodajas",
                "category": "Comidas Rapidas",
                "subcategory": "El Corral",
            },

            {  
                "name": "Corral",
                "price": 23900,
                "image": "https://i.imgur.com/l9VNcfu.jpeg",
                "description": "cod:07. Carne de 125g,tomate y cebolla en rodajas",
                "category": "Comidas Rapidas",
                "subcategory": "El Corral",
            },
            #el corral
            {
                "name": "Corral Pollo",
                "price": 25900,
                "image": "https://i.imgur.com/dK9p11X.jpeg",
                "description": "cod:08. Pechuga de pollo de 154g con salsa bbq.",
                "category": "Comidas Rapidas",
                "subcategory": "El Corral",
            },

              #el corral  
            {
                "name": "Callejero En Combo",
                "price": 28900,
                "image": "https://i.imgur.com/3bJtjzW.png",
                "description": "cod:09. Con salchicha de 115g a la parrilla.",
                "category": "Comidas Rapidas",
                "subcategory": "El Corral",
            },
            #el corral
            {
                "name": "Hawaiano Combo",
                "price": 32900,
                "image": "https://i.imgur.com/pfkNBGy.jpeg",
                "description": "cod:10. Con salchicha a la parrilla, queso,piña y salsas",
                "category": "Comidas Rapidas",
                "subcategory": "El Corral",
            },
            #EL CARRIEL
            {
                "name": "El Carriel",
                "price": 32000,
                "image": "https://i.imgur.com/xAvOav3.png",
                "description": "cod:01. Un Kilo de arroz paisa con chicharron te alcanza pa' 2 o 3 personas",
                "category": "El carriel",
            },
            #EL CARRIEL
            {
                "name": "El Carriel",
                "price": 18000,
                "image": "https://i.imgur.com/tHviOSw.jpeg",
                "description": "cod:02. Personal con papitas, Porción personal de arroz paisa con papitas y limonada",
                "category": "El carriel",
            },
            #el carriel
            {
                "name": "El carriel",
                "price": 60000,
                "image": "https://i.imgur.com/sVWsjG8.jpeg",
                "description": "cod:03. merrada de dos kilos de arroz Paisa y Chicharrón. Oiga! Y rinde hasta pa' 6 personas ",
                "category": "El carriel",
            },
            #el carriel
            {
                "name": "El carriel",
                "price": 32000,
                "image": "https://i.imgur.com/t0xczti.jpeg",
                "description": "cod:04. 750 Grs de Arroz Paisa acompañados de papitas a la francesa ideal para compartir",
                "category": "El carriel",
            },
            #el carriel
            {
                "name": "El carriel",
                "price": 90000,
                "image": "https://i.imgur.com/qvPftTI.jpeg",
                "description": "cod:05. Donde come 8 comen 10, EXTRA FAMILIAR con semejante merrada de arroz Paisa.",
                "category": "El carriel",
            }, 
             #el carriel
            {
                "name": "El carriel",
                "price": 18000,
                "image": "https://i.imgur.com/pDfMwf6.jpeg",
                "description": "cod:06. Cajita personal con una libra de arroz paisa y vaso de limonada del día ",
                "category": "El carriel",
            },    

            #MAGDALENA
            {
                "name": "Magdalena",
                "price": 48000,
                "image": "https://i.imgur.com/VX1OoNT.png",
                "description": "cod:01. Mulata Torta a elección: chocolate, zanahoria o naranja ",
                "category": "magdalena",
            },
             #MAGDALENA
            {
                "name": "Magdalena",
                "price": 78000,
                "image": "https://i.imgur.com/05RR79d.png",
                "description": "cod:02. Me Latte Elixir de frutas Sándwich Llanero",
                "category": "magdalena",
            },

            #MAGDALENA
            {
                "name": "Magdalena",
                "price": 59000,
                "image": "https://i.imgur.com/lZGVX0C.png",
                "description": "cod:03. Antojo ácido 🥭🧋Mini fresas🍓Sandwich de pollo Napoleón",
                "category": "magdalena",
            },

            #MAGDALENA
                {
                "name": "Magdalena",
                "price": 52000,
                "image": "https://i.imgur.com/XPuJn5F.png",
                "description": "cod:04. Cherrymocca🧋Sándwich Marco polo🥪",
                "category": "magdalena",
            },

            #MAGDALENA
            {
                "name": "Magdalena",
                "price": 46000,
                "image": "https://i.imgur.com/JHY6d7o.png",
                "description": "cod:05. Smoothie frutos rojos 🥤Torta de chocolate, zanahoria o naranja🎂",
                "category": "magdalena",
            },

            #MAGDALENA
            {
                "name": "Magdalena",
                "price": 65000,
                "image": "https://i.imgur.com/IaUeplo.png",
                "description": "cod:06. Me Latte🧋Mini Elixir ✨Sándwich de pollo Napoleón🥪",
                "category": "magdalena",
            },

            
            #MAGDALENA
            {
                "name": "Magdalena",
                "price": 23000,
                "image": "https://i.imgur.com/MaI4Nox.png",
                "description": "cod:07. Con crema chantilly, topping de chocolate o lecherita.",
                "category": "magdalena",
            },

            
            #MAGDALENA
            {
                "name": "Magdalena",
                "price": 23000,
                "image": "https://i.imgur.com/ldV1vj7.png",
                "description": "cod:08. Fressas con durazno Con crema chantilly, topping de chocolate o lecherita.",
                "category": "magdalena",
            },

            #MAGDALENA
            {
                "name": "Magdalena",
                "price": 18000,
                "image": "https://i.imgur.com/HsqYXky.png",
                "description": "cod:09. Delicioso Bowl fresas con helado.",
                 "category": "magdalena",
            },

            #MAGDALENA
            {
                "name": "Magdalena",
                "price": 25000,
                "image": "https://i.imgur.com/e897HRS.png",
                "description": "cod:10. Mini fresas kiwi X3, durazno con chantilly y topping de chocolate.",
                "category": "magdalena",
            },

            # QUBANO
            {
                "name": "Qbano",
                "price": 30600,
                "image": "https://i.imgur.com/tyul788.jpeg",
                "description": "cod:01. Sándwich Ropa Vieja En Combo",
                "category": "Qbano",
            },
             # QUBANO
            {
                "name": "Qbano",
                "price": 24600,
                "image": "https://i.imgur.com/4EXltWq.jpeg",
                "description": "cod:02. Sándwich Especial Combo",
                "category": "Qbano",
            },
            {
                "name": "Qbano",
                "price": 27600,
                "image": "https://i.imgur.com/1UhLhOe.jpeg",
                "description": "cod:03. Sándwich Súper Especial Combo",
                "category": "Qbano",
            },
             # QUBANO
            {
                "name": "Qbano",
                "price": 29600,
                "image": "https://i.imgur.com/NVfqHoc.jpeg",
                "description": "cod:04. Sándwich Roast Beef Combo",
                "category": "Qbano",
            },

             # QUBANO

            {
                "name": "Qbano",
                "price": 29600,
                "image": "https://i.imgur.com/0U7wPHo.jpeg",
                "description": "cod:05. Sándwich Cordero Combo",
                "category": "Qbano",
            },
             # QUBANO
            {
                "name": "Qbano",
                "price": 29600,
                "image": "https://i.imgur.com/2IRMt6B.jpeg",
                "description": "cod:06. Sándwich Pollo Combo",
                "category": "Qbano",
            },
             # QUBANO vegetariano
            {
                "name": "Qbano Vegetariano",
                "price": 25900,
                "image": "https://b2cqbano.vtexassets.com/arquivos/ids/156056-800-auto?v=638843436041770000&width=800&height=auto&aspect=true",
                "description": "cod:20. combinación de proteína, verduras y arroz con todo el sabor Qbano",
                "category": "Comida Vegetariana",
            },
            # QUBANO vegetariano
            {
                "name": "Qbano Vegetariano",
                "price": 31900,
                "image": "https://b2cqbano.vtexassets.com/arquivos/ids/156094-800-auto?v=638843455088070000&width=800&height=auto&aspect=true",
                "description": "cod:21. combinación de proteína, verduras y arroz con todo el sabor Qbano",
                "category": "Comida Vegetariana",
            },
            # QUBANO vegetariano
            {
                "name": "Qbano Vegetariano",
                "price": 27600,
                "image": "https://b2cqbano.vtexassets.com/arquivos/ids/156160-800-auto?v=638846752535070000&width=800&height=auto&aspect=true",
                "description": "cod:22. Tamaño personal 21 cm",
                "category": "Comida Vegetariana",
            },
             # QUBANO vegetariano
            {
                "name": "Qbano Vegetariano",
                "price": 22300,
                "image": "https://b2cqbano.vtexassets.com/arquivos/ids/156158-800-auto?v=638846752223630000&width=800&height=auto&aspect=true",
                "description": "cod:23. Tamaño personal 21 cm",
                "category": "Comida Vegetariana",
            },
            # QUBANO vegetariano
            {
                "name": "Qbano Vegetariano",
                "price": 27600,
                "image": "https://b2cqbano.vtexassets.com/arquivos/ids/156062-800-auto?v=638843439879430000&width=800&height=auto&aspect=true",
                "description": "cod:23. Sándwich ahora en Wrap, con acompañante y bebida",
                "category": "Comida Vegetariana",
            },
                    # QUBANO vegetariano
            {
                "name": "Qbano Vegetariano",
                "price": 22300,
                "image": "https://b2cqbano.vtexassets.com/arquivos/ids/156061-800-auto?v=638843439532930000&width=800&height=auto&aspect=true",
                "description": "cod:24. Sándwich ahora en Wrap, con acompañante y bebida",
                "category": "Comida Vegetariana",
            },
                
            #comida china
            {
                "name": "Combo Pollo",
                "price": 33000,
                "image": "https://i.imgur.com/UajBfHQ.jpeg",
                "description": "cod:01. 1/4 de pollo, papas y arroz.",
                "category": "comida china",
            },
            #comida china
            {
                "name": "Media Valenciana",
                "price": 39000,
                "image": "https://i.imgur.com/2ZXIdcA.jpeg",
                "description": "cod:02. 1/4 de pollo, arroz chino.",
                "category": "comida china",
            },
            #comida china
            {
                "name": "Combo Chop Suey",
                "price": 33000,
                "image": "https://i.imgur.com/7iCQYxg.jpeg",
                "description": "cod:03. papas,chop suey y arroz chino.",
                "category": "comida china",
            },
            #comida china
            {
                "name": "Valenciana",
                "price": 46000,
                "image": "https://i.imgur.com/cKI8mR9.jpeg",
                "description": "cod:04. Arroz para 4 personas y medio pollo frito.",
                "category": "comida china",
            },
            #comida china
            {
                "name": "Arroz Chino",
                "price": 46000,
                "image": "https://i.imgur.com/evczF8R.jpeg",
                "description": "cod:05. Arroz para 4 personas con pollo desmellado.",
                "category": "comida china",
            },
            #comida china
            {
                "name": "Combo Camaron",
                "price": 33000,
                "image": "https://i.imgur.com/U4UKNAI.jpeg",
                "description": "cod:06. Arroz con camaron para dos personas y una porción de papas.",
                "category": "comida china",
            },
            #comida china
            {
                "name": "Yon Chow Fan",
                "price": 57000,
                "image": "https://i.imgur.com/BH2d8Ho.jpeg",
                "description": "cod:07. Arroz,carne,jamon,pollo desmechado,raizes chinas,verduras y camaron grande,.",
                "category": "comida china",
            },
                

             #supermercados
                
            {
                "name": "Los Ocobos",
                "price": 11400,
                "image": "https://i.imgur.com/IGHnkaE.jpeg",
                "description": "cod:01. Aceite 900ml",
                "category": "Supermercados",
                "category": "Los Ocobos",
            },
                

            {
                "name": "Los Ocobos",
                "price": 14500,
                "image": "https://i.imgur.com/BTWJj1W.jpeg",
                "description": "cod:02. Cubeta de huevos",
                "category": "Supermercados",
                "subcategory": "Los Ocobos"
            },

                
            {
                "name": "Los Ocobos",
                "price": 6100,
                "image": "https://i.imgur.com/alzkciX.jpeg",
                "description": "cod:03. Salchicha Zenú, 5 und",
                "category": "Supermercados",
                "subcategory": "Los Ocobos"
            },

            {
                "name": "Los Ocobos",
                "price": 2200,
                "image": "https://i.imgur.com/vUyo1uM.jpeg",
                "description": "cod:04. Arroz 460g ",
                "category": "Supermercados",
                "subcategory": "Los Ocobos"
            },
            {
                "name": "Los Ocobos",
                "price": 6800,
                'image':'https://i.imgur.com/CdWQwAS.jpeg',
                "description": "cod:05. DON CAT 500g",
                "category": "Supermercados",
                "subcategory": "Los Ocobos"
            },

            {
                "name": "Los Ocobos",
                "price": 8500,
                "image": "https://i.imgur.com/8mYeRbM.png",
                "description": "cod:06. Coca-cola 2.5lts",
                "category": "Supermercados",
                "subcategory": "Los Ocobos"
            },
                
           #Tiendas D1 leche
            {
                "name": "Tiendas D1",
                "price": 3050,
                "image": "https://i.imgur.com/zqm2ji5.png",
                "description": "cod:01. Deslactosada 900ml",
                "category": "tiendas D1",
            },
            #Tiendas D1 leche
            {
                "name": "Tiendas D1",
                "price": 3350,
                "image": "https://i.imgur.com/toiCwNd.png",
                "description": "cod:02. Leche Entera 900ml",
                "category": "tiendas D1",
            },
            #Tiendas D1 leche

            {
                "name": "Tiendas D1",
                "price": 8300,
                "image": "https://i.imgur.com/IEdmQX3.png",
                "description": "cod:03 En Polvo Entera 350g",
                "category": "Supermercados", 
                "subcategory": "Tiendas D1",
            },
            #Tiendas D1 leche
            {
                "name": "Tiendas D1",
                "price": 1200,
                "image": "https://i.imgur.com/86A2hwi.png",
                "description": "cod:04 Leche Entera 200ml",
                "category": "Supermercados", 
                "subcategory": "Tiendas D1",
            },

            #tiendas D1 Queso
            {
                "name": "Tiendas D1",
                "price": 5490,
                "image": "https://i.imgur.com/hSNhJGd.png",
                "description": "cod:15 Queso Mozzarella Bufala 100g",
                "category": "Supermercados", 
                "subcategory": "Tiendas D1",
            },
            #Tiendas D1 Queso 
            {
                "name": "Tiendas D1",
                "price": 8750,
                "image": "https://i.imgur.com/LzbTraU.png",
                "description": "cod:16. Queso Campesino Bloque 350g",
                "category": "tiendas D1",
            },
            #Tiendas D1 queso
            {
                "name": "Tiendas D1",
                "price": 3300,
                "image": "https://i.imgur.com/2FRw5OC.png",
                "description": "cod:17. Queso Crema 200g",
                "category": "Supermercados", 
                "subcategory": "Tiendas D1",
            },
            #Tiendas D1 Queso
            {
                "name": "Tiendas D1",
                "price": 13650,
                "image": "https://i.imgur.com/1Z4zfQQ.png",
                "description": "cod:18. Queso Parmesano Alpina 120g",
                "category": "Supermercados", 
                "subcategory": "Tiendas D1",
            },
            #Tiendas D1 Queso
            {
                "name": "Tiendas D1",
                "price": 9900,
                "image": "https://stockimages.tiendasd1.com/stockimages.tiendasd1.com/kobastockimages/IMAGENES/12000084/queso-mozzarella-tajado-latti-400-grs-01.png",
                "description": "cod:19. Queso tajado 18 tajadas 400 grs",
                "category": "Supermercados", 
                "subcategory": "Tiendas D1",
            },
            #Tiendas D1 Queso
            {
                "name": "Tiendas D1",
                "price": 9300,
                "image": "https://stockimages.tiendasd1.com/stockimages.tiendasd1.com/kobastockimages/IMAGENES/12006207/queso-mozzarella-tajado-x-250g-latti-01.png",
                "description": "cod:20. Queso tajado 15 tajadas 250 grs",
                "category": "Supermercados", 
                "subcategory": "Tiendas D1",
            },
            

            

            #Tiendas D1 salchicha
            
            {
                "name": "Tiendas D1",
                "price": 9300,
                "image": "https://i.imgur.com/gnC8O4x.png",
                "description": "cod:30 Salchicha Camprestre 400g",
                "category": "Supermercados", 
                "subcategory": "Tiendas D1",
            },
            #Tiendas D1 chorizo
            {
                "name": "Tiendas D1",
                "price": 7990,
                "image": "https://i.imgur.com/FuUuoUV.png",
                "description": "cod:45 Chorizo Santarrosano 225g",
                "category": "Supermercados", 
                "subcategory": "Tiendas D1",
            },
            #Tiendas D1 chorizo
            {
                "name": "Tiendas D1",
                "price": 7990,
                "image": "https://i.imgur.com/v7J7Klr.png",
                "description": "cod:46 Chorizo Antioqueño 225g",
                "category": "Supermercados", 
                "subcategory": "Tiendas D1",
            },

             
            #Tiendas D1 galletas
            {
                "name": "Tiendas D1",
                "price": 6600,
                "image": "https://i.imgur.com/pChtWsT_d.jpeg?maxwidth=520&shape=thumb&fidelity=high",
                "description": "cod:60 saltin noe, 5 tacos 410 gms",
                "category": "Supermercados", 
                "subcategory": "Tiendas D1",
            },
            #Tiendas D1 galletas
            {
                "name": "Tiendas D1",
                "price": 5700,
                "image": "https://stockimages.tiendasd1.com/stockimages.tiendasd1.com/kobastockimages/IMAGENES/12000096/galleta-2-tacos-ducales-noel-241-grs-01.png",
                "description": "cod:61. Galletas 2 tacos noel 241g",
                "category": "Supermercados", 
                "subcategory": "Tiendas D1",
            },
            #Tiendas D1 galletas
            {
                "name": "Tiendas D1",
                "price": 4650,
                "image": "https://stockimages.tiendasd1.com/stockimages.tiendasd1.com/kobastockimages/IMAGENES/12005070/galletas-happy-wafer-x-12-und-288g-01.png",
                "description": "cod:62. Galletas happy wafer 12 unidades ",
                "category": "Supermercados", 
                "subcategory": "Tiendas D1",
            },
            #Tiendas D1 azucar
            {
                "name": "Tiendas D1",
                "price": 4150,
                "image": "https://i.imgur.com/ydGhqpe.jpeg",
                "description": "cod:75. Azucar morena 10000 grs",
                "category": "Supermercados", 
                "subcategory": "Tiendas D1",
            },
            #Tiendas D1 azucar
            {
                "name": "Tiendas D1",
                "price": 6150,
                "image": "https://i.imgur.com/JQD4LEm.jpeg",
                "description": "cod:76. Endulzante con stevia natri 180 grs",
                "category": "Supermercados", 
                "subcategory": "Tiendas D1",
            },
            #tiendas d1 arvejas
            {
                "name": "Tiendas D1",
                "price": 5990,
                "image": "https://stockimages.tiendasd1.com/stockimages.tiendasd1.com/kobastockimages/IMAGENES/12006459/arveja-verde-congelada-cooltivo-500-g-01.png",
                "description": "cod:80 Arveja verde congelada 500g",
                "category": "Supermercados", 
                "subcategory": "Tiendas D1",
            },
            #tiendas d1 lenteja
            {
                "name": "Tiendas D1",
                "price": 3200,
                "image": "https://stockimages.tiendasd1.com/stockimages.tiendasd1.com/kobastockimages/IMAGENES/12000042/lenteja-el-estio-500-grs-01.png",
                "description": "cod:85. Lenteja el estio 500g",
                "category": "Supermercados", 
                "subcategory": "Tiendas D1",
            },
            #tiendas d1 arina de trigo
            {
                "name": "Tiendas D1",
                "price": 1700,
                "image": "https://stockimages.tiendasd1.com/stockimages.tiendasd1.com/kobastockimages/IMAGENES/12001162/harina-de-trigo-cereales-harinas-y-premezclas-12001162-1.png",
                "description": "cod:88. Harina de trigo quicksy 500g",
                "category": "tiendas D1",
            },
            #tiendas d1 arina de trigo en plovo
            {
                "name": "Tiendas D1",
                "price": 2150,
                "image": "https://stockimages.tiendasd1.com/stockimages.tiendasd1.com/kobastockimages/IMAGENES/12003539/0722.png",
                "description": "cod:89. Harina de trigo con plovo para hornear 500g",
                "category": "Supermercados", 
                "subcategory": "Tiendas D1",
            },
            #tiendas d1 arroz
            {
                "name": "Tiendas D1",
                "price": 1990,
                "image": "https://stockimages.tiendasd1.com/stockimages.tiendasd1.com/kobastockimages/IMAGENES/12002073/arroz-diana-500-g-01.png",
                "description": "cod:90. Arroz Diana 500g",
                "category": "Supermercados", 
                "subcategory": "Tiendas D1",
            },

            #Tiendas D1 SAL
            {
                "name": "Tiendas D1",
                "price": 2550,
                "image": "https://stockimages.tiendasd1.com/stockimages.tiendasd1.com/kobastockimages/IMAGENES/12002874/caldo-de-gallina-condimentos-12002946-1.png",
                "description": "cod:97. sal refisal 1000 g ",
                "category": "Supermercados", 
                "subcategory": "Tiendas D1",
            },

            
            #Tiendas D1 ACEITES
            {
                "name": "Tiendas D1",
                "price": 19950,
                "image": "https://i.imgur.com/r4FmWWM_d.jpeg?maxwidth=520&shape=thumb&fidelity=high",
                "description": "cod:001. Aceite de oliva extra virgen 500ml",
                "category": "Supermercados", 
                "subcategory": "Tiendas D1",
            },
            #Tiendas D1 ATUN
            {
                "name": "Tiendas D1",
                "price": 5990,
                "image": "https://stockimages.tiendasd1.com/stockimages.tiendasd1.com/kobastockimages/IMAGENES/12005690/duopack-atun-en-agua-c-f-160-g-neto-01.png",
                "description": "cod:010. Atún en agua x 2",
                "category": "Supermercados", 
                "subcategory": "Tiendas D1",
            },
            #Tiendas D1 ATUN
            {
                "name": "Tiendas D1",
                "price": 7990,
                "image": "https://stockimages.tiendasd1.com/stockimages.tiendasd1.com/kobastockimages/IMAGENES/12004368/duopack-atun-a.oliva-cf-160-g-neto-01.png",
                "description": "cod:002. Atún x 2 aceite de oliva",
                "category": "Supermercados", 
                "subcategory": "Tiendas D1",
            },


            #Tiendas D1 Avena hojuelas
            {
                "name": "Tiendas D1",
                "price": 1400,
                "image": "https://stockimages.tiendasd1.com/stockimages.tiendasd1.com/kobastockimages/IMAGENES/12000457/avena-en-hojuelas-fit-graan-250-g-01.png",
                "description": "cod:010. Avena en hojuelas fit graan 250g",
                "category": "Supermercados", 
                "subcategory": "Tiendas D1",
            },
            #Tiendas D1 cafe
            {
                "name": "Tiendas D1",
                "price": 16950,
                "image": "https://stockimages.tiendasd1.com/stockimages.tiendasd1.com/kobastockimages/IMAGENES/12006609/cafe-sello-rojo-300g-01.png",
                "description": "cod:015 Cafe sello rojo 300g",
                "category": "Supermercados", 
                "subcategory": "Tiendas D1",
            },
            
            #Tiendas D1 salsa de tomate
            {
                "name": "Tiendas D1",
                "price": 4490,
                "image": "https://stockimages.tiendasd1.com/stockimages.tiendasd1.com/kobastockimages/IMAGENES/12000266/salsa-de-tomate-zev-500-g-01.png",
                "description": "cod:025. Salsa de tomate zev 500g",
                "category": "Supermercados", 
                "subcategory": "Tiendas D1",
            },
            
            
            #Tiendas D1 arepas
            {
                "name": "Tiendas D1",
                "price": 1990,
                "image": "https://i.imgur.com/PNtDPaH.png",
                "description": "cod:035. Arepa Minitela 600g",
                "category": "Supermercados", 
                "subcategory": "Tiendas D1",
            },
            #Tiendas D1 arepas
            {
                "name": "Tiendas D1",
                "price": 1890,
                "image": "https://i.imgur.com/BB48JmZ.png",
                "description": "cod:036. Arepa Blanca 500g",
                "category": "Supermercados", 
                "subcategory": "Tiendas D1",
            },
            #Tiendas D1 pan tajado
            {
                "name": "Tiendas D1",
                "price": 5990,
                "image": "https://stockimages.tiendasd1.com/stockimages.tiendasd1.com/kobastockimages/IMAGENES/12005835/pan-tajado-multigranos-450-g-01.png",
                "description": "cod:045. Pan tajado multigranos 450g",
                "category": "Supermercados", 
                "subcategory": "Tiendas D1",
            },
            #Tiendas D1 pan tajado
            {
                "name": "Tiendas D1",
                "price": 3650,
                "image": "https://stockimages.tiendasd1.com/stockimages.tiendasd1.com/kobastockimages/IMAGENES/12005834/pan-tajado-mantequilla-450g-01.png",
                "description": "cod:046. Pan tajado mantequilla 450g",
                "category": "Supermercados", 
                "subcategory": "Tiendas D1",
            },
            #Tiendas D1 pan tajado
            {
                "name": "Tiendas D1",
                "price": 6900,
                "image": "https://stockimages.tiendasd1.com/stockimages.tiendasd1.com/kobastockimages/IMAGENES/12004942/pan-tajado-brioche-horneaditos-380-g-01.png",
                "description": "cod:047. Pan tajado brioche horneaditos 380g",
                "category": "Supermercados", 
                "subcategory": "Tiendas D1",
            },
            #Tiendas D1 manzana
            {
                "name": "Tiendas D1",
                "price": 10100,
                "image": "https://stockimages.tiendasd1.com/stockimages.tiendasd1.com/kobastockimages/IMAGENES/12006029/manzana-verde-850-g-01.png",
                "description": "cod:055. Manzana verde 850g",
                "category": "tiendas D1",
            },
            #Tiendas D1  manzana
            {
                "name": "Tiendas D1",
                "price": 10990,
                "image": "https://stockimages.tiendasd1.com/stockimages.tiendasd1.com/kobastockimages/IMAGENES/12000109/manzana-royal-gala-1000-grs-01.png",
                "description": "cod:056. Manzana royal gala 1000g",
                "category": "Supermercados", 
                "subcategory": "Tiendas D1",
            },
            #Tiendas D1  papaya
            {
                "name": "Tiendas D1",
                "price": 8200,
                "image": "https://stockimages.tiendasd1.com/stockimages.tiendasd1.com/kobastockimages/IMAGENES/12006187/papaya-unidad-01.png",
                "description": "cod:057. Papaya unidad",
                "category": "Supermercados", 
                "subcategory": "Tiendas D1",
            },
            #Tiendas D1  Banano
            {
                "name": "Tiendas D1",
                "price": 450,
                "image": "https://stockimages.tiendasd1.com/stockimages.tiendasd1.com/kobastockimages/IMAGENES/12005468/banano-unidad-01.png",
                "description": "cod:058. Banano unidad",
                "category": "Supermercados", 
                "subcategory": "Tiendas D1",
            },
            #Tiendas D1  fresas
            {
                "name": "Tiendas D1",
                "price": 5990,
                "image": "https://stockimages.tiendasd1.com/stockimages.tiendasd1.com/kobastockimages/IMAGENES/12002531/fresa-congelada-tree-fruts-500-g-01.png",
                "description": "cod:059 Fresa congelada tree fruts 500g",
                "category": "Supermercados", 
                "subcategory": "Tiendas D1",
            },


            #tiendas d1 champiñon
            {
                "name": "Tiendas D1",
                "price": 7200,
                "image": "https://stockimages.tiendasd1.com/stockimages.tiendasd1.com/kobastockimages/IMAGENES/12006032/champinon-250-gr-01.png",
                "description": "cod:069 Champiñon 1 bandeja 250g",
                "category": "Supermercados", 
                "subcategory": "Tiendas D1",
            },
            #tiendas d1 brocoli
            {
                "name": "Tiendas D1",
                "price": 6990,
                "image": "https://stockimages.tiendasd1.com/stockimages.tiendasd1.com/kobastockimages/IMAGENES/12006464/brocoli-congelado-cooltivo-500g-01.png",
                "description": "cod:070. Brocoli congelado cooltivo 500g",
                "category": "Supermercados", 
                "subcategory": "Tiendas D1",
            },

            #tiendas d1 tomate
            {
                "name": "Tiendas D1",
                "price": 4800,
                "image": "https://stockimages.tiendasd1.com/stockimages.tiendasd1.com/kobastockimages/IMAGENES/12005556/tomate-chonto-x-1000-g-01.png",
                "description": "cod:080. tomate chonto 1000g",
                "category": "Supermercados", 
                "subcategory": "Tiendas D1",
            },
            #tiendas d1 zanahoria
            {
                "name": "Tiendas D1",
                "price": 4300,
                "image": "https://stockimages.tiendasd1.com/stockimages.tiendasd1.com/kobastockimages/IMAGENES/12002258/zanahoria-x-1000-g-01.png",
                "description": "cod:081. Zanahoria 1000g",
                "category": "Supermercados", 
                "subcategory": "Tiendas D1",
            },
            #tiendas d1 pimenton
            {
                "name": "Tiendas D1",
                "price": 1250,
                "image": "https://stockimages.tiendasd1.com/stockimages.tiendasd1.com/kobastockimages/IMAGENES/12005183/pimenton-unidad-01.png",
                "description": "cod:082. Pimenton unidad",
                "category": "tiendas D1",
            },
            #tiendas d1 cebolla cabezona
            {
                "name": "Tiendas D1",
                "price": 3300,
                "image": "https://stockimages.tiendasd1.com/stockimages.tiendasd1.com/kobastockimages/IMAGENES/12005767/cebolla-cabezona-x-1000g-01.png",
                "description": "cod:083. Cebolla cabezona 1000g",
                "category": "Supermercados", 
                "subcategory": "Tiendas D1",
            },
            #tiendas d1 cebolla larga
            {
                "name": "Tiendas D1",
                "price": 3900,
                "image": "https://stockimages.tiendasd1.com/stockimages.tiendasd1.com/kobastockimages/IMAGENES/12003363/cebolla-larga-500-gr-01.png",
                "description": "cod:084. Cebolla larga 500g",
                "category": "Supermercados", 
                "subcategory": "Tiendas D1",
            },
            #tiendas d1 lechuga crespa
            {
                "name": "Tiendas D1",
                "price": 2200,
                "image": "https://stockimages.tiendasd1.com/stockimages.tiendasd1.com/kobastockimages/IMAGENES/12005805/lechuga-verde-crespa-x-180-g-01.png",
                "description": "cod:084. Lechuga verde crespa 180g",
                "category": "Supermercados", 
                "subcategory": "Tiendas D1",
            },
            #tiendas d1 piña
            {
                "name": "Tiendas D1",
                "price": 5990,
                "image": "https://stockimages.tiendasd1.com/stockimages.tiendasd1.com/kobastockimages/IMAGENES/12003720/pinas-golden-unidad-01.png",
                "description": "cod:085. Piña golden unidad",
                "category": "Supermercados", 
                "subcategory": "Tiendas D1",
            },
            #tiendas d1 naranjas
            {
                "name": "Tiendas D1",
                "price": 4500,
                "image": "https://stockimages.tiendasd1.com/stockimages.tiendasd1.com/kobastockimages/IMAGENES/12000182/naranja-x-2000-gr-01.png",
                "description": "cod:086. naranja x 2000 gr",
                "category": "Supermercados", 
                "subcategory": "Tiendas D1",
            },
            #tiendas d1 fazenda
            {
                "name": "Tiendas D1",
                "price": 7950,
                "image": "https://stockimages.tiendasd1.com/stockimages.tiendasd1.com/kobastockimages/IMAGENES/12005983/chicharron-500-g-01.png",
                "description": "cod:D1 Chicarron 500g",
                "category": "Supermercados", 
                "subcategory": "Tiendas D1",
            },




            #Tiendas D1 bicarbonato
            {
                "name": "Tiendas D1",
                "price": 23000,
                "image": "https://i.imgur.com/Xq3Pfit.jpeg",
                "description": "cod:D5 Bicarbonato de sodio 200 grs",
                "category": "Supermercados", 
                "subcategory": "Tiendas D1",
            },
            
            #Tiendas D1 vinagre
            {
                "name": "Tiendas D1",
                "price": 3400,
                "image": "https://i.imgur.com/Iohkn2c.png",
                "description": "cod:D6 Vinagre de Limpieza 1 Litro",
                "category": "Supermercados", 
                "subcategory": "Tiendas D1",
            },
            #Tiendas D1
            {
                "name": "Tiendas D1",
                "price": 4990,
                "image": "https://i.imgur.com/6oH9v21.png",
                "description": "cod:D15 Toalla de Papel Green 3h 80 Hojas",
                "category": "Supermercados", 
                "subcategory": "Tiendas D1",
            },
            #Tiendas D1
            {
                "name": "Tiendas D1",
                "price": 2200,
                "image": "https://i.imgur.com/A1hnmlq.png",
                "description": "cod:D16 Esponja Multiusos 2 und",
                "category": "Supermercados", 
                "subcategory": "Tiendas D1",
            },

            #TIENDAS D1 JABONES
            {
                "name": "Tiendas D1",
                "price": 4990,
                "image": "https://i.imgur.com/B9i9eMg.png",
                "description": "cod:D17 Jabón Líquido Aloe Vera 1000ml",
                "category": "Supermercados", 
                "subcategory": "Tiendas D1",
            },
            #TIENDAS D1 JABONES
            {
                "name": "Tiendas D1",
                "price": 4450,
                "image": "https://i.imgur.com/XRVq0dJ.png",
                "description": "cod:D18 Jabón Liquido King 1000ml",
                "category": "Supermercados", 
                "subcategory": "Tiendas D1",
            },
            #TIENDAS D1 JABONES
            {
                "name": "Tiendas D1",
                "price": 12600,
                "image": "https://i.imgur.com/NK302TQ.png",
                "description": "cod:D19 Jabón Liquido King 3 litros",
                "category": "Supermercados", 
                "subcategory": "Tiendas D1",
            },
            #TIENDAS D1 JABONES
            {
                "name": "Tiendas D1",
                "price": 8990,
                "image": "https://i.imgur.com/wel8N6J.png",
                "description": "cod:D20 Suavisante Floral 3 litros",
                "category": "Supermercados", 
                "subcategory": "Tiendas D1",
            },
            #TIENDAS D1 JABONES
            {
                "name": "Tiendas D1",
                "price": 3850,
                "image": "https://i.imgur.com/cXarf1W.png",
                "description": "cod:20 Quitamanchas Liquido 1 Litro",
                "category": "Supermercados", 
                "subcategory": "Tiendas D1",
            },
            #TIENDAS D1 JABONES
            {
                "name": "Tiendas D1",
                "price": 2900,
                "image": "https://i.imgur.com/Zus88nZ.png",
                "description": "cod:D21. Ropa Color",
                "category": "Supermercados", 
                "subcategory": "Tiendas D1",
            },
            #TIENDAS D1 JABONES
            {
                "name": "Tiendas D1",
                "price": 3500,
                "image": "https://i.imgur.com/uk04WVV.png",
                "description": "cod:D22 Detergente Multiusos 900g",
                "category": "Supermercados", 
                "subcategory": "Tiendas D1",
                    
            },
            #TIENDAS D1 JABONES
            {
                "name": "Tiendas D1",
                "price": 2550,
                "image": "https://i.imgur.com/msG0WSF.png",
                "description": "cod:22 Crema Lavaloza King 500g",
                "category": "Supermercados", 
                "subcategory": "Tiendas D1",
            },
            #TIENDAS D1 JABONES
            {
                "name": "Tiendas D1",
                "price": 2600,
                "image": "https://i.imgur.com/t2ugmq4.jpg",
                "description": "cod:D23 Lavaloza King 500g",
                "category": "Supermercados", 
                "subcategory": "Tiendas D1", 
            },
            #TIENDAS D1 GASEOSAS
            {
                "name": "Tiendas D1",
                "price": 5650,
                "image": "https://i.imgur.com/z3iXdbD.jpeg",
                "description": "cod:D24 Coca-Cola Zero 1750ml",
                "category": "Supermercados", 
                "subcategory": "Tiendas D1",
            },

            #TIENDAS D1 GASEOSAS
            {
                "name": "Tiendas D1",
                "price": 13750,
                "image": "https://i.imgur.com/f7kFe65.jpeg",
                "description": "cod:D40. Coca-Cola Zero 2x2.5L",
                "category": "Supermercados", 
                "subcategory": "Tiendas D1", 
            },
            #TIENDAS D1 GASEOSAS
            {
                "name": "Tiendas D1",
                "price": 14450,
                "image": "https://i.imgur.com/fshZ1Cx.jpeg",
                "description": "cod:D42. Coca-Cola 2x2.5L",
                "category": "Supermercados", 
                "subcategory": "Tiendas D1", 
            },
                
            
            #TIENDAS D1 GASEOSAS
            {
                "name": "Tiendas D1",
                "price": 2990,
                "image": "https://i.imgur.com/0Quuyks.png",
                "description": "cod:D42. Gaseosa Cola Negra 1700ml",
                "category": "Supermercados", 
                "subcategory": "Tiendas D1", 
            },
            #TIENDAS D1 GASEOSAS
            {
                "name": "Tiendas D1",
                "price": 5950,
                "image": "https://i.imgur.com/2SKowfM.jpeg",
                "description": "cod:D43. Pony Malta 2 Litros",
                "category": "Supermercados", 
                "subcategory": "Tiendas D1", 
            },
            #TIENDAS D1 GASEOSAS
            {
                "name": "Tiendas D1",
                "price": 1300,
                "image": "https://i.imgur.com/oJXFpvw.jpeg",
                "description": "cod:D44 Pony Malta 200 ml",
                "category": "Supermercados", 
                "subcategory": "Tiendas D1", 
            },
            #TIENDAS D1 ARENAS PARA GATOS
            {
                "name": "Tiendas D1",
                "price": 14850,
                "image": "https://i.imgur.com/SYwZkz9.jpeg",
                "description": "cod:D60. Arena Para Gatos 4500g",
                "category": "Supermercados", 
                "subcategory": "Tiendas D1", 
            },
            #TIENDAS D1 COMIDAS PARA GATOS
            {
                "name": "Tiendas D1",
                "price": 6250,
                "image": "https://i.imgur.com/Gcoj65q.png",
                "description": "cod:D65. Alimento Para Gatos 1000g",
                "category": "Supermercados", 
                "subcategory": "Tiendas D1", 
            },
            #TIENDAS D1 COMIDAS PARA GATOS
            {
                "name": "Tiendas D1",
                "price": 10950,
                "image": "https://i.imgur.com/HoYUpfp.jpeg",
                "description": "cod:D66. Alimento Para Gatos 1000g",
                "category": "Supermercados", 
                "subcategory": "Tiendas D1", 
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
                "category": "plomeros",
            },
            #PLOMEROS
            {
                "name": "Plomeros",
                "price": 0.00,
                "image": "https://i.imgur.com/LRTnmuS.jpeg",
                "description": "Mantenimiento de Tuberias",
                "category": "plomeros",
            },
            #PLOMEROS

            {
                "name": "Plomeros",
                "price": 0.00,
                "image": "https://i.imgur.com/rWeKPRu.jpeg",
                "description": "Construimos tu Vivienda desde Cero",
                "category": "plomeros",
            }
                
            #Puedes añadir más productos aquí
         
            
        ]

        for product in sample_products:
            products_ref.add(product)

        print("🔁 Productos cargados desde código (modo DEV).")
        return sample_products
    else:
        try:
            docs = products_ref.stream()
            products = [doc.to_dict() | {"id": doc.id} for doc in docs]
            print("✅ Productos cargados desde Firebase.")
            return products
        except Exception as e:
            st.error(f"Error al cargar productos: {str(e)}")
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
    '<div class="main-header"><h1>🛵 Domicilios las 24 horas</h1><p>Bienvenido/a aqui encuentras todo en solo lugar, recibimos todas las tarjetas</p></div>',
    unsafe_allow_html=True
)



# Sidebar con información del usuario y carrito
with st.sidebar:
    st.markdown(f"### 👤 {st.session_state['usuario']['nombre']}")

    if st.button("🚪 Cerrar Sesión"):
        st.session_state.clear()
        st.rerun()

    st.markdown("---")

    

# Contenido principal - Catálogo de productos
st.markdown("## 🛍️ Catálogo de Productosy Servicios")


# Inicializar estados de sesión si no existen
if 'selected_category' not in st.session_state:
    st.session_state.selected_category = 'todos'
if 'selected_subcategory' not in st.session_state:
    st.session_state.selected_subcategory = 'todos'


# --- LÓGICA DE FILTROS CON SUBCATEGORÍAS ---
col1, col2 = st.columns([1, 3])
with col1:
    # Lista de categorías principales
    categories = [
        'Comida Vegetariana',
        'Comidas Rapidas',
        
        
        
        'Supermercados',

        
        
        'El carriel',
        'Qbano',
        
        'magdalena',
        'comida china',
        'cobijas y cortinas',
        'plomeros'
    ]
    
    # Selector de categoría principal
    selected_category = st.selectbox("Categoría", categories, key="category_selector")
    
    # Si la categoría seleccionada es Supermercados, muestra el selector de subcategoría
    if selected_category == "Supermercados":
        subcategories = ['Los Ocobos','Tiendas D1']
        selected_subcategory = st.selectbox("Subcategoría", subcategories, key="subcategory_selector")
    else:
        # Resetea la subcategoría si se elige otra categoría principal
        selected_subcategory = 'Los Ocobos'

    
    if selected_category == "Comidas Rapidas":
        subcategories = ['El Corral','La tribu','Punky Chicarron','Vaquita Costeña']
        selected_subcategory = st.selectbox("Subcategoría", subcategories, key="subcategory_selector")
    else:
        # Resetea la subcategoría si se elige otra categoría principal
        selected_subcategory = 'El corral'
        

# Cargar productos si no están en la sesión
if 'productos' not in st.session_state:
    with st.spinner("🛵 Cargando productos disponibles..."):
        st.session_state['productos'] = get_products()

all_products = st.session_state['productos']
products_to_show = all_products

# Aplicar filtros según la lógica solicitada
if selected_category != 'todos':
    # Filtra por categoría principal
    products_to_show = [p for p in all_products if p.get('category') == selected_category]
    
    # Si la categoría es Supermercados Y se ha seleccionado una subcategoría específica
    if selected_category == "Supermercados" and selected_subcategory != 'todos':
        # Filtra adicionalmente por subcategoría
        products_to_show = [p for p in products_to_show if p.get('subcategory') == selected_subcategory]

# Mostrar productos en grid
if products_to_show:
    cols = st.columns(3)
    for idx, product in enumerate(products_to_show):
        with cols[idx % 3]:
            mensaje = f"Hola, estoy interesado en el producto: {product['name']} {product['description']} con precio ${product.get('price', 0):.2f}. mi dirección es: "
            mensaje_url = urllib.parse.quote(mensaje)

            st.markdown(f"""
                <div class="product-card" style="text-align:center;">
                    <img src="{product['image']}" style="width: 100%; height: 200px; object-fit: cover; border-radius: 10px;">
                    <h3 style="margin: 1rem 0 0.5rem 0; color: #333;">{product.get('name', 'Sin nombre')}</h3>
                    <p style="color: #666; margin-bottom: 1rem;">{product.get('description', '')}</p>
                    <div style="display: flex; justify-content: center; align-items: center; gap: 10px; margin-bottom: 1rem;">
                        <div class="price-tag" style="background-color:#FF5C5C;padding:0.5rem 1rem;border-radius:12px;display:inline-block;">
                            ${product.get('price', 0):.2f}
                        </div>
                        <a href="https://wa.me/573212033979?text={mensaje_url}" target="_blank" style="text-decoration:none;">
                            <button style="background-color:#FF5C5C;padding:0.5rem 1rem;border-radius:12px;display:inline-block;border:none;color:white;cursor:pointer;">
                                Chat
                            </button>
                        </a>
                    </div>
                </div>
            """, unsafe_allow_html=True)

            col4, col5, col6 = st.columns([0.5, 2, 0.5])
            with col5:
                st.markdown(
                    f"""
                    <a href="https://checkout.wompi.co/l/VPOS_s3EEBF" target="_blank">
                        <button style="
                            background: linear-gradient(45deg, #667eea, #764ba2);
                            color: white;
                            border: none;
                            border-radius: 25px;
                            padding: 0.75rem 2rem;
                            font-weight: bold;
                            cursor: pointer;
                            margin-bottom: 1.5rem;
                        ">
                            Pagar el producto
                        </button>
                    </a>
                    """,
                    unsafe_allow_html=True
                )
else:
    st.warning("No se encontraron productos para la selección actual.")

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



