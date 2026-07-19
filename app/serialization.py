import re

_LIMITE_CAMEL = re.compile(r'(?<!^)(?=[A-Z])')


def _para_snake(chave):
    return _LIMITE_CAMEL.sub('_', chave).lower()


def normalizar_chaves(dados):
    if isinstance(dados, dict):
        return {_para_snake(chave): normalizar_chaves(valor) for chave, valor in dados.items()}
    if isinstance(dados, list):
        return [normalizar_chaves(item) for item in dados]
    return dados
