import os
from langchain.chat_models import ChatOpenAI
from langchain import OpenAI, Wikipedia
from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType
from langchain.agents.react.base import DocstoreExplorer
import constants
import random
import react
import biografia


#Switch case con los metodos 
def randomChoice(nomb, corr, direcc, nacimi, telefo, labor, inter, famil):
    methods = [react, biografia]
    return random.choice(methods)

