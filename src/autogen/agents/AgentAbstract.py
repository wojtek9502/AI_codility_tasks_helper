import abc

import autogen


class AgentAbstract(abc.ABC):
    @abc.abstractmethod
    def get_agent(self, model: str) -> autogen.ConversableAgent:
        ...
