import asyncio
from typing import List, Dict, Optional
from abc import ABC, abstractmethod
from openai import AsyncOpenAI


class Colors:
    """ANSI color codes"""
    GREEN = "\033[0;32m"
    BLUE = "\033[0;34m"
    GRAY = "\033[0;90m"
    BOLD = "\033[1m"
    END = "\033[0m"


class Message(ABC):
    def __init__(self, content: str):
        self.content = content

    @property
    @abstractmethod
    def role(self) -> str:
        pass

    @property
    @abstractmethod
    def emoji(self) -> str:
        pass

    @property
    @abstractmethod
    def color(self) -> str:
        pass

    def to_dict(self) -> Dict[str, str]:
        return {"role": self.role, "content": self.content}

    def __str__(self) -> str:
        return f"{self.color}{self.emoji}: {self.content}{Colors.END}"


class UserMessage(Message):
    role = "user"
    emoji = "👤"
    color = Colors.GREEN


class AssistantMessage(Message):
    role = "assistant"
    emoji = "🤖"
    color = Colors.BLUE


class SystemMessage(Message):
    role = "system"
    emoji = "🔧"
    color = Colors.GRAY


class ToolMessage(Message):
    def __init__(self, content: str, tool_name: str):
        super().__init__(content)
        self.tool_name = tool_name

    role = "tool"
    emoji = "🛠️"
    color = Colors.BOLD

    def to_dict(self) -> Dict[str, str]:
        return {"role": self.role, "content": self.content, "tool_name": self.tool_name}


class AsyncOpenAILLM:
    def __init__(self, api_key: str, base_url: Optional[str] = None):
        self.client = AsyncOpenAI(api_key=api_key)
        if base_url:
            self.client.base_url = base_url
        self.model = None

    async def initialize(self):
        models = await self.client.models.list()
        self.model = models.data[0]

    async def chat_completion(self, messages: List[Message], stream: bool = True):
        stream = await self.client.chat.completions.create(
            model=self.model.id,
            messages=[message.to_dict() for message in messages],
            stream=stream,
            temperature=0.0
        )
        async for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                yield chunk.choices[0].delta.content

    @staticmethod
    def print_messages(messages: List[Message]):
        for message in messages:
            print(message)


async def main():
    api_key = "YOUR API KEY"
    base_url = "YOUR BASE URL"


    llm = AsyncOpenAILLM(api_key, base_url)
    await llm.initialize()
    system_message = SystemMessage("""You are an expert AI assistant that explains your reasoning step by step. For each step, provide a title and content. Decide if you need another step or are ready to give the final answer. Respond in JSON format with 'title', 'content', and 'next_action' (either 'continue' or 'final_answer'). Use as many reasoning steps as needed, at least 3. Be aware of your limitations as an LLM. In your reasoning:

- Include exploration of alternative answers.
- Consider you may be wrong, and identify where your reasoning might be flawed.
- Fully test all other possibilities.
- Use at least 3 methods to derive the answer.
- When dealing with words, carefully examine each character.
- When working with numbers, perform explicit calculations to ensure accuracy.
- Use best practices.

Example of a valid JSON response:
json
{
    "title": "Identifying Key Information",
    "content": "To begin solving this problem, we need to carefully examine the given information and identify the crucial elements that will guide our solution process. This involves...",
    "next_action": "continue"
}
""")

    async def process_task(task_id, msgs):
        print(f"\nTask {task_id}:")
        AsyncOpenAILLM.print_messages(messages)
        response = ""
        async for content in llm.chat_completion(messages):
            response += content
        print(f"\nTask {task_id} completed.")
        return response

    messages = [
        system_message,
        UserMessage("Which is larger, .9 or .11?"),
    ]
    tasks = [asyncio.create_task(process_task(i, messages)) for i in range(1)]
    results = await asyncio.gather(*tasks)

    print("\nAll tasks completed. Final results:")
    for i, result in enumerate(results, 1):
        print(f"\nTask {i} result:\n{result}")

    messages = [
        system_message,
        UserMessage("How many R's are in strawberry?"),
    ]
    tasks = [asyncio.create_task(process_task(i, messages)) for i in range(1)]
    results = await asyncio.gather(*tasks)

    print("\nAll tasks completed. Final results:")
    for i, result in enumerate(results, 1):
        print(f"\nTask {i} result:\n{result}")
if __name__ == "__main__":
    asyncio.run(main())
