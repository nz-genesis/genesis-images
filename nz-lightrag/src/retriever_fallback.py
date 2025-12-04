# ВАЖНО: Импорт QdrantRetriever удален, так как он не существует в lightrag==0.1.0b6
from lightrag.components.retriever.bm25_retriever import BM25Retriever
from lightrag.components.retriever.postgres_retriever import PostgresRetriever
from lightrag.components.retriever.llm_retriever import LLMRetriever
from lightrag.components.retriever.reranker_retriever import RerankerRetriever

class FallbackRetriever:
    def __init__(self, postgres_url, llm_client):
        self.retrievers = []

        # ВАЖНО: Блок QdrantRetriever полностью удален.
        # Мы можем вернуть его, когда появится рабочая версия.

        try:
            self.retrievers.append(BM25Retriever())
        except Exception:
            pass

        try:
            # Убеждаемся, что postgres_url не None перед созданием
            if postgres_url:
                self.retrievers.append(PostgresRetriever(connection_string=postgres_url))
        except Exception:
            pass

        try:
            self.retrievers.append(
                LLMRetriever(llm_client=llm_client, model_kwargs={"model": "gpt-4o-mini"}, text_limit=2048)
            )
        except Exception:
            pass

        try:
            self.retrievers.append(RerankerRetriever())
        except Exception:
            pass

        if not self.retrievers:
            raise Exception("Нет доступных retriever-компонентов!")

    def retrieve(self, query):
        last_error = None

        for retr in self.retrievers:
            try:
                result = retr(query=query, top_k=5)
                if result:
                    return result
            except Exception as e:
                last_error = e

        raise Exception(f"Все retriever-компоненты упали. Последняя ошибка: {last_error}")