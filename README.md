# Workshop FCUL - AI Agents with Model Context Protocol (MCP)

Este repositório contém os materiais e exercícios para o workshop de AI Agents utilizando o Model Context Protocol (MCP) da Google ADK.

## 📋 Índice

- [Estrutura do Projeto](#estrutura-do-projeto)
- [Configuração Inicial](#configuração-inicial)
- [Exercícios](#exercícios)
- [Servidores MCP](#servidores-mcp)
- [Como Executar](#como-executar)

## 📁 Estrutura do Projeto

```
alunos/
├── agents/                      # Implementação dos agentes AI
│   ├── llm.py                  # Configuração do modelo de linguagem
│   ├── city_expert/            # Agente especialista em cidades
│   │   ├── __init__.py
│   │   └── agent.py           # Implementação completa (referência)
│   ├── logistic/              # Agente de logística
│   │   ├── __init__.py
│   │   └── agent.py           # 🎯 EXERCÍCIO 1
│   └── travel/                # Agente de viagens (orquestrador)
│       ├── __init__.py
│       └── agent.py           # 🎯 EXERCÍCIO 2
├── servers/                    # Servidores MCP que fornecem ferramentas
│   ├── accommodations/        # Servidor de alojamentos
│   │   ├── accommodations.py
│   │   ├── dataset/
│   │   └── helpers/
│   ├── city/                  # Servidor de informações de cidades
│   │   └── city.py
│   └── flights/               # Servidor de voos
│       ├── flights.py
│       ├── dataset/
│       └── helpers/
├── utils/                      # Utilitários
│   └── loader.py
└── requirements.txt            # Dependências Python
```

## 🚀 Configuração Inicial

### 1. Extrair o ficheiro `.env`

O ficheiro de configuração está protegido por password no arquivo `_.env.zip`.

```bash
# Extrair o ficheiro
unzip _.env.zip

# Renomear para .env
mv _.env .env
```

> **Nota:** A password para descomprimir o ficheiro deve ser solicitada aos instrutores.

### 2. Instalar Dependências

```bash
# Navegar para a pasta alunos
cd alunos

# Criar ambiente virtual (recomendado)
python -m venv .venv
source .venv/bin/activate  # No Windows: .venv\Scripts\activate

# Instalar dependências
pip install -r requirements.txt
```

### 3. Verificar o ficheiro `.env`

O ficheiro `.env` deve conter as seguintes variáveis:

```env
AZURE_OPENAI_API_KEY=your_api_key_here
AZURE_OPENAI_ENDPOINT=your_endpoint_here
AZURE_OPENAI_DEPLOYMENT=your_deployment_name
TAVILY_API_KEY=your_tavily_key_here
```

## 📝 Exercícios

### Exercício 1: Agente de Logística (`agents/logistic/agent.py`)

**Objetivo:** Implementar o agente responsável por gerir voos e alojamentos.

**Tarefas:**

1. **Adicionar os servidores MCP** necessários:
   - Servidor de voos: `http://localhost:8001/flights_server`
   - Servidor de alojamentos: `http://localhost:8003/accommodations_server`

2. **Definir o Logistic Agent** com:
   - `name`: Nome identificativo do agente
   - `description`: Descrição clara das capacidades do agente
   - `global_instruction`: Instruções gerais sobre o comportamento do agente
   - `instruction`: Diretrizes específicas para execução de tarefas
   - `tools`: Ferramentas MCP dos servidores de voos e alojamentos
   - `model`: Modelo de linguagem (usar `LLM`)

**Dica:** Use o `city_expert/agent.py` como referência de estrutura.

### Exercício 2: Agente de Viagens (`agents/travel/agent.py`)

**Objetivo:** Criar o agente orquestrador que coordena os outros agentes.

**Tarefas:**

1. **Definir o Travel Agent** com:
   - `name`: Nome do agente orquestrador
   - `description`: Descrição das responsabilidades de coordenação
   - `global_instruction`: Como deve orquestrar os outros agentes
   - `instruction`: Estratégia de delegação de tarefas
   - `model`: Modelo de linguagem (usar `LLM`)

2. **Adicionar conexões** aos agentes especializados:
   - `city_expert_agent`: Para informações sobre cidades
   - `logistic_agent`: Para voos e alojamentos

**Comportamento esperado:**
- Receber pedidos complexos de viagem
- Delegar subtarefas aos agentes especializados
- Consolidar informações numa resposta coerente

## 🛠️ Servidores MCP

Os servidores MCP fornecem ferramentas especializadas aos agentes:

| Servidor | URL | Funcionalidades |
|----------|-----|-----------------|
| **City** | `http://localhost:8004/city_server` | Informações sobre clima, atrações, fuso horário |
| **Tavily** | `https://mcp.tavily.com/mcp/?tavilyApiKey={KEY}` | Pesquisa web e informações atualizadas |
| **Flights** | `http://localhost:8001/flights_server` | Pesquisa de voos, horários, preços |
| **Accommodations** | `http://localhost:8003/accommodations_server` | Hotéis, Airbnbs, preços, disponibilidade |

### Iniciar os Servidores

```bash
# Terminal 1 - Servidor de Voos
cd alunos/servers/flights
python flights.py

# Terminal 2 - Servidor de Alojamentos
cd alunos/servers/accommodations
python accommodations.py

# Terminal 3 - Servidor de Cidades
cd alunos/servers/city
python city.py
```

## 💻 Como Executar

### Testar os Agentes Individualmente

```python
# Exemplo: Testar o Logistic Agent
from agents.logistic.agent import root_agent

response = await root_agent.run("Encontra voos de Lisboa para Paris amanhã")
print(response)
```

### Testar o Sistema Completo

```python
# Testar o Travel Agent (orquestrador)
from agents.travel.agent import root_agent

query = """
Estou a planear uma viagem a Barcelona para a próxima semana.
Preciso de:
1. Informações sobre o clima
2. Voos desde Lisboa
3. Sugestões de alojamento no centro
4. Principais atrações turísticas
"""

response = await root_agent.run(query)
print(response)
```

## 📚 Recursos Adicionais

- [Google ADK Documentation](https://github.com/google/adk)
- [Model Context Protocol Specification](https://modelcontextprotocol.io/)
- [FastMCP Documentation](https://github.com/jlowin/fastmcp)

## 🤝 Suporte

Para questões ou problemas durante o workshop, contacte os instrutores.

## 📄 Licença

Este material é fornecido exclusivamente para fins educacionais no contexto do Workshop FCUL.
