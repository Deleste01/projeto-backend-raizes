# Raízes do Nordeste - API REST (Back-End)

Esse é o repositório do backend do projeto Raízes do Nordeste, desenvolvido para a disciplina de Projeto Multidisciplinar. A API foi construída em Python com Flask e tem como objetivo centralizar e gerenciar unidades, cardápio, estoque e os pedidos multicanal da rede.

## O que você vai precisar

Antes de começar, certifique-se de ter instalado na sua máquina:
- Python 3.10 ou superior
- Git (opcional, caso prefira baixar o código via arquivo ZIP direto do GitHub)
- Postman ou Insomnia (para importar e executar a coleção de testes)

---

## Como rodar o projeto localmente

Siga a ordem dos comandos abaixo para configurar a aplicação do zero.

### 1. Baixando o código
Abra o seu terminal e faça o clone do repositório:
```bash
git clone [https://github.com/Deleste01/projeto-backend-raizes.git](https://github.com/Deleste01/projeto-backend-raizes.git)
cd projeto-backend-raizes

(Se preferiu baixar o ZIP, extraia o arquivo e abra o terminal dentro da pasta principal do projeto).

2. Criando e ativando o Ambiente Virtual (venv)
É recomendado o uso de um ambiente virtual para isolar as bibliotecas do projeto.

Primeiro, crie o ambiente virtual rodando o comando:

Bash
python -m venv venv
Em seguida, ative o ambiente de acordo com o seu sistema operacional:

Para Linux e macOS:

Bash
source venv/bin/activate
Para Windows (PowerShell / CMD):

PowerShell
.\venv\Scripts\activate
Aviso para usuários de Windows: se o PowerShell bloquear a execução com um erro vermelho de permissão, rode este comando primeiro para destravar a execução de scripts: Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned

3. Instalando as dependências
Com o seu ambiente virtual ativado (você verá um (venv) no início da linha do terminal), instale as bibliotecas necessárias:

python -m pip install -r requirements.txt

Dica: Usar python -m pip em vez de apenas pip garante que os pacotes sejam instalados estritamente dentro do ambiente virtual, prevenindo o erro de ModuleNotFoundError que costuma acontecer em algumas configurações do Windows.

4. Configurando as Variáveis de Ambiente
A API precisa de um arquivo de configuração para rodar. Você só precisa duplicar o arquivo de exemplo.

No Linux ou Mac:

Bash
cp .env.example .env
No Windows:

PowerShell
copy .env.example .env
5. Subindo o Banco de Dados e a API
Com tudo configurado, inicie o servidor:

Bash
python run.py
A API estará online e acessível no endereço: http://127.0.0.1:5000

Nota sobre o Banco de Dados: Eu configurei o script run.py para automatizar a criação do banco de dados (SQLite) e realizar a carga inicial de produtos e usuários assim que o servidor é ligado. Não é necessário executar comandos de migration manualmente.

Documentação e Testes
Swagger
A documentação visual da API sobe automaticamente junto com o servidor. Para visualizar os endpoints, os schemas de requisição/resposta e testar as rotas, acesse no seu navegador:
http://127.0.0.1:5000/api/docs

Postman
O arquivo Raizes do Nordeste - Testes API.postman_collection.json está na raiz deste repositório e contém todos os cenários de teste mapeados.

Abra o Postman e importe o arquivo .json.

A coleção possui 12 testes sequenciais que cobrem o caminho feliz (criar pedido, pagar, atualizar status) e as validações de regras de negócio (falta de estoque, falta de permissão de acesso, etc).

Aviso Crítico sobre os Perfis e Tokens:
Para testar os bloqueios de segurança (LGPD/Roles) sem precisar fazer cadastros manuais, o sistema já inicia com dois usuários pré-configurados. Você precisará rodar a rota de Login (T02) com eles para obter os Tokens JWT adequados:

Perfil Cliente

E-mail: cliente@raizes.com

Senha: cliente123

Onde usar: Utilize o token deste usuário para rodar os primeiros testes (criação do pedido) e, obrigatoriamente, no teste T11 (Acesso Negado 403). A API vai reconhecer o perfil restrito e barrar a tentativa de atualizar a entrega.

Perfil Funcionário

E-mail: gustavo@raizes.com

Senha: meusegredo123

Onde usar: Utilize o token deste usuário para rodar os testes de simulação de pagamento (T04) e os testes de atualização de status da cozinha (T05 e T06).

Segurança e Privacidade (LGPD)
A arquitetura e as regras de negócio foram projetadas respeitando diretrizes essenciais de segurança e proteção de dados:

Minimização de Dados (LGPD): No cadastro do cliente, peço apenas o nome e o e-mail. A base legal utilizada é a Execução de Contrato, pois a aplicação necessita apenas do básico para identificar de quem é o pedido.

Senhas com Hash: Nenhuma credencial é armazenada em texto plano no banco de dados. Usei a biblioteca werkzeug.security para gerar e validar o hash das senhas.

Omissão de dados sensíveis: Tomei o cuidado de omitir dados sensíveis no retorno da API. Operações de consulta de usuários, por exemplo, não devolvem a senha no JSON.

Autorização (Roles): As rotas são rigorosamente protegidas por tokens JWT e bloqueio por perfil. Isso significa que um usuário com o perfil de cliente não tem permissão para acessar rotas da cozinha ou alterar o estoque. Tentativas de acesso não autorizado retornam o erro 403 (Proibido).