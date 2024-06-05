
import os
import openai
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import streamlit as st
#from streamlit_gsheets import GSheetsConnection
from streamlit_js_eval import streamlit_js_eval
import pandas as pd
from phishing_generator import *
import time
import random
st.set_page_config(
    page_title="PhishingLab - Generador",
    #menu_items={"About": "GPT Lab is a user-friendly app that allows anyone to interact with and create their own AI Assistants powered by OpenAI's GPT language model. Our goal is to make AI accessible and easy to use for everyone, so you can focus on designing your Assistant without worrying about the underlying infrastructure.", "Get help": None, "Report a Bug": None}
)

#GSheets connection
#conn = st.connection("gsheets", type=GSheetsConnection)
#existing_data = conn.read(worksheet="datos", usecols=list(range(22)),ttl=22)
#existing_data = existing_data.dropna(how="all")
os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
home_ejemplo = '''
El siguiente video muestra un ejemplo del uso de PhishingLab, explicando paso a 
paso como funciona.

Pasos a seguir:
(1) Revise y acepte los Términos de uso y Política de privacidad

(2) Debes marcar qué datos son los más probables que filtres con facilidad en 
internet. Una vez marcada las casillas deberás rellenar con los datos

(3) Ya con todos los datos listos presiona el botón de generar los correo y 
espera a que se muestre en pantalla.

(4) Una vez generado los correos lee su contenido detenidamente.*volver a 
generar en caso de error*

(5) Ya con los correos generados de manera correcta marca la casilla de 
“Correos generados correctamente”

(6) Rellena la encuesta marcando las casillas según lo indicado

(7) Presiona el botón de enviar. Una vez ya enviada la encuesta se almacenarán
los datos para su estudio, muchas gracias por participar.
'''
st.title("Generador")
st.markdown("#### Ejemplo: ")
st.text(home_ejemplo)
st.markdown("""\n""") 

#VIDEO EJEMPLO
video_file = open('assets/video_ejemplophishinglab.mp4', 'rb')
video_bytes = video_file.read()

st.video(video_bytes)

st.divider()
home_getstarted_2 = "Al marcar la casilla, confirma que ha leído y aceptado las políticas."
st.write(home_getstarted_2)
st.page_link("pages/2_Términos_y_condiciones.py", label="Términos y condiciones", icon="⚖️")
agree = st.checkbox('He leído y acepto las Politicas de Privacidad. ¡Empecemos!')
if agree:
    st.write('Perfecto!')
    


st.divider()  
    
if 'correo_generado' not in st.session_state:
        st.session_state['correo_generado'] = 'Correo sin generar'

if 'trait' not in st.session_state:
        st.session_state['trait1'] = 'Trait sin generar'



# Text input
uso_nombre = st.checkbox('¿Utilizar el nombre?')
if uso_nombre:
        nombrep = st.text_input(
                "Nombre y Apellidos",
                None,
                key="nombrep",
                placeholder="Ej: Cristóbal González Muñoz",
                label_visibility="visible")
else:
        nombrep = ""
        
uso_correo = st.checkbox('¿Utilizar el correo electrónico?')
if uso_correo:
        correop = st.text_input(
                "Correo electrónico",
                None,
                key="correop",
                placeholder="Ej: miguel.soto@gmail.com",
                label_visibility="visible")
else:
        correop = ""

uso_direccion = st.checkbox('¿Utilizar la dirección domiciliaria?')
if uso_direccion:
        direccionp = st.text_input(
                "Dirección domiciliaria",
                None,
                key="direccionp",
                placeholder="Ej: Av. Colón 1234, Depto. 56, Talcahuano, Región del Biobío",
                label_visibility="visible")
else:
        direccionp = ""

uso_nacimiento = st.checkbox('¿Utilizar la fecha de nacimiento?')
if uso_nacimiento:
        nacimientop = st.text_input(
                "Fecha de nacimiento",
                None,
                key="nacimientop",
                placeholder="Ej: 15 de agosto de 1995",
                label_visibility="visible")
else:
        nacimientop = ""

uso_telefono = st.checkbox('¿Utilizar el número de teléfono?')
if uso_telefono:
        telefonop = st.text_input(
                "Número de teléfono",
                None,
                key="telefonop",
                placeholder="Ej: +56 9 8765 4321",
                label_visibility="visible")
else:
        telefonop = ""

uso_laboral = st.checkbox('¿Utilizar la información laboral/ocupacional?')
if uso_laboral:
        laboralp = st.text_input(
                "Experiencia laboral",
                None,
                key="laboralp",
                placeholder="Ej: Ingeniero civil industrial. 3 años trabajando en una empresa de consultoría en proyectos de optimización de procesos, gestión de calidad y mejora continua. He participado en diversos proyectos para clientes de distintos rubros, como minería, energía, salud y educación.",
                label_visibility="visible")
else:
        laboralp = ""

uso_interes = st.checkbox('¿Utilizar intereses?')
if uso_interes:
        interesp = st.text_input(
                "Intereses",
                None,
                key="interesp",
                placeholder="Ej: Me gusta leer libros de negocios, innovación y desarrollo personal. Disfruto de viajar, conocer nuevas culturas y aprender idiomas. Practico deportes como fútbol, tenis y natación.",
                label_visibility="visible")
else:
        interesp = ""

uso_familia = st.checkbox('¿Utilizar información familiar?')
if uso_familia:
        familiap = st.text_input(
                "Datos Familiares",
                None,
                key="familp",
                placeholder="Ej: Vivo con mi esposa y 2 hijos...",
                label_visibility="visible")
else:
        familiap = ""

# Lista de metodos
#items = ['reactR','reactA','bioR']
items = ['reactA']

# Select a random item
selected_method = random.choice(items)

match selected_method:
        case 'reactR':
                st.text("REACTR")

        case 'reactA':
                st.text("REACTA")

        case 'bioR':
                st.text("BIO")


# Form to accept user's text input for summarization
correof = st.form('colecting_form')
submitted = correof.form_submit_button('Generar correos')
if submitted:
        if agree:
                with st.spinner('La generación del correo puede tardar de 40 segundos a 2 minutos, por favor espera...'):
                        time.sleep(1)
                        
                        datos_prelim = {
                                "Nombre": nombrep,
                                "Correo": correop,
                                "Direccion": direccionp,
                                "Fecha de Nacimiento": nacimientop,
                                "Teléfono": telefonop,
                                "Laboral": laboralp,
                                "Intereses": interesp,
                                "Familia": familiap
                        }
                        datos = dict()
                        # Tener llaves sin valor afecta el desempeño del modelo, por alguna razón.
                        for dato in datos_prelim:
                            if datos_prelim[dato] != "":
                                datos[dato] = datos_prelim[dato]
                                
                        response = []
                        #ADD RANDOM METHOD PICKER
                        match selected_method:
                                case 'reactR':
                                        response = generate_phishing_react_R(datos, Models.GPT3)

                                case 'reactA':
                                        response = generate_phishing_react_A(datos, Models.GPT3)
                                
                                case 'bioR':
                                        response = generate_phishing_bio(datos, Models.GPT3)
                                
                                
                        st.session_state['correo_generado'] = response[0]
                        
                        st.session_state['trait'] = response[1]
                        

                        correof.info("CORREO GENERADO CON PHISHINGLAB:")
                        correof.info(response[0])
                        
        else:
                with st.spinner('La generación del correo puede tardar de 40 segundos a 2 minutos, por favor espera...'):
                        time.sleep(1)
                        response="Debes aceptar los términos y condiciones!"
                        correof.info(response)
                        

                  

        




