# Genesis Images — AGENTS.md

**ACTIVE_MODE:** EXTERNAL
**MODE_SOURCE:** /root/.kilocode/modes/external.mode.md
**Тип:** Docker/ML образы

---

## Обзор

Репозиторий Docker и ML образов для системы Genesis.

## Назначение

- Docker образы для сервисов
- ML модели
- Build pipelines

## Структура

```
genesis-images/
├── .kilocode/           # Локальные файлы килокод
│   └── AGENTS.md        # ЭТОТ ФАЙЛ
├── nz-execution-gateway/ # Execution gateway
├── nz-intent-adapter/   # Intent adapter
├── nz-litellm/          # LiteLLM прокси
├── nz-mem0/             # Memory service
├── nz-stack-core/       # Stack core
├── .github/             # GitHub Actions
└── docs/                # Документация
```

## Правила работы

- Все изменения — только в этом репо
- При переключении на другое репо — новая сессия
- Локальные файлы килокод только в `.kilocode/`

## Режим работы

**ACTIVE_MODE:** ENGINEERING — для инженерных задач

