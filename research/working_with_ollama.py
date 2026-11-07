from ollama import chat 
from ollama import ChatResponse

import logging
from rich.logging import RichHandler
logging.basicConfig(
    level=logging.DEBUG,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)],
)

logger = logging.getLogger(__name__)
# response:ChatResponse = chat(
#     model="qwen2.5:0.5b",
#     messages=[
#         {
#             'role': 'user', 
#             'content': 'Why is the sky blue'
#         }, 
#     ]
# )
# logger.debug(response['message']['content'])


# stream  = chat(
#     model="qwen2.5:0.5b",
#     messages=[
#         {
#             'role': 'user', 
#             'content': 'Why is the sky blue'
#         }, 
#     ]
# )


# content = ''
# thinking = ''
# in_thinking = False

# for chunk in stream:
#     logger.debug("chunk: %s", chunk)
#     if chunk.message.thinking:
#         if not in_thinking:
#             print("Thinking:\n", end='', flush=True)
#         print(chunk.message.thinking, end='', flush=True)

#         thinking += chunk.message.thinking
#     elif chunk.message.content:
#         if in_thinking:
#             in_thinking = False
#             print("\n\nAnswer:\n", end='', flush=True)

#         print(chunk.message.content, end='', flush=True)

#         content += chunk.message.content

#     # append the accumulated fields to the messages for the next request
#     new_messages = [{ role: 'assistant', thinking: thinking, content: content }]


stream = chat(
    model='qwen2.5:0.5b',
    messages=[{'role': 'user', 'content': 'How do you write Monday in Chinese'}],
    stream=True,
)

in_thinking = False
content = ''
thinking = ''
for chunk in stream:
    if chunk.message.thinking:
        if not in_thinking:
            in_thinking = True
            print('Thinking:\n', end='', flush=True)

        print(chunk.message.thinking, end='', flush=True)
        # accumulate the partial thinking 
        thinking += chunk.message.thinking

    elif chunk.message.content:
        if in_thinking:
            in_thinking = False
            print('\n\nAnswer:\n', end='', flush=True)

        print(chunk.message.content, end='', flush=True)
        # accumulate the partial content
        content += chunk.message.content

  # append the accumulated fields to the messages for the next request
new_messages = [{ 'role': 'assistant', thinking: thinking, content: content }]

logger.debug("new_messages: %s", new_messages)