from pathlib import Path

from streamlit import config as _config
from streamlit.web.bootstrap import run

from src import STREAMLIT_DIR_PATH

streamlit_file = str(Path(STREAMLIT_DIR_PATH, 'streamlit.py'))
_config.set_option("server.headless", True)
run(streamlit_file, args=[], flag_options=dict(), is_hello=False)
