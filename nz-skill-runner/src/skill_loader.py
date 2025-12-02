"""
skill_loader: читает SKILL.md с frontmatter, собирает 'меню' и пути к скриптам.
Ожидает, что на хосте репозиторий находится по пути, который прокинут как /app/repo (read-only).
"""
import os
import frontmatter
import logging
from typing import List, Dict, Any
from fastapi import HTTPException

SKILLS_DIR = os.getenv("SKILLS_DIR_PATH", "/app/repo/skills")

class SkillsRegistry:
    def __init__(self):
        self._skills: Dict[str, Dict] = {}
        self._menu: List[Dict] = []

    def load_skills(self):
        self._skills.clear()
        self._menu.clear()
        logging.info(f"Сканирование директории со Скиллами: {SKILLS_DIR}")
        if not os.path.isdir(SKILLS_DIR):
            logging.warning(f"Директория со Скиллами '{SKILLS_DIR}' не найдена. Пропускаем загрузку.")
            return

        for root, _, files in os.walk(SKILLS_DIR):
            if "SKILL.md" in files:
                skill_name = os.path.basename(root)
                namespace = os.path.basename(os.path.dirname(root))
                full_slug = f"{namespace}/{skill_name}"
                try:
                    path = os.path.join(root, "SKILL.md")
                    with open(path, "r", encoding="utf-8") as f:
                        skill_file = frontmatter.load(f)
                    
                    metadata = skill_file.metadata
                    metadata['name'] = full_slug
                    
                    script_path = None
                    if metadata.get("script"):
                        candidate = os.path.join(root, metadata["script"])
                        if os.path.exists(candidate):
                            script_path = candidate
                        else:
                            logging.warning(f"Для Скилла {full_slug} указан скрипт '{metadata['script']}', но файл не найден.")

                    self._skills[full_slug] = {
                        "metadata": metadata,
                        "instructions": skill_file.content,
                        "script_path": script_path
                    }
                    
                    self._menu.append({
                        "name": full_slug,
                        "description": metadata.get("description", "Нет описания."),
                        "tags": metadata.get("tags", [])
                    })
                    logging.info(f"Загружен Скилл: {full_slug}")
                except Exception as e:
                    logging.error(f"Ошибка загрузки Скилла '{full_slug}' по пути {root}: {e}")

    def get_menu(self) -> List[Dict[str, Any]]:
        return self._menu

    def get_skill(self, name: str) -> Dict[str, Any]:
        skill = self._skills.get(name)
        if not skill:
            raise HTTPException(status_code=404, detail=f"Скилл '{name}' не найден.")
        return skill

skills_registry = SkillsRegistry()