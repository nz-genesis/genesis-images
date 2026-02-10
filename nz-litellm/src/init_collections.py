def init_qdrant():
    """Проверка доступности Qdrant (для будущих версий)."""
    # NOTE: Qdrant не установлен в текущем образе
    return False

def init_postgres(url: str):
    """Проверка подключения к PostgreSQL."""
    # NOTE: PostgreSQL драйвер не установлен в текущем образе
    return False
