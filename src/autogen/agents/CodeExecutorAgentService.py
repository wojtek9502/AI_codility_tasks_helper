import autogen
from autogen.coding import DockerCommandLineCodeExecutor

from src import AI_CODE_DIR_PATH
from src.autogen.agents.AgentAbstract import AgentAbstract


class CodeExecutorAgentService(AgentAbstract):
    def __init__(self):
        self.executor = self._get_executor()

    @staticmethod
    def _get_executor():
        # execute code created by chat inside container. Better security
        executor = DockerCommandLineCodeExecutor(
            image="python:3.12-slim",  # Execute code using the given docker image name.
            timeout=10,  # Timeout for each code execution in seconds.
            work_dir=AI_CODE_DIR_PATH,  # Use the temporary directory to store the code files.
        )
        return executor

    def get_agent(self, model: str) -> autogen.ConversableAgent:
        executor = self.executor
        code_executor_agent = autogen.ConversableAgent(
            "code_executor_agent",
            llm_config=False,  # Turn off LLM for this agent.
            code_execution_config={"executor": executor},  # Use the docker command line code executor.
            human_input_mode="NEVER"
        )
        return code_executor_agent
