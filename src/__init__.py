from pathlib import Path

import dotenv

dotenv.load_dotenv()

PROJECT_PATH = Path(__file__).parent.parent

AI_CODE_DIR_PATH = Path(PROJECT_PATH, 'temp')
AI_CODE_DIR_PATH.mkdir(exist_ok=True)
