from lightrag.core.generator import Generator

class RAGManager:
    def __init__(self, llm_client, model_name, retriever, system_prompt):
        self.retriever = retriever
        self.generator = Generator(
            model_client=llm_client,
            model_kwargs={"model": model_name},
            prompt_kwargs={"template": f"{system_prompt}\n\nContext:\n{{context}}\n\nQuestion: {{query}}"}
        )

    def ask(self, query: str):
        # 1. Получаем контекст с помощью retriever'а
        context_results = self.retriever.retrieve(query)
        context_str = "\n".join([doc.text for doc in context_results])

        # 2. Вызываем генератор, который сам построит промпт и вызовет модель
        response = self.generator.call(query=query, context=context_str)
        return response