from django import template
from flashtext import KeywordProcessor
from news.badwords import OBSCENE_WORDS


register = template.Library()

keyword_processor = KeywordProcessor()
keyword_processor.add_keywords_from_dict(OBSCENE_WORDS)


@register.filter()
def makegoodwords(value):
    new_value = keyword_processor.replace_keywords(value)
    return new_value

