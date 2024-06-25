#import openai
import ollama
import sys
sys.path.append('C:\\Users\\sheld\\Downloads\\tree-of-thought-puzzle-solver\\common')
from common.enums import ChatbotType
from common.config import Config 

class LLMAgent(object):

    def __init__(self, config) -> None:
        self.config = config
        self.chatbot = self._initialize_chatbot(config.chatbot_type)
    
    def compose_messages(self, roles, msg_content_list) -> object:
        if not (len(roles) == len(msg_content_list)):
            raise "Failed to compose messages"
        msgs = [{"role" : roles[i], "content" : msg_content_list[i]} for i in range(len(roles))]
        return msgs
    
    def get_reply(self, messages, temperature = None, max_tokens = None) -> str:
        return self.chatbot.get_reply(messages, temperature, max_tokens)

    def _initialize_chatbot(self, chatbot_type):
        if chatbot_type == ChatbotType.OpenAI:
            return OpenAIChatbot(self.config.openai_model,self.config.openai_api_key)
        else:
            raise "Not supported for now!"


class ChatbotBase(object):

    def __init__(self) -> None:
        pass

    def get_reply(self, messages, temperature = None, max_tokens = None) -> str:
        return ""
    
    
class OpenAIChatbot(ChatbotBase):

    def __init__(self, openai_model, openai_api_key) -> None:
        super().__init__()
        self.model = openai_model
        #openai.api_key = openai_api_key

    def get_reply(self, messages, temperature = None, max_tokens = None) -> str:
        print("LLM Query:", messages)
        try:
            #response = openai.ChatCompletion.create(
            #    model = self.model,
            #    messages = messages,
            #    temperature = temperature,
            #    max_tokens = max_tokens
            #)

            response = ollama.chat(model='llama3', messages=messages, options={'temperature':temperature,})
            reply=response['message']['content']
            #reply = response.choices[0].message["content"]
            print("LLM Reply:", reply)
            print("")
            return reply
        except:
            reply = "Failed to get LLM reply"
            print(reply)
            return reply
