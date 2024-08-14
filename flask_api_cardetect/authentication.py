
from .enviroment import SECRET_KEY



class Authentication:

    @staticmethod
    def authenticate(secret_key:str):
        """Meétodo de validação da chave do cliente
         
         ->Implementação fake apenas para ilustrar a lógica

        Args:
            secret_key (str): chave secreta do cliente hipotetico

        Raises:
            Exception: exceção gerada por erro em configuração do ambiente

        Returns:
            bool: respota de autenticação bem sucedida
        """        
        if SECRET_KEY is None:
            raise Exception("Secret key is not set")
        return SECRET_KEY == secret_key