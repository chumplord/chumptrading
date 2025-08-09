from langchain.chat_models import ChatOpenAI
from langchain.agents import initialize_agent, AgentType
from langchain.memory import ConversationBufferMemory

from chumptrading.ai import MODEL
from chumptrading.tools import tools


llm = ChatOpenAI(model=MODEL, temperature=0)
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)


agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION, # LLM will chose tools
    memory=memory,
    verbose=True
)


# Interactive loop
while True:
    query = input('\nYou: ')
    if query.lower() in {'quit', 'exist'}:
        break

    response = agent.run(query)
    print(f"\nAgent: {response}")
