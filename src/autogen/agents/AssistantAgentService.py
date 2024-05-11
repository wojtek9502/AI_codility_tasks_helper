import autogen

from src.autogen.agents.AgentAbstract import AgentAbstract


class AssistantAgentService(AgentAbstract):
    def get_agent(self, model: str) -> autogen.ConversableAgent:
        assistant_agent = autogen.UserProxyAgent(
            name="assistant_agent",
        )
        return assistant_agent
