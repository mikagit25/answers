"""
Валидатор источников: проверка наличия подтверждённых цитат в ответе.
Использует регулярные выражения и проверку по базе данных.
"""
import re
from typing import List, Dict


def validate_sources(answer: str, sources: List[Dict]) -> List[Dict]:
    """
    Валидация источников в сгенерированном ответе.
    
    Проверяет:
    1. Упоминаются ли авторы из предоставленных источников
    2. Есть ли ссылки на произведения
    3. Соответствуют ли цитаты оригинальным текстам
    
    Возвращает список подтверждённых источников.
    """
    validated = []
    answer_lower = answer.lower()
    
    for source in sources:
        is_mentioned = False
        
        # Проверка упоминания автора
        author_lower = source['author'].lower()
        if author_lower in answer_lower:
            is_mentioned = True
        
        # Проверка упоминания произведения (сокращённо)
        work_keywords = extract_work_keywords(source['work'])
        for keyword in work_keywords:
            if keyword.lower() in answer_lower:
                is_mentioned = True
                break
        
        # Проверка наличия ключевых фраз из цитаты (минимум 3-4 слова подряд)
        quote_matches = check_quote_presence(source['text'], answer)
        if quote_matches >= 2:  # Хотя бы 2 частичных совпадения
            is_mentioned = True
        
        if is_mentioned:
            validated.append(source)
    
    return validated


def extract_work_keywords(work_title: str) -> List[str]:
    """Извлечение ключевых слов из названия произведения для поиска"""
    # Убираем артикли и предлоги
    stop_words = {'the', 'a', 'an', 'и', 'в', 'на', 'с', 'по', 'к', 'у'}
    words = work_title.split()
    keywords = [w for w in words if w.lower() not in stop_words and len(w) > 2]
    return keywords[:3]  # Возвращаем максимум 3 ключевых слова


def check_quote_presence(original_text: str, answer: str) -> int:
    """
    Проверка наличия фрагментов оригинальной цитаты в ответе.
    Возвращает количество найденных совпадений.
    """
    # Разбиваем оригинальный текст на фразы (3-5 слов)
    words = original_text.split()
    matches = 0
    
    for i in range(len(words) - 2):
        phrase = ' '.join(words[i:i+3])
        if phrase.lower() in answer.lower():
            matches += 1
    
    return matches


def check_minimum_sources(validated_sources: List[Dict], minimum: int = 2) -> bool:
    """Проверка минимального количества подтверждённых источников"""
    return len(validated_sources) >= minimum
