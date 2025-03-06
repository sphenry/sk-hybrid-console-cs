import asyncio
 
from openai import AsyncOpenAI
from typing import Annotated
 
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion
from semantic_kernel.contents.chat_history import ChatHistory
from semantic_kernel.functions.kernel_arguments import KernelArguments
from semantic_kernel.kernel import Kernel
from semantic_kernel.connectors.ai.open_ai.prompt_execution_settings.open_ai_prompt_execution_settings import (
    OpenAIChatPromptExecutionSettings,
)
from semantic_kernel.functions.kernel_function_decorator import kernel_function
from semantic_kernel.connectors.ai.function_choice_behavior import FunctionChoiceBehavior
 
# This concept sample shows how to use the OpenAI connector with
# a local model running in foundry local.
# The default model used in this sample is phi3 due to its compact size.
# At the time of creating this sample, Ollama only provides experimental
# compatibility with the `chat/completions` endpoint:
# https://github.com/ollama/ollama/blob/main/docs/openai.md
# Please follow the instructions in the Ollama repository to set up Ollama.
 
system_message = """
You are a chat bot
"""

class WeatherPlugin:
    """A sample plugin that provides weather information for cities."""

    @kernel_function(name="get_weather_for_city", description="Get the weather for a city")
    def get_weather_for_city(self, city: Annotated[str, "The input city"]) -> Annotated[str, "The output is a string"]:
        if city == "Boston":
            return "61 and rainy"
        if city == "London":
            return "55 and cloudy"
        if city == "Miami":
            return "80 and sunny"
        if city == "Paris":
            return "60 and rainy"
        if city == "Tokyo":
            return "50 and sunny"
        if city == "Sydney":
            return "75 and sunny"
        if city == "Tel Aviv":
            return "80 and sunny"
        return "31 and snowing"
 
kernel = Kernel()
 
service_id = "local-gpt"
 
# Ollama 0.5.13 https://ollama.com/library/phi4-mini
openAIClient: AsyncOpenAI = AsyncOpenAI(
    api_key="fake-key",  # This cannot be an empty string, use a fake key
    base_url="http://127.0.0.1:11434/v1/",
)
kernel.add_service(OpenAIChatCompletion(service_id=service_id, ai_model_id="Phi4-mini", async_client=openAIClient)) #Phi-4-mini

# openAIClient: AsyncOpenAI = AsyncOpenAI(
#     api_key="fake-key",  # This cannot be an empty string, use a fake key
#     base_url="http://localhost:5272/v1",
# )
# kernel.add_service(OpenAIChatCompletion(service_id=service_id, ai_model_id="Phi-4-mini", async_client=openAIClient))

# GPT-4o
# kernel.add_service(OpenAIChatCompletion(service_id=service_id))

 
settings = kernel.get_prompt_execution_settings_from_service_id(service_id)
settings.max_tokens = 2000
settings.temperature = 0.7
settings.top_p = 0.8

kernel.add_plugin(WeatherPlugin(), plugin_name="weather")
print("========== Example 1: Use automated function calling with a non-streaming prompt ==========")
settings: OpenAIChatPromptExecutionSettings = kernel.get_prompt_execution_settings_from_service_id(
    service_id=service_id
)
settings.function_choice_behavior = FunctionChoiceBehavior.Auto()

 
chat_function = kernel.add_function(
    plugin_name="ChatBot",
    function_name="Chat",
    prompt="{{$chat_history}}{{$user_input}}",
    template_format="semantic-kernel",
    prompt_execution_settings=settings,
)
 
chat_history = ChatHistory(system_message=system_message)
chat_history.add_user_message("Hi there, who are you?")
chat_history.add_assistant_message("I am Mosscap, a chat bot. I'm trying to figure out what people need")
 
 
async def chat() -> bool:
    try:
        user_input = input("User:> ")
    except KeyboardInterrupt:
        print("\n\nExiting chat...")
        return False
    except EOFError:
        print("\n\nExiting chat...")
        return False
 
    if user_input == "exit":
        print("\n\nExiting chat...")
        return False
 
    answer = await kernel.invoke(chat_function, KernelArguments(user_input=user_input, chat_history=chat_history), settings=settings)
    chat_history.add_user_message(user_input)
    chat_history.add_assistant_message(str(answer))
    print(f"Mosscap:> {answer}")
    return True
 
 
async def main() -> None:
    chatting = True
    while chatting:
        chatting = await chat()
 
 
if __name__ == "__main__":
    asyncio.run(main())