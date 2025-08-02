import secrets
import string

def gerar_id():
    caracteres = string.ascii_uppercase + string.digits
    return ''.join(secrets.choice(caracteres) for _ in range(5))

class IndentificavelMixin:
    def __init__(self):
        self.id = str(gerar_id())
    
    def get_id(self):
        return self.id