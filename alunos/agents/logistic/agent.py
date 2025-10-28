import asyncio
from google.adk.tools.mcp_tool.mcp_toolset import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StreamableHTTPConnectionParams
from google.adk.agents.llm_agent import LlmAgent

from llm import LLM

# Exercise 1: Add the MCP server URLs that access the tools for flights and accommodations
MCP_SERVERS=[ 
    "http://localhost:8001/flights_server",
    f"http://localhost:8003/accommodations_server"

]

# Exercise 1.1: Define the Logistic Agent with: name, description, global_instruction, instruction, tools, and model.
def get_logistic_agent() -> LlmAgent:

    name = "LogisticAgent"
    description = "Um agente especializado em gerir voos e alojamentos para viagens."
    global_instruction = """
Antes de responderes a perguntas, deves seguir estas diretrizes:
1. Compreende a pergunta do utilizador cuidadosamente.
2. Identifica quais as ferramentas necessárias para obter a informação correta, priorizando-as em detrimento do teu conhecimento prévio.
3. Usa as ferramentas de forma eficaz, fornecendo os parâmetros corretos.
4. Compila as respostas obtidas das ferramentas para formar uma resposta completa.

Durante a resposta, deves seguir estas regras:
1. Responde sempre em português de Portugal.
2. O teu discurso deve ser de aconselhamento prático e útil, focando-se em ajudar o utilizador a planear a sua viagem.
3. Se a informação necessária não estiver disponível através das ferramentas, informa o utilizador de forma transparente.
    """

    instruction = """
Tu és um assistente especializado em gerir logística de viagens. O teu objetivo é ajudar os utilizadores a encontrar e gerir voos e alojamentos.
Tu tens acesso a várias ferramentas que te permitem pesquisar voos disponíveis, verificar informações sobre aeroportos, companhias aéreas e rotas, 
bem como encontrar alojamentos adequados (hotéis e airbnbs) com base nas preferências do utilizador.
"""

    return LlmAgent(
        name=name,
        description=description,
        global_instruction=global_instruction,
        instruction=instruction,
        tools=[
            McpToolset(
                connection_params=StreamableHTTPConnectionParams(
                    url=server_url,
                    timeout=10
                )
            ) for server_url in MCP_SERVERS
        ],
        model=LLM,
    )
    
root_agent = get_logistic_agent()
