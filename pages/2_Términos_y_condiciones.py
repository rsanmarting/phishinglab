import streamlit as st 

st.set_page_config(
    page_title="PhishingLab - Términos",
    #menu_items={"About": "GPT Lab is a user-friendly app that allows anyone to interact with and create their own AI Assistants powered by OpenAI's GPT language model. Our goal is to make AI accessible and easy to use for everyone, so you can focus on designing your Assistant without worrying about the underlying infrastructure.", "Get help": None, "Report a Bug": None}
)

st.markdown(
    "<style>#MainMenu{visibility:hidden;}</style>",
    unsafe_allow_html=True
)
  

st.title("Términos")
st.write("Actualizado: 10-01-2024")
st.header("Términos de uso")

st.info("""
PhishingLab es una plataforma orientada a analizar el impacto de ChatGPT en la generación de phishing. Al acceder a estos servicios, usted acepta cumplir con los siguientes términos de servicio. Lea atentamente estas condiciones y el acuerdo de licencia. Si no acepta estas condiciones o el acuerdo de licencia, no debe utilizar nuestros servicios.
""")

st.markdown("""
##### 1. Uso de nuestros servicios  \n 
PhishingLab proporciona una plataforma para evaluar contenido creado con Asistentes de IA impulsados por el modelo de lenguaje GPT de OpenAI. Estos términos se aplican específicamente al uso de la versión alojada de esta plataforma. Al utilizar los servicios, usted se compromete a utilizarlos únicamente con fines lícitos y de un modo que no infrinja los derechos de terceros.

##### 2. Política de uso de OpenAI\n
OpenAI quiere que todo el mundo utilice sus herramientas de forma segura y responsable. Por eso OpenAI ha creado políticas de uso que se aplican a todos los usuarios de sus modelos, herramientas y servicios. Siguiendo estas políticas, los usuarios se asegurarán de que la tecnología de OpenAI se utiliza de manera correcta. Si OpenAI determina que el producto o uso de un usuario no sigue estas políticas, puede pedir al usuario que realice los cambios necesarios.

Las políticas de OpenAI pueden cambiar a medida que aprendan más sobre el uso y abuso de sus modelos. Para obtener más información sobre la política de uso de OpenAI, visite https://platform.openai.com/docs/usage-policies.

##### 3. Política de privacidad  \n
En PhishingLab es de suma importancia la privacidad. La aplicación sólo utiliza su información durante las sesiones para interactuar con los modelos de IA. Para garantizar su confidencialidad y seguridad, los datos no son almacenados de ninguna forma ni tampoco el correo generado, solo será almacenada la información proporcionada en la encuesta final y los tipos de datos que se usan.

##### 4. Conducta del Usuario  \n
Usted se compromete a utilizar PhishingLab sólo para fines de estudio y de conformidad con estas Condiciones del servicio. En concreto, se compromete a no: (a) compartir correos generados; (b) utilizar información de terceros. También se compromete a utilizar PhishingLab de forma responsable. Esto también incluye crear y utilizar el contenido de forma responsable y ética.

##### 5. Uso de correos creados en la página  \n
PhishingLab proporciona una plataforma para crear y evaluar la peligrosidad de correos tipo Phishing impulsados por el modelo de lenguaje GPT de OpenAI. Cualquier correo proporcionado por la página debe tratarse únicamente con fines de estudio. No seremos responsables de las decisiones que tomen los usuarios.

""")

st.markdown("  \n  \n  \n  \n")

st.header("Política de privacidad")

st.markdown("""
PhishingLab resguarda su privacidad. A continuación le explicamos cómo tratamos sus datos:

##### 1. Datos personales \n
Cuando entre en la página de PhishingLab, le pediremos que introduzca sus datos personales para rellenar los formularios de generación de correos. Nuestra aplicación utiliza sus datos durante las sesiones para interactuar con los modelos de IA y generar correos que traten de usar estos datos para simular posibles correos de spam/phishing, así las personas podrán evaluar la credibilidad de estos correos y que tan peligrosos podrían llegar a ser. No almacenamos sus datos de ninguna forma, una vez se procesan los datos no se ocupan para nada más y se eliminan, solo se almacenarán los resultados de las encuestas y los tipos de datos que son más usados.

##### 2. Políticas de privacidad por parte de OpenAI   \n
https://openai.com/policies/privacy-policy

Al utilizar PhishingLab, usted acepta esta Política de Privacidad.
""")
st.divider()
st.page_link("PhishingLab.py", label="Inicio PhishingLab", icon="🏠")
st.page_link("pages/1_Generador.py", label="Generador PhishingLab", icon="🤖")