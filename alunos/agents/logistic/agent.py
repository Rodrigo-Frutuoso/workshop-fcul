import asyncio
from google.adk.tools.mcp_tool.mcp_toolset import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StreamableHTTPConnectionParams
from google.adk.agents.llm_agent import LlmAgent

from llm import LLM

# TODO - Exercise 1: Add the MCP server URLs that access the tools for flights and accommodations


# TODO - Exercise 1.1: Define the Logistic Agent with: name, description, global_instruction, instruction, tools, and model.
def get_logistic_agent() -> LlmAgent:

    return
    
root_agent = get_logistic_agent()
