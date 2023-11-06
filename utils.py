import os
import sys

# Este arquivo conterá funções de utilidade que podem ser usadas em toda a aplicação.

def get_data_directory():
    """Obtém o diretório de dados da aplicação."""
    if getattr(sys, 'frozen', False):
        # Se o aplicativo estiver congelado (como um executável), use este caminho.
        return sys._MEIPASS
    else:
        # Caso contrário, use o diretório do arquivo de script.
        return os.path.dirname(__file__)
