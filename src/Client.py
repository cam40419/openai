import ast
from openai import OpenAI
import configparser
from dotenv import load_dotenv
import json
import os
import Logger
import time
from random import randint

class chat_completion:
    logger = Logger.Logger()  # Class variable for logging

    client = None  # The OpenAI API connection
    save_name = None
    model = None
    messages = None
    temperature = None
    top_p = None
    frequency_penalty = None
    logit_bias = None
    presence_penalty = None
    seed = None
    preset_name = None
    user = "An all-around helpful AI assistant"
    saved = False
    json = None
    response_type = None
    save_file = ""
    response_format_file = ""

    def __init__(self, preset_name="DEFAULT", save_name=None):
        # Load preset configurations
        self.presets = configparser.ConfigParser()
        preset_file = os.getenv("OPENAI_PRESET_FILE")
        self.presets.read(preset_file)
        self.preset_name = preset_name
        
        # Load environment variables
        load_dotenv()
        api_key = os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=api_key)

        # Load save and response format file paths
        self.save_file = os.getenv("OPENAI_SAVE_FILE")
        self.response_format_file = os.getenv("OPENAI_RESPONSE_FORMAT_FILE")

        # Attempt to load saved conversation
        if save_name is None:
            self.new_conversation()
        else:
            self.load_conversation(save_name)

    def new_conversation(self):
        preset = self.presets[self.preset_name]
        if 'deterministic_output' in preset and preset['deterministic_output']:
            self.seed = randint(1000000000, 9999999999)

        # Load preset values: user, presence_penalty, logit_bias, frequency_penalty, temperature, top_p
        self.load_preset()

        # Initialize the conversation with a system message
        self.messages = [{"role": "system", "content": self.user}]
        self.saved = True
        self.logger.log("Created new conversation")

    def save_conversation(self, save_name=None):
        self.save_name = save_name
        if save_name is None:
            self.logger.error("Unable to save conversation, no save name provided")
            print("Error: No save name provided for conversation.")
        else:
            if not self.saved:
                with open(os.getenv("SAVE_FILE"), "r") as f:
                    saves = json.loads(f.read())

                saves[save_name] = {
                    'messages': self.messages,
                    'preset_name': self.preset_name,
                    'seed': self.seed
                }

                with open(self.save_file, "w") as f:
                    f.write(json.dumps(saves))

                self.saved = True
                self.logger.log(f"Saved conversation: {self.save_name}")
                print(f"Conversation saved as: {self.save_name}")
            else:
                self.logger.log(f"Conversation: {self.save_name} already saved")

    def load_conversation(self, save_name):
        try:
            with open(self.save_file, "r") as f:
                save = json.loads(f.read())[save_name]

            self.save_name = save_name
            self.preset_name = save['preset_name']
            self.load_preset()
            self.messages = save['messages']
            self.seed = save['seed']
            self.saved = True

            self.logger.log(f"Conversation: {self.save_name} loaded")
            print(f"Loaded conversation: {self.save_name}")
        except Exception:
            self.logger.error(f"No saved conversation found: {self.save_name}")
            print(f"No saved conversation found: {self.save_name}")

    def load_preset(self):
        preset = self.presets[self.preset_name]

        if 'model' in preset: 
            self.model = preset['model']
        if 'temperature' in preset: 
            self.temperature = float(preset['temperature'])
        if 'top_p' in preset: 
            self.top_p = float(preset['top_p'])
        if 'frequency_penalty' in preset: 
            self.frequency_penalty = float(preset['frequency_penalty'])
        if 'logit_bias' in preset: 
            self.logit_bias = preset['logit_bias']
        if 'presence_penalty' in preset: 
            self.presence_penalty = float(preset['presence_penalty'])
        if 'user' in preset: 
            self.user = preset['user']
        if 'deterministic_output' in preset: 
            self.deterministic_output = preset['deterministic_output']
        if 'format' in preset:
            self.load_response_format(preset['format'])

        self.logger.log(f"Loaded preset: {self.preset_name} for conversation: {self.save_name}")

    def load_response_format(self, response_format):
        try:
            with open(self.response_format_file, "r") as f:
                format = json.loads(f.read())[response_format]

            self.response_type = format["type"]
            self.user = self.user + " Please respond with the following json format: " + json.dumps(format["format"])
            
            self.logger.log(f"Loaded response format: {response_format} for conversation: {self.save_name}")
        except Exception as e:
            self.logger.error(f"No response format found: {response_format}")
            print(f"No response format found: {response_format}")
            
    def chat(self, query):
        self.logger.log(f"Sending chat request using model: {self.model}")
        query_start = time.time()

        previous = self.messages
        self.messages.append({"role": "user", "content": query})

        response_message = ""

        params = {
            "model": self.model,
            "messages": self.messages,
            "temperature": self.temperature,
            "top_p": self.top_p,
            "frequency_penalty": self.frequency_penalty,
            "logit_bias": self.logit_bias,
            "presence_penalty": self.presence_penalty,
            "seed": self.seed
        }

        if self.response_type is not None:
            params["response_format"] = self.response_type

        try:
            response = self.client.chat.completions.create(**params)
            query_time = time.time() - query_start

            if response.choices[0].finish_reason == "stop":
                response_message = response.choices[0].message.content
                self.messages.append({"role": "assistant", "content": response_message})
                self.saved = False
                self.last_query = query
                self.last_response = response_message
                self.logger.log(f"Received chat response in {query_time:.2f} seconds")
                print(f"Chat response received in {query_time:.2f} seconds")
                
        except Exception as e:
            self.messages = previous
            self.logger.error(f"Error sending request: {str(e)}")
            print(f"Error sending request: {str(e)}")

        self.saved = False
        return response_message

def load_conversation(save_name):
    try:
        # Open the saved conversations file
        with open(os.getenv("SAVE_FILE"), "r") as f:
            saves = json.loads(f.read())

            # Check if the save_name exists in the saved conversations
            if save_name in saves:
                save = saves[save_name]

                # Create a chat_completion instance and set the loaded values
                chat = chat_completion(preset_name=save['preset_name'], save_name=save_name)
                chat.messages = save['messages']
                chat.seed = save['seed']
                chat.saved = True

                return chat
            else:
                print(f"No saved conversation found with name: {save_name}")
                return None
    except Exception as e:
        print(f"Error loading conversation: {str(e)}")
        return None