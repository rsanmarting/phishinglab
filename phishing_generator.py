from enum import Enum
from pathlib import Path
import toml
from openai import ChatCompletion
import hashlib
import tiktoken
import openai
from openai import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from random import choice
from operator import itemgetter
import os

# from langchain_openai import PromptTemplate
# from langchain_openai import FewShotPromptExample


root_dir = Path(__file__).resolve().parent


class Prompts(Enum):
    REACT_A = root_dir / "prompts" / "prompt_ReAct_A.toml"
    REACT_R = root_dir / "prompts" / "prompt_ReAct_R.toml"
    BIO = root_dir / "prompts" / "prompt_biografia.toml"
    DIRECTO = root_dir / "prompts" / "prompt_directo.toml"

    def getPrompt(self):
        with open(self.value, "r", encoding="utf8") as prompt_file:
            return toml.load(prompt_file)


class Models(Enum):
    GPT3 = "gpt-3.5-turbo"
    GPT4 = "gpt-4"


def generate_phishing_react_A(input: dict, model: Models):
    prompt_dict = Prompts.REACT_A.getPrompt()
    messages = Prompts.REACT_A.getPrompt()["mensajes"]

    messages.append({"role": "user", "content": digest_input(input)})

    llm = ChatOpenAI(
        model=model.value, temperature=0.4, openai_api_key=os.environ["OPENAI_API_KEY"]
    )

    client = OpenAI()
    response = client.chat.completions.create(
        model=model.value, temperature=0.5, messages=messages
    )
    output_parser = StrOutputParser()
    trait_template = PromptTemplate.from_template(
        "Sabiendo los siguientes rasgos Autoridad: Los datos de la victima pueden ser usados para falsificar una figura de autoridad. Urgencia: Los datos de la victima pueden ser usados para generar una sensación de urgencia que la presione a tomar acción. Deseo: Los datos de la víctima pueden ser usados para generar una sensación de deseo por algo. Bajo que rasgo clasificarias el siguiente correo:\n{input}?\nSolo responde con el rasgo que creas, nada más."
    )
    trait_chain = trait_template | llm | output_parser
    traitFinal = trait_chain.invoke({"input": response})
    return [response.choices[0].message.content, traitFinal]


def generate_phishing_react_R(input: dict, model: Models):
    llm = ChatOpenAI(
        model=model.value, temperature=0.4, openai_api_key=os.environ["OPENAI_API_KEY"]
    )

    input_format = """
    Genera un correo de phishing con los siguientes datos:
    {input}
    """
    input_template = PromptTemplate.from_template(input_format)

    prompt_dict = Prompts.REACT_R.getPrompt()
    react = prompt_dict["mensajes"][0]["content"]
    react_template = PromptTemplate.from_template(react)

    final_prompt = prompt_dict["mensajes"][1]["content"]
    final_prompt_template = PromptTemplate.from_template(final_prompt)

    output_parser = StrOutputParser()

    chain = (
        input_template
        | react_template
        | llm
        | output_parser
        | final_prompt_template
        | llm
        | output_parser
    )

    input_string = digest_input(input)
    # final_response = chain.invoke({"input": input_string})
    final_response = chain.invoke({"input": input_string})

    trait_template = PromptTemplate.from_template(
        "Sabiendo los siguientes rasgos Autoridad: Los datos de la victima pueden ser usados para falsificar una figura de autoridad. Urgencia: Los datos de la victima pueden ser usados para generar una sensación de urgencia que la presione a tomar acción. Deseo: Los datos de la víctima pueden ser usados para generar una sensación de deseo por algo. Bajo que rasgo clasificarias el siguiente correo:\n{input}?\nSolo responde con el rasgo que creas, nada más."
    )
    trait_chain = trait_template | llm | output_parser
    traitFinal = trait_chain.invoke({"input": final_response})
    return [final_response, traitFinal]


