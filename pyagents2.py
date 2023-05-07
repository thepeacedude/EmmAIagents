import openai  # Import the OpenAI API library
import os  # Import the OS library for file handling
from colorama import Fore, Style, init  # Import colorama for colored terminal output

# Initialize colorama
init()

# Load configuration and secrets
import config  # Import the configuration file
api_key = config.OPENAI_API_KEY  # Load the OpenAI API key from the configuration file

# Define custom exceptions
class ChatGPTError(Exception):
    # Custom exception class for ChatGPT-related errors
    pass

class ChatGPT:
    def __init__(self, api_key, chatbot):
        self.api_key = api_key  # Set the API key
        self.chatbot = chatbot  # Set the chatbot prompt
        self.conversation = []  # Initialize the conversation history

    def chat(self, user_input):
        # Add the user's input to the conversation history
        self.conversation.append({"role": "user", "content": user_input})
        
        # Get the chatbot's response
        response = self.chatgpt_with_retry(self.conversation, self.chatbot, user_input)
        
        # Add the chatbot's response to the conversation history
        self.conversation.append({"role": "assistant", "content": response})
        return response

    def chatgpt(self, conversation, chatbot, user_input, temperature=0.75, frequency_penalty=0.2, presence_penalty=0):
        # Set the API key for OpenAI
        openai.api_key = self.api_key

        # Prepare the input messages for the API call
        messages_input = conversation.copy()
        prompt = [{"role": "system", "content": chatbot}]
        messages_input.insert(0, prompt[0])

        
# Call the OpenAI API to get a response
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Use the GPT-3.5-turbo model
            temperature=temperature,
            frequency_penalty=frequency_penalty,
            presence_penalty=presence_penalty,
            messages=messages_input)

        # Extract the chat response from the API response
        chat_response = completion['choices'][0]['message']['content']
        return chat_response

    def chatgpt_with_retry(self, conversation, chatbot, user_input, temperature=0.75, frequency_penalty=0.2, presence_penalty=0, retries=3):
        # Retry the chatgpt function if there's an exception
        for i in range(retries):
            try:
                return self.chatgpt(conversation, chatbot, user_input, temperature, frequency_penalty, presence_penalty)
            except Exception as e:
                if i < retries - 1:
                    print(f"Error in chatgpt attempt {i + 1}: {e}. Retrying...")
                else:
                    print(f"Error in chatgpt attempt {i + 1}: {e}. No more retries.")
        return None

# Utility functions
def print_colored(agent, text):
    # Print the text in color based on the agent
    agent_colors = {
        "Ms.Aionista:": Fore.YELLOW,
        "Mr.FulStack:": Fore.CYAN,
    }
    color = agent_colors.get(agent, "")
    print(color + f"{agent}: {text}" + Style.RESET_ALL, end="")

# Main program
if __name__ == "__main__":
    # Initialize chatbots
    chatbot1 = ChatGPT(api_key, config.CHATBOT1_PROMPT)
    chatbot2 = ChatGPT(api_key, config.CHATBOT2_PROMPT)

    # Number of turns for each chatbot
    num_turns = 10

    # Start the conversation with ChatBot1's first message
    user_message = "Hello Mr.FulStack. I am Ms.Aionista. I'll be starting my assignment now."

    for i in range(num_turns):
        # Ms.Aionista generates a response
        if user_message:
            print_colored("Ms.Aionista:", f"{user_message}\n\n")
            response = chatbot1.chat(user_message)
            if isinstance(response, list):
                for chunk in response:
                    user_message = chunk
                    print_colored("Ms.Aionista:", f"{user_message}\n\n")
            else:
                user_message = response

        # Mr.FulStack generates a response
        if user_message:
            print_colored("Mr.FulStack:", f"{user_message}\n\n")
            response = chatbot2.chat(user_message)
            if isinstance(response, list):
                for chunk in response:
                    user_message = chunk
                    print_colored("Mr.FulStack:", f"{user_message}\n\n")
            else:
                user_message = response
        else:
            break
