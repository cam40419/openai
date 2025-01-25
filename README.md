# openai

This application is intended to be used as a full ai replacement for any manual work or school assignment.

## Latest Release
Version 1.0:
- Basic chat completion support
- Saving and loading conversations
- Presets for all opanai settings
- Deterministic output
- Forced structured outputs (json)

## Coming Soon
Version 1.1:
- File loading support
- Custom model training

## Setting Up a Python Virtual Environment and Installing Requirements

Follow these steps to create a Python virtual environment and install dependencies from the `requirements.txt` file.

### 1. Create a Virtual Environment

First, navigate to your project directory and create a virtual environment.

On Windows:

`python -m venv venv`

On macOS/Linux:

`python3 -m venv venv`

### 2. Activate the Virtual Environment

On Windows:

`.\venv\Scripts\activate`

On macOS/Linux:

`source venv/bin/activate`

### 3. Install the Required Dependencies

`pip install -r requirements.txt`


## Creating a .env File

Create a file ".env" in the main HIRE directory. Add the paths for the save file, preset file, and response format file. 

You will also need to add your opanai api key.

Here is an example .env file:

```
API_KEY = YOUR_OPENAI_KEY
SAVE_FILE = ..\data\saved_conversations.json
PRESET_FILE = ..\data\presets.ini
RESPONSE_FORMAT_FILE = ..\data\response_formats.json
```

