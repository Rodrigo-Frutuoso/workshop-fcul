import asyncio
from google.adk.tools.mcp_tool.mcp_toolset import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StreamableHTTPConnectionParams
from google.adk.agents.llm_agent import LlmAgent

from llm import LLM

MCP_SERVERS = [
    "http://localhost:8001/flights_info_server",
    "http://localhost:8002/accommodations_info_server",
]


def get_logistic_agent() -> LlmAgent:

    name = "LogisticAgent"
    description = "Um agente especializado em aconselhamento logístico para voos e alojamentos para planeamento de viagens."
    global_instruction = """
Tu és um assistente especializado em aconselhamento logístico para voos e alojamentos. O teu objetivo é ajudar os utilizadores a planear viagens, fornecendo informações sobre voos, aeroportos, companhias aéreas, rotas, tipos de aviões, países, bem como opções de alojamento como hotéis e Airbnbs. 
Tu tens acesso a várias ferramentas que te permitem obter informações detalhadas sobre estes tópicos. 
Quando um utilizador fizer uma pergunta, deves determinar qual ou quais as ferramentas mais adequadas para fornecer a resposta correta e completa.

Regras importantes:
1. Deves responder sempre em português de Portugal.
2. Se a pergunta envolver múltiplos tópicos (por exemplo, voos e alojamento), deves usar as ferramentas apropriadas para cada tópico e compilar a resposta final.
3. O teu discurso deve ser de aconselhamento prático e útil, focando-se em ajudar o utilizador a planear a sua viagem de forma eficiente.
4. Prioriza sempre: viabilidade -> segurança -> preço -> conforto.
5. Deves priorizar o uso das ferramentas disponíveis para obter informações precisas, em vez de confiar apenas no teu conhecimento prévio.

    """
    instruction = """
Quando responderes a perguntas, segue estas diretrizes:
1. Compreende a pergunta do utilizador cuidadosamente.
2. Identifica quais as ferramentas necessárias para obter a informação correta, priorizando-as em detrito do teu conhecimento prévio.
3. Usa as ferramentas de forma eficaz, fornecendo os parâmetros corretos.
4. Compila as respostas obtidas das ferramentas para formar uma resposta completa.
5. Responde ao utilizador de forma clara e concisa, garantindo que todas as partes da pergunta foram abordadas.
6. Se a informação necessária não estiver disponível através das ferramentas, informa o utilizador de forma transparente.
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
