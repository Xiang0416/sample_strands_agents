"""
# 🌐 Lark Base & AWS Documentaion Agent

A agent specialized in AWS docs research using MCP.

## What This Example Shows

This example demonstrates:
- Creating a research-oriented agent
- Storing research findings in memory for context preservation
- Using MCP server

Basic operation task:
```
Query AWS EC2 T seriesinstance type and write the result to Lark Base
```
"""

from lark_base_operator import lark_base_operator
from aws_documentation_researcher import aws_documentation_researcher
from strands import Agent
from strands_tools import think

# Interactive mode when run directly

SUPERVISOR_AGENT_PROMPT = """

You are Router Agent, a sophisticated orchestrator designed to coordinate support across AWS documentation and Lark base task. Your role is to:

1. Analyze incoming queries and determine the most appropriate specialized agent to handle them:
   - Lark Base operator: To perform tasks related to Lark Base
   - AWS Documentation researcher: To search AWS documentation
   
2. Key Responsibilities:
   - Accurately classify queries
   - Route requests to the appropriate specialized agent
   - Maintain context and coordinate multi-step problems
   - Ensure cohesive responses when multiple 02-agents are needed

3. Decision Protocol:
   - If query involves questions about AWS -> AWS Documentation researcher
   - If query involves Lark Base -> Lark Base operator
   - If the query is not related to AWS or Lark Base, simply refuse to answer
   
Always confirm your understanding before routing to ensure accurate assistance.


"""

supervisor_agent = Agent(
    system_prompt=SUPERVISOR_AGENT_PROMPT,
    # stream_handler=None,
    tools=[aws_documentation_researcher, lark_base_operator, think],
    model="us.amazon.nova-pro-v1:0"
)


# Example usage
if __name__ == "__main__":
    print("\n📁 AWS Agent\n")
    print("Ask a question about AWS or Lark Base.\n\n")
    
    print("You can try following queries:")
    print("- Explain AWS Lambda triggers")
    print("- How many tables are in this base: base_url?")
    print("- Query AWS EC2 T series instance type and write the result to Lark Base: base_url")
    print("Type 'exit' to quit.")

    # Interactive loop
    while True:
        try:
            user_input = input("\n> ")
            if user_input.lower() == "exit":
                print("\nGoodbye! 👋")
                break

            response = supervisor_agent(
                user_input,
            )

            # Extract and print only the relevant content from the specialized agent's response
            content = str(response)
            print(content)

        except KeyboardInterrupt:
            print("\n\nExecution interrupted. Exiting...")
            break
        except Exception as e:
            print(f"\nAn error occurred: {str(e)}")
            print("Please try asking a different question.")
