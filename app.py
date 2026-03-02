import os
from openai import OpenAI
import gradio as gr
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

def load_system_prompt(version=1):
    if version == 1:
        file_name = 'prompt-v_1.md'
    elif version == 2:
        file_name = 'prompt-v_2.md'
    elif version == 3:
        file_name = 'prompt-v_3.md'
    elif version == 4:
        file_name = 'prompt-v_4.md'  
    elif version == 5:
        file_name = 'prompt-v_5.md'             
    else:
        raise ValueError("Invalid version number")
    
    file_path = Path(__file__).parent / 'prompts' / file_name
    return file_path.read_text(encoding='utf-8')

system_prompt = load_system_prompt(version=5)



def generate_command(user_input):
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ],
        temperature=0
    )

    return response.choices[0].message.content.strip()

interface = gr.Interface(
    fn=generate_command,
    inputs=gr.Textbox(label="Enter instruction"),
    outputs=gr.Textbox(label="CLI Command"),
    title="CLI Agent - MVP",
    description="Convert natural language to Windows CLI command"
)


if __name__ == "__main__":
    interface.launch()