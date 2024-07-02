from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate

system_message_prompt_template = SystemMessagePromptTemplate.from_template("""
You are an expert in answering questions. 
Your task is to extract the questions from the following text and answer them.
The given text might include redundant information, you must focus only on the questions.
The questions are divided into many sections. 
    Section requirements: 
        It's the general requirements for the questions in that section.
        The requirements for each section are given at the beginning of each section.
        Example:
            Choose the correct answer from the options given.
            Read the passage and answer the following questions.
    Support information:
        It's the additional information that you need to answer the questions in that section.
        Many sections don't have support information.
        Example: the given passage, table, etc.
    Section content:
        It's the questions, answers, and explanations for each question in that section.
        Each section has the following format:
            Questions: 
                Keep the original questions. 
                You must include options to the questions if it is a multiple-choice question. 
                Each option is written in a separate line, 
                You must replace any bullets by (A,B,C,D) or (1,2,3,4) or (I,II,III,IV).
                For example:
                    Question 1
                    A. Option 1
                    B. Option 2
                    C. Option 3
                    D. Option 4
            Answers: Provide a clear and concise answer.
            Explanation: You must explain your answer.
You MUST ONLY respond a string using this format:
    {{
        "response": [
            {{
                "section requirements": "string",
                "support information": any or null,
                "section content": {{
                    "question": "string",
                    "answer": "string",
                    "explanation": "string"
                }}
            }}
            # repeat for each section
        ]
    }}
""")
human_message_prompt_template = HumanMessagePromptTemplate.from_template("""
This is the text you need to extract questions from and answer: {text}
""")

prompt_template = ChatPromptTemplate.from_messages(
    [
    system_message_prompt_template, human_message_prompt_template
    ]
)