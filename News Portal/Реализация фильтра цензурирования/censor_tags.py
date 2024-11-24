from django import template  
import re  

register = template.Library()  

# Список запрещенных слов  
CENSORED_WORDS = ['ругательство1', 'ругательство2', 'редиска']  

@register.filter(name='censor')  
def censor(value):  
    if not isinstance(value, str):  
        raise ValueError("Фильтр 'censor' применяется только к строкам.")  
    
    # Подстановка для каждого ругательства  
    for word in CENSORED_WORDS:  
        regex = re.compile(re.escape(word), re.IGNORECASE)  
        # Замена ругательства на "звёздочки"  
        value = regex.sub(word[0] + '*' * (len(word) - 1), value)  
    
    return value  