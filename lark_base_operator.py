import os
from mcp import StdioServerParameters, stdio_client
from strands import Agent, tool
from strands.tools.mcp import MCPClient


@tool
def lark_base_operator(query: str) -> str:
    """
    Process and respond Lark related task.

    Args:
        query: The user's task

    Returns:
        A helpful response addressing user task
    """

    formatted_query = f"Analyze and respond to this task: {query}"
    response = str()

    try:
        # Load configuration from config.properties
        config_path = os.path.join(os.path.dirname(__file__), 'config.properties')
        config = {}
        with open(config_path, 'r') as f:
            for line in f:
                key, value = line.strip().split('=', 1)
                config[key] = value
        
        lark_base_mcp_server = MCPClient(
            lambda: stdio_client(
                StdioServerParameters(
                    command="npx", args=["-y",
                                        "@larksuiteoapi/lark-mcp",
                                        "mcp",
                                        "-a",
                                        config["lark_app_id"],
                                        "-s",
                                        config["lark_app_secret"],
                                        "-d",
                                        "https://open.larksuite.com",
                                        "--token-mode",
                                        "tenant_access_token"
                                        ]
                )
            )
        )

        with lark_base_mcp_server:

            tools = lark_base_mcp_server.list_tools_sync()
            # Create the research agent with specific capabilities
            research_agent = Agent(
                system_prompt="""You are a Lark Base task processing agent. Your job is to understand and respond to user tasks effectively.
                """,
                tools=tools,
                model="us.amazon.nova-pro-v1:0"
            )
            response = str(research_agent(formatted_query))
            print("\n\n")

        if len(response) > 0:
            return response

        return "I apologize, but I couldn't properly analyze your task. Could you please rephrase or provide more context?"

    # Return specific error message for English queries
    except Exception as e:
        return f"Error processing your task: {str(e)}"


if __name__ == "__main__":
    lark_base_operator("how many tables in this base: https://fsgob25o8zi9.sg.larksuite.com/base/YlEmbyfj0aeQ5zsMeUIluVXEguf?table=tblC2rRPWwOte5It&view=vewryUwH6m")
    # lark_base_operator("Create a base with name 'test from strands agent'")