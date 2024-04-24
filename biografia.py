import os
from langchain.chat_models import ChatOpenAI
from langchain import OpenAI, Wikipedia
from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType
from langchain.agents.react.base import DocstoreExplorer
import constants
import random
#Definir PromptTemplate
from langchain import PromptTemplate
os.environ["OPENAI_API_KEY"] = constants.APIKEY

def phishing_biografia(nomb, corr, direcc, nacimi, telefo, labor, inter, famil):
    #Filtrar datos segun importancia
    nombrep=nomb
    correop=corr
    direccionp=direcc
    nacimientop=nacimi
    telefonop=telefo
    laborp=labor
    interesp=inter
    familp=famil
    prompt_template = PromptTemplate.from_template( """
        Simula una biografia para los siguientes datos:Nombre: {nombre},Correo electrónico: {correo},Dirección domiciliaria: {direccion},Fecha de nacimiento: {nacimiento},Número de teléfono: {telefono},Experiencia laboral: {laboral},Intereses: {interes}, Familia: {familia}                                                                                 
    """
    )
    
    #2-Autoridad 2-Urgencia 2-Deseo 2-Urgencia y Autoridad 2-Urgencia y Deseo 2-Autoridad y Deseo
    llm = OpenAI(model_name="gpt-3.5-turbo-1106",temperature=0.4)
    question = prompt_template.format(nombre=nombrep, correo=correop, direccion=direccionp, nacimiento=nacimientop, telefono=telefonop, laboral=laborp, interes=interesp, familia=familp)

    response1 = llm(question)
    
    traits = ["Autoridad", "Urgencia", "Deseo"]
    selected_trait = random.choice(traits)
    question2 = PromptTemplate.from_template("Simula un posible correo Phishing para la siguiente persona: {response1p}. El correo debe generar {traitp} y solicitar ingresar a un link falso.")
    response2 = question2.format(traitp=selected_trait,response1p=response1)
    response3 = llm(response2)

    template2 = PromptTemplate.from_template("{response2p}. Mejora redaccion y estructura, añadiendo un asunto coherente a lo descrito en el correo. ")
    generador = template2.format(response2p=response3)
    respuesta_final = llm(generador)
    return ([respuesta_final,selected_trait])

  