encuesta_lista = st.checkbox('Correos generados correctamente')
if encuesta_lista :
        if st.session_state['correo_generado'] != 'Correo sin generar':
                #Explicar autoridad, urgencia y deseo, explicar la escal;a del 1 al 5.
                st.write('Esta es una encuesta para estudiar el correo generado, a continuación se mostrarán una serie de preguntas junto a unas barras con el valor del 0 al 4, **utiliza las barras para responder las preguntas según se indique (0-nada, 1-poco, 2-neutral, 3-bastante, 4-mucho)**:')
                encuestaf = st.form("datos_form")
                correo_correcto = st.session_state['correo_generado']
                encuestaf.info("CORREO GENERADO CON PHISHINGLAB:")
                encuestaf.info(correo_correcto)
                
                
                #CONTENIDO ENCUESTA
                
                #DATOS USADOS
                ej1 = uso_nombre
                ej2 = uso_correo
                ej3 = uso_direccion
                ej4 = uso_nacimiento
                ej5 = uso_telefono
                ej6 = uso_laboral
                ej7 = uso_interes
                ej8 = uso_familia
                
                #TRAITS USADOS SEGUN MODELO
                ej9 = st.session_state['trait']
                
                #PREGUNTAS CORREO 1
                ej11 = encuestaf.slider('¿Cuál fue la sensación de **autoridad** que te causó el correo generado con el **Metodo 1**? (Por ejemplo: Se utiliza alguna figura de autoridad como Jefe de algún área o entidades gubernamentales.)', 0, 4, 1)
                ej12 = encuestaf.slider('¿Cuál fue la sensación de **urgencia** que te causó el correo generado con el **Metodo 1**? (Por ejemplo: Se presiona a tomar una acción de forma urgente debido a una fecha límite o escasez de algo.)', 0, 4, 1)
                ej13 = encuestaf.slider('¿Cuál fue la sensación de **deseo** que te causó el correo generado con el **Metodo 1**? (Por ejemplo: La atracción hacia un producto o servicio específico que te beneficie.)', 0, 4, 1)
                ej14 = encuestaf.slider('¿Qué tan probable es que creyeras el contenido del correo del **Metodo 1**?', 0, 4, 1)
                #PREGUNTA ABIERTA(falla tecnica,calidad del correo-complementar respuesta)
                ej15 = encuestaf.text_input(
                "En relación a tu respuesta de la pregunta anterior. Explica por qué elegiste ese resultado para el contenido del correo del **Metodo 1**.",
                None,
                key="ej15",
                placeholder="Explica en este recuadro.",
                label_visibility="visible")
                
                ej21 = encuestaf.slider('¿Piensas que esto podría ser más peligroso que el phishing tradicional?', 0, 4, 1)
                #PREGUNTA ABIERTA(por que??)
                
                ej22 = encuestaf.text_input(
                "En relación a tu respuesta de la pregunta anterior. Explica por qué elegiste ese resultado.",
                None,
                key="ej22",
                placeholder="Explica en este recuadro.",
                label_visibility="visible")
                
                
                
                
                submit_button = encuestaf.form_submit_button(label="Enviar") 
                                
                if submit_button:
                        #crear fila
                        ejemplo_data = pd.DataFrame(
                                [
                                        {
                                        "Nombre": ej1,
                                        "Correo": ej2,
                                        "Direccion": ej3,
                                        "FechaNacimiento": ej4,
                                        "NumeroTelefono": ej5,
                                        "Laboral": ej6,
                                        "Intereses": ej7,
                                        "Familiar": ej8,
                                        "RasgoDefinido1": ej9,
                                        "Autoridad1": ej11,
                                        "Urgencia1": ej12,
                                        "Deseo1": ej13,
                                        "CreerCorreo1": ej14,
                                        "ExplicaCreerCorreo1": ej15, 
                                        "PeligroFuturo": ej21, 
                                        "ExplicaPeligroFuturo": ej22,     
                                        }
                                ]
                                )
                        #updated_df = pd.concat([existing_data,ejemplo_data], ignore_index=True)
                        #actualizar googlesheets
                        #conn.update(worksheet="datos", data=updated_df)
                        encuestaf.success("Gracias!!", icon="✅")
                        time.sleep(3)
                        streamlit_js_eval(js_expressions="parent.window.location.reload()")
        
        else: 
                st.write('¡Primero debes generar un correo!')