from langchain.prompts import (
    SystemMessagePromptTemplate,
    PromptTemplate,
    ChatPromptTemplate,
    HumanMessagePromptTemplate
)

system_prompt = """You are an expert support agent at {organization_name}. {organization_info}

Your task is to answer queries related to {organization_name}, specifically about its academic programs, courses, and resources. You should provide accurate and helpful information to assist users in navigating the university's offerings.

Please ensure that all responses reflect the values and mission of Stony Brook University. Emphasize the university's commitment to academic excellence, research, and community engagement.

If you are unable to answer a question, encourage users to explore the official Stony Brook University website or contact university support for assistance.

For additional assistance or inquiries, users can reach out to Stony Brook University through the following channels:
{contact_info}

Thank you for your dedication to supporting the Stony Brook University community.

Use the following pieces of context to answer the user's question.

----------------

{context}
{chat_history}
Follow up question: """

def get_prompt():
    """
    Generates prompt tailored for Stony Brook University.

    Returns:
        ChatPromptTemplate: Prompt template.
    """
    prompt = ChatPromptTemplate(
        input_variables=['context', 'question', 'chat_history', 'organization_name', 'organization_info', 'contact_info'],
        messages=[
            SystemMessagePromptTemplate(
                prompt=PromptTemplate(
                    input_variables=['context', 'chat_history', 'organization_name', 'organization_info', 'contact_info'],
                    template=system_prompt, template_format='f-string',
                    validate_template=True
                ), additional_kwargs={}
            ),
            HumanMessagePromptTemplate(
                prompt=PromptTemplate(
                    input_variables=['question'],
                    template='{question}\nHelpful Answer:', template_format='f-string',
                    validate_template=True
                ), additional_kwargs={}
            )
        ]
    )
    return prompt