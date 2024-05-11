import streamlit as st

from src.autogen.service import AutogenAiService


def set_session_vars():
    if "task_chat_output_key" not in st.session_state:
        st.session_state.task_chat_output_key = ""
        st.session_state.task_input_key = ""


def get_code_from_ai(task_msg: str) -> str:
    generated_code = AutogenAiService().generate_code(task_msg=task_msg)
    return generated_code


def gen_button_submit():
    task_input_text = st.session_state.task_input_key
    generated_code = get_code_from_ai(task_msg=task_input_text)
    st.session_state.task_chat_output_key = generated_code


def main_loop():
    set_session_vars()

    st.title('AI Autogen Codility tasks resolver')

    st.text_area('Codility task here', value='', height=300, max_chars=None, key='task_input_key')
    st.button('Generate code', on_click=gen_button_submit)
    st.text_area('AI output', value='', height=300, max_chars=None, key='task_chat_output_key')


if __name__ == '__main__':
    main_loop()
