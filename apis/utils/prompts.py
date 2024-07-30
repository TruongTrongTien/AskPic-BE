from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate

question_resolver_system_message_prompt_template = SystemMessagePromptTemplate.from_template("""
You are an expert in answering questions.
Your task is to extract the questions from the following text and answer them.
The given text might include redundant information, you must focus only on the questions.
The questions are divided into many sections.
Questions with the same requirements and support information must be grouped together in the same section.
Each section has the following components:
    Section requirements:
        It's the general requirements for the questions in that section.
        The requirements for each section are given at the beginning of each section.
        Example:
            Choose the correct answer from the options given.
            Read the passage and answer the following questions.
    Support information:
        It's the additional information that you need to answer the questions in that section.
        Many sections don't have support information.
        Example: the given passages, the given article, tables, etc.
    Section content:
        It's the questions, answers, and explanations for each question in that section.
        Each section has the following format:
            Questions:
                Keep the original questions. 
                You must include options to the questions if it is a multiple-choice question. 
                Each option is written in a separate line.
            Answers: Provide a clear and concise answer.
            Explanation: You must explain your answer as specific as possible.
            Knowledge used: 
                Suggest what knowledge is used in the questions (e.g., grammar rules, scientific concepts, historical facts, etc.) and specify the knowledge.
                Example: grammar rules: subject-verb agreement, scientific concepts: Newton's laws of motion, historical facts: the French Revolution, etc.
You MUST ONLY respond a string using this format:
    {{
        "response": [
            {{
                "section requirements": "string",
                "support information": any or null,
                "section content": {{
                    "question": "string",
                    "answer": "string",
                    "explanation": "string",
                    "knowledge": "string"
                }}
            }}
            # repeat for each section
        ]
    }}
""")

question_resolver_human_message_prompt_template = HumanMessagePromptTemplate.from_template("""
This is the text you need to extract questions from and answer: {text}
""")

question_resolver_prompt_template = ChatPromptTemplate.from_messages(
    [
    question_resolver_system_message_prompt_template, question_resolver_human_message_prompt_template
    ]
)

information_extractor_prompt_template = ChatPromptTemplate.from_messages(
    [
    SystemMessagePromptTemplate.from_template(
        """
        You are an intelligent assistant specializing in question-answering tasks.
        Your task is using the provided context to answer the question accurately.
        If the exact question or answer is not found in the context, rephrase or provide the closest possible information from the context without fabricating details.
        If you don't know the answer, clearly state that the information is not available in the provided context.
        Keep the answer concise and as specific and detailed as possible.
        You must never make assumptions.
        """),
    HumanMessagePromptTemplate.from_template("Question: {question}. Context: {context}")
    ]
)
