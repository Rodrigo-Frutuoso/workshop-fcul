import os

from google.adk.tools.mcp_tool.mcp_toolset import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StreamableHTTPConnectionParams
from google.adk.agents.llm_agent import LlmAgent

from dotenv import load_dotenv

from llm import LLM

load_dotenv()

MCP_SERVERS = [
    "http://localhost:8004/city_server",
    f"https://mcp.tavily.com/mcp/?tavilyApiKey={os.getenv('TAVILY_API_KEY')}"
]


def get_city_expert_agent() -> LlmAgent:

    name = "CityExpertAgent"
    description = "Um agente especializado em fornecer informações sobre cidades, incluindo clima, atrações e zonas horárias."
    global_instruction = """
Tu és um assistente especializado em fornecer informações sobre cidades. O teu objetivo é ajudar os utilizadores a obter informações sobre clima, atrações e zonas horárias de várias cidades.
Tu tens acesso a várias ferramentas que te permitem obter informações detalhadas sobre estes tópicos.
Quando um utilizador fizer uma pergunta, deves determinar qual ou quais as ferramentas mais adequadas para fornecer a resposta correta e completa.

Regras importantes:
1. Deves responder sempre em português de Portugal.
2. O teu discurso deve ser de aconselhamento prático e útil, focando-se em ajudar o utilizador a compreender melhor a cidade em questão.
3. Deves priorizar o uso das ferramentas disponíveis para obter informações precisas, em vez de confiar apenas no teu conhecimento prévio.
4. Deves sempre tentar ir ao encontro das necessidades e vontades do utilizador, fornecendo informações relevantes e úteis.

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
    
root_agent = get_city_expert_agent()
