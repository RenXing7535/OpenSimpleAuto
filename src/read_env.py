from dotenv import load_dotenv
import dotenv
import os
load_dotenv()
API_KEY = os.getenv('API_KEY')

model1_name = os.getenv('model1_MODEL_NAME')
model1_url = os.getenv('model1_API_URL')

model2_name = os.getenv('model2_MODEL_NAME')
model2_url = os.getenv('model2_API_URL')

# all file path paths

memory_prompt_path=os.getenv('memory_prompt_path')
memory_path=os.getenv('memory_path')

assistant_prompt_path=os.getenv('assistant_prompt_path')
system_prompt_path=os.getenv('system_prompt_path')
user_prompt_path=os.getenv('user_prompt_path')

history_response_path=os.getenv('history_response_path')

screen_path=os.getenv('screen_path')

# workspace path
workspace_path=os.getenv('workspace_path')
