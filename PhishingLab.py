import os
from streamlit_js_eval import streamlit_js_eval
import streamlit as st
#from streamlit_gsheets import GSheetsConnection
import pandas as pd
#import constants

st.set_page_config(layout="wide")

os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
# copies 
home_title = "PhishingLab"
home_introduction = "Hola, esta es una aplicación de generación de correos phishing que te muestra cómo pueden ser los correos fraudulentos que intentan engañarte para obtener tus datos personales, financieros o de acceso. Con esta aplicación, puedes ver ejemplos de correos phishing que simulan ser de entidades legítimas, como bancos, empresas, organismos públicos, etc. **Solo tienes que introducir los datos que creas que filtras con mayor facilidad** y la aplicación te mostrará un correo falso que podrías recibir en tu bandeja de entrada. Esta aplicación utiliza la tecnología GPT de OpenAI para crear correos phishing convincentes. Úsala y aprende a identificar y evitar los correos phishing."
home_privacy = "Tu información personal no es almacenada de ninguna forma, apenas generas un correo todo se elimina, asegurando una completa privacidad y anonimato. Esto significa que puedes usar PhishingLab con tranquilidad, tus datos siempre están seguros."
home_getstarted_1 = "Revise los Términos de uso y Política de privacidad, disponibles en la página de Términos."
home_getstarted_2 = "Comienza a utilizar el sistema, guiado de un tutorial que enseñara como generar y evaluar los correos fraudulentos... ¡Empecemos!"
st.markdown(
    "<style>#MainMenu{visibility:hidden;}</style>",
    unsafe_allow_html=True
)

#st.title(home_title)
st.markdown(f"""# {home_title} <span style=color:#2E9BF5><font size=5>Beta</font></span>""",unsafe_allow_html=True)

st.markdown("""\n""")
st.markdown("#### Saludos")
st.write(home_introduction)
st.divider()
#st.markdown("---")

st.markdown("#### Privacidad")
st.write(home_privacy)
st.write(home_getstarted_1)
st.page_link("pages/2_Términos_y_condiciones.py", label="Términos y condiciones", icon="⚖️")
st.markdown("""\n""")

st.divider()    
st.markdown("""\n""")
st.markdown("#### Generador")
st.write(home_getstarted_2)
st.page_link("pages/1_Generador.py", label="COMENZAR", icon="🤖", use_container_width=False)
st.markdown("""\n""")
st.divider()
#GSheets connection
#conn = st.connection("gsheets", type=GSheetsConnection)
#existing_data = conn.read(worksheet="datos", usecols=list(range(22)),ttl=22)
#existing_data = existing_data.dropna(how="all")

#st.markdown("#### Instrucciones de uso")

        



                