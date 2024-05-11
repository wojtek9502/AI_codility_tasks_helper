import os

import autogen

from src import USE_DOCKER_CODE_EXECUTOR
from src.autogen.agents.AssistantAgentService import AssistantAgentService
from src.autogen.agents.CodeExecutorAgentService import CodeExecutorAgentService
from src.autogen.agents.CodeWriterAgentService import CodeWriterAgentService


class AutogenAiService:
    def __init__(self, model: str = None):
        if not model:
            model = os.environ['OPENAI_MODEL']

        code_executor_agent_service = CodeExecutorAgentService()
        self._code_executor = code_executor_agent_service.executor
        self._agents_map = {
            'assistant_agent': AssistantAgentService().get_agent(model=model),
            'code_writer_agent': CodeWriterAgentService().get_agent(model=model),
            'code_executor_agent': code_executor_agent_service.get_agent(model=model)
        }
        self.ai_model_name = model

    def stop_executor(self):
        if USE_DOCKER_CODE_EXECUTOR:
            self._code_executor.stop()

    def _get_custom_chats_state_transition(self, last_speaker, chats_group):
        messages = chats_group.messages
        assistant_agent = self._agents_map['assistant_agent']
        code_writer_agent = self._agents_map['code_writer_agent']
        code_executor_agent = self._agents_map['code_executor_agent']

        # Flow:
        # 1) assistant -> code writer
        # 2) code writer -> code executor
        # 3) run code and check code execution results
        #    if ends with exitcode: 1
        #      code executor -> code writer
        #      check code execution results [start 3) again]
        #    else:
        #      stop executor
        #      flow ends

        if last_speaker is assistant_agent:
            return code_writer_agent
        elif last_speaker is code_writer_agent:
            return code_executor_agent
        elif last_speaker is code_executor_agent:
            if messages[-1]["content"] == "exitcode: 1":
                return code_writer_agent
            else:
                self.stop_executor()
                return None

    def _create_chat_group(self, model: str, max_chat_rounds: int = 5) -> autogen.GroupChatManager:
        config_list = [
            {
                "model": model,
                "api_key": os.environ["OPENAI_API_KEY"],
            }
        ]
        gpt_config = {
            "temperature": 0,
            "config_list": config_list,
            "timeout": 120,
        }

        chats_group = autogen.GroupChat(
            agents=list(self._agents_map.values()),
            messages=[],
            max_round=max_chat_rounds,
            speaker_selection_method=self._get_custom_chats_state_transition,
        )
        group_manager = autogen.GroupChatManager(groupchat=chats_group, llm_config=gpt_config)
        return group_manager

    def generate_code(self, task_msg: str):
        assistant_agent = self._agents_map['assistant_agent']
        group_manager = self._create_chat_group(model=self.ai_model_name)

        ai_response = assistant_agent.initiate_chat(
            group_manager, message=task_msg
        )
        generated_code = ai_response.chat_history[-2]['content']  # last response is from code executor
        return generated_code
