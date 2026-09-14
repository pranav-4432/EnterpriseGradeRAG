import logfire
from pydantic_ai import Agent

logfire.configure()

agent = Agent(
    "gemini-2.0-flash",
    system_prompt="You are a helpful assistant."
)

result = agent.run_sync("What is RAG? Explain in one sentence.")

print("Pydantic AI response:")
print(result.output)