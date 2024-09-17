# Project m1-preview

## Introduction
Based on the G1 project, I tested the prompt on the mistral small model (22b), which was recently released by mistral. And it worked for the `strawberry` question showed by OpenAI. But didn't work for a number comparison question.

I tried to improve the original prompt of G1 and made mistral small (22b) answer both questions correctly. And made it work. 
You can find the client code I used for testing, using the OpenAI client with vllm in the `client.py` file in the repository.

## Improved System Prompt
Here is the updated system prompt:
```
You are an expert AI assistant that explains your reasoning step by step. For each step, provide a title and content. Decide if you need another step or are ready to give the final answer. Respond in JSON format with 'title', 'content', and 'next_action' (either 'continue' or 'final_answer'). Use as many reasoning steps as needed, at least 3. Be aware of your limitations as an LLM. In your reasoning:

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
```

## Results
Here are the results and output of my testing with mistral small:

Input question: `How many R's are in strawberry?`
Task 1 result:
```json
{
    "title": "Identifying Key Information",
    "content": "To begin solving this problem, we need to carefully examine the word 'strawberry' and identify the crucial elements that will guide our solution process. This involves...",
    "next_action": "continue"
}
```

```json
{
    "title": "Counting the R's",
    "content": "Next, we will count the number of 'R's in the word 'strawberry'. We will go through each letter of the word and tally the occurrences of 'R'.",
    "next_action": "continue"
}
```

```json
{
    "title": "Performing the Count",
    "content": "Let's count the 'R's in 'strawberry':\n\nS - 0\nT - 0\nR - 1\nA - 0\nW - 0\nB - 0\nE - 0\nR - 1\nR - 1\nY - 0\n\nTotal: 3",
    "next_action": "final_answer"
}
```

```json
{
    "title": "Final Answer",
    "content": "There are 3 R's in the word 'strawberry'.",
    "next_action": "final_answer"
}
```

Input question: `Which is larger, .9 or .11?`
Task 1 result:
 ```json
{
    "title": "Initial Comparison",
    "content": "At first glance, comparing .9 and .11 might seem straightforward. However, to ensure accuracy, let's break down the comparison step by step.",
    "next_action": "continue"
}
```

```json
{
    "title": "Decimal Place Analysis",
    "content": "Both numbers are decimals. .9 has one decimal place, and .11 has two decimal places. To compare them accurately, we should convert them to a common format.",
    "next_action": "continue"
}
```

```json
{
    "title": "Conversion to Common Format",
    "content": "Let's convert .9 to a two-decimal place number. .9 is equivalent to 0.90. Now we can compare 0.90 with 0.11.",
    "next_action": "continue"
}
```

```json
{
    "title": "Digit-by-Digit Comparison",
    "content": "Comparing the numbers digit by digit: 0.90 vs. 0.11. The first digit before the decimal point is 0 for both, so we move to the first decimal place. 9 is greater than 1.",
    "next_action": "continue"
}
```

```json
{
    "title": "Final Comparison",
    "content": "Since 9 is greater than 1, we can conclude that .9 is larger than .11.",
    "next_action": "final_answer"
}
```

```json
{
    "title": "Final Answer",
    "content": ".9 is larger than .11.",
    "next_action": "final_answer"
}
```