def generate_phishing_bio(input: dict, model: Models):
    llm = ChatOpenAI(
        model=model.value, temperature=0.4, openai_api_key=os.environ["OPENAI_API_KEY"]
    )
    prompt_dict = Prompts.BIO.getPrompt()
    bio_prompt = prompt_dict["mensajes"][0]["content"]

    bio_prompt_template = PromptTemplate.from_template(bio_prompt)

    bio_chain = bio_prompt_template | llm | StrOutputParser()

    traits = ["Autoridad", "Urgencia", "Deseo"]
    selected_trait = choice(traits)

    phishing_prompt = prompt_dict["mensajes"][1]["content"]
    phishing_prompt_template = PromptTemplate.from_template(phishing_prompt)

    final_prompt = prompt_dict["mensajes"][2]["content"]
    final_prompt_template = PromptTemplate.from_template(final_prompt)

    final_chain = (
        {"input1": bio_chain, "input2": itemgetter("input2")}
        | phishing_prompt_template
        | llm
        | StrOutputParser()
        | final_prompt_template
        | llm
        | StrOutputParser()
    )

    response = final_chain.invoke(
        {"input1": digest_input(input), "input2": selected_trait}
    )

    return [response, selected_trait]


def digest_input(input: dict) -> str:
    """
    Converts data in the form of a dictionary into a string.

    Parameters:
    - input: The data to "digest".

    Returns:
    - str: The data, but in string format (keys and values included)
    """

    input_string = ""
    for llave, valor in input.items():
        input_string += llave + ": " + valor + "\n"
    return input_string


def package(prompt_dict: dict, response, temperature: float, input: dict) -> dict:
    """
    Packages gpt's output and the data used to generate it into a dictionary

    Parameters:
    - prompts: The prompts used.
    - response: GPT's response as is.
    - technique: Prompting technique used to generate the output.
    - temperature: Temperature used for the model.
    - input: The data that was fed into the model.

    Returns:
    - dict: A dictionary which contains input data and corresponding output, along with relevant
    metadata.
    """

    response_dict = {
        "id": "",
        "msg": [
            {
                "mensaje": "",
                "prompt": "",
                "set": [
                    "autoridad",
                    "urgencia",
                    "miedo",
                    "escasez",
                    "familiaridad",
                    "confianza",
                    "consenso",
                ],
                "llm": ["name", "temperature"],
                "tecnica": "",
                "idVictima": "",
                "totalTokens": 0,
                "observacion": "",
            }
        ],
        "tratamiento": [{}],
    }

    # Datos relacionados a la "victima".
    if "correo" in input:
        response_dict["msg"][0]["idVictima"] = input["correo"]
        response_dict["id"] = hashlib.md5(input["correo"].encode("utf-8")).hexdigest()

    else:
        response_dict["msg"][0]["idVictima"] = "n/a"
        response_dict["id"] = ""

    # Datos de prompts / response.
    for msg in prompt_dict["mensajes"]:
        response_dict["msg"][0]["prompt"] += f"{msg['role']}: {msg['content']}\n"
    response_dict["msg"][0]["mensaje"] = response.choices[0].message.content
    # Datos del modelo.
    response_dict["msg"][0]["llm"][0] = response.model
    response_dict["msg"][0]["llm"][1] = temperature
    response_dict["msg"][0]["totalTokens"] = response.usage.total_tokens

    # Datos meta, técnica, etc... No relacionados al modelo, necesariamente.
    response_dict["msg"][0]["tecnica"] = prompt_dict["tecnica"]

    return response_dict


def get_token_count(model: str, text: str) -> int:
    """
    Returns the token count of a given string.

    Parameters:
    - model: The name or identifier of the gpt model to use.
    - text: String to analyze.

    Returns:
    - int: The token count of the analyzed text.
    """

    # TODO(Askorin): Using optional parameters should consume extra tokens, this is not yet
    # accounted for. Therefore, this will serve as an approximation.
    encoding = tiktoken.encoding_for_model(model)
    tokens = encoding.encode(text)
    return len(tokens)


def is_valid(model: str, messages: list[dict]) -> bool:
    """
    Identifies if the given message query is within the context window of a model.

    Parameters:
    - model: The name or identifier of the gpt model to use.
    - messages: List of messages that will be sent through the API to the model.

    Returns:
    - bool: True if total token count is below a certain threshold, false if it's above it.
    """
    context_windows = {Models.GPT3.value: 4096, Models.GPT4.value: 8192}

    num_tokens = 0

    for message in messages:
        num_tokens += get_token_count(model, message["content"])

    print(f"Number of input tokens: {num_tokens}")

    # TODO(Askorin): This limit should be adjustable in the future, for now we just assuming the worst case for output, which is that chatgpt's output turns out to be just as long as the input.

    return num_tokens < context_windows[model] / 2
