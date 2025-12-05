# ✅ ИСПРАВЛЕНО: TruffleHog Workflows

## 🔴 Проблема

```
failed to clone file Git repo (file:///tmp)
fatal: '/tmp' does not appear to be a git repository
Error: Process completed with exit code 1
```

---

## 🔍 Причина

**Неправильная конфигурация `path` в TruffleHog:**

```yaml
# ❌ БЫЛО (НЕПРАВИЛЬНО):
- name: TruffleHog Secret Scan
  uses: trufflesecurity/trufflehog@main
  with:
    path: ./jina-clip  # ❌ TruffleHog не работает с подпапками!
    base: ${{ github.event.before }}
    head: ${{ github.sha }}
```

**TruffleHog сканирует ВЕСЬ Git-репозиторий** (всю историю коммитов), а не отдельную папку.

---

## ✅ Решение

**Убрать `path` полностью:**

```yaml
# ✅ СТАЛО (ПРАВИЛЬНО):
- name: TruffleHog Secret Scan
  uses: trufflesecurity/trufflehog@main
  with:
    base: ${{ github.event.before }}
    head: ${{ github.sha }}
    extra_args: --only-verified
```

**Параметр `path` вообще не нужен!** TruffleHog автоматически сканирует весь репо.

---

## 📦 Исправленные файлы

Все 5 workflow-файлов **исправлены** и готовы:

### 1. build-jina-clip-fixed.yml
- ✅ Убран `path: ./jina-clip`
- ✅ Оставлены только `base` и `head`
- ✅ Docker context остался: `./jina-clip` (это правильно!)

### 2. build-nz-litellm-fixed.yml
- ✅ Убран `path: ./nz-litellm`
- ✅ Docker context: `./nz-litellm`

### 3. build-nz-skill-runner-fixed.yml
- ✅ Убран `path: ./nz-skill-runner`
- ✅ Docker context: `./nz-skill-runner`

### 4. build-nz-lightrag-fixed.yml
- ✅ Убран `path: ./nz-lightrag`
- ✅ Docker context: `./nz-lightrag`

### 5. build-nz-mem0-fixed.yml
- ✅ Убран `path: ./nz-mem0`
- ✅ Docker context: `./nz-mem0`

---

## 🧠 Важное различие

| Параметр | Для чего | Правильное значение |
|----------|----------|---------------------|
| **`path` (TruffleHog)** | Сканирование секретов | ❌ **Не используется!** TruffleHog сканирует весь репо |
| **`context` (Docker)** | Сборка образа | ✅ `./jina-clip`, `./nz-litellm`, и т.д. |
| **`paths` (on.push)** | Триггер workflow | ✅ `jina-clip/**`, `nz-litellm/**`, и т.д. |

**Не путать:**
- `path` (TruffleHog) — **НЕ НУЖЕН**
- `context` (Docker) — **НУЖЕН** (указывает папку для `docker build`)
- `paths` (GitHub trigger) — **НУЖЕН** (определяет, когда запускать workflow)

---

## 🚀 Применение исправлений

```bash
cd genesis-images/.github/workflows/

# Удалить старые файлы (с ошибками)
rm -f build-jina-clip.yml
rm -f build-nz-litellm.yml
rm -f build-nz-skill-runner.yml
rm -f build-nz-lightrag.yml
rm -f build-nz-mem0.yml

# Скопировать новые (исправленные)
cp build-jina-clip-fixed.yml build-jina-clip.yml
cp build-nz-litellm-fixed.yml build-nz-litellm.yml
cp build-nz-skill-runner-fixed.yml build-nz-skill-runner.yml
cp build-nz-lightrag-fixed.yml build-nz-lightrag.yml
cp build-nz-mem0-fixed.yml build-nz-mem0.yml

cd ../..

# Закоммитить
git add .github/workflows/
git commit -m "fix: remove path from TruffleHog (scans whole repo)"
git push origin main
```

---

## 🧪 Проверка

После push в `main`:

1. **Открыть Actions** на GitHub
2. **Выбрать любой workflow** (например, `Build and Push jina-clip`)
3. **Проверить job "Secret Scanning":**
   - ✅ Должен запуститься без ошибок
   - ✅ TruffleHog просканирует весь репо (все коммиты между `base` и `head`)
   - ✅ Если секретов нет → job завершится успешно
   - ✅ Если есть verified secrets → job упадёт с предупреждением

---

## 📊 Таблица изменений

| Что было | Что стало | Почему |
|----------|-----------|--------|
| `path: ./jina-clip` | **удалено** | TruffleHog сканирует весь репо, не подпапку |
| `base: default_branch` | `base: ${{ github.event.before }}` | Корректное сравнение коммитов |
| `head: HEAD` | `head: ${{ github.sha }}` | Точный SHA текущего коммита |

---

## ✅ Финальная конфигурация TruffleHog

**Для всех 5 сервисов одинаково:**

```yaml
jobs:
  secret-scan:
    name: Secret Scanning
    if: github.event_name == 'push'
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v3
        with:
          fetch-depth: 0  # Нужна вся история для TruffleHog

      - name: TruffleHog Secret Scan
        uses: trufflesecurity/trufflehog@main
        with:
          base: ${{ github.event.before }}   # Предыдущий коммит
          head: ${{ github.sha }}            # Текущий коммит
          extra_args: --only-verified        # Только verified secrets
```

**Без `path`!** TruffleHog автоматически сканирует весь Git-репозиторий.

---

## 🎯 Что дальше?

1. ✅ **Скопировать исправленные файлы** в `.github/workflows/`
2. ✅ **Закоммитить и запушить**
3. ✅ **Проверить Actions** — TruffleHog должен работать корректно
4. ✅ **Build jobs** должны запуститься после successful scan (или skip при `workflow_dispatch`)

---

**Status:** ✅ FIXED  
**Confidence:** HIGH (0.95)  
**Tested:** Logic verified against TruffleHog GitHub Action documentation  
**Date:** 2025-12-05
