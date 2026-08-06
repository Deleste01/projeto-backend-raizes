API REST - Raízes do Nordeste
Backend desenvolvido em Python (Flask) para o Projeto Multidisciplinar (Trilha Back-End). O sistema gerencia o cadastro de unidades físicas, cardápio regionalizado, controle de estoque por loja e o fluxo de pedidos multicanal da rede.

Requisitos de Ambiente
Python 3.10 ou superior

Git (opcional, caso prefira baixar via ZIP)

Postman ou Insomnia (para rodar a suíte de testes)

Como rodar o projeto localmente
1. Baixar o projeto
Você pode clonar o repositório via Git:

Bash
git clone https://github.com/Deleste01/projeto-backend-raizes.git
cd projeto-backend-raizes
Ou, se preferir, baixe o código-fonte em formato ZIP diretamente pelo GitHub e extraia a pasta. Lembre-se de abrir o terminal dentro da pasta principal do projeto (a que contém o arquivo run.py).

2. Criar e ativar o ambiente virtual (Recomendado)
Para evitar conflito de bibliotecas no seu computador, vamos isolar o ambiente.

No Linux/Mac:

Bash
python3 -m venv venv
source venv/bin/activate
No Windows (PowerShell):
Se você receber um erro vermelho dizendo que a execução de scripts está desabilitada, rode este comando primeiro para destravar:

PowerShell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
Depois, crie e ative o ambiente:

PowerShell
python -m venv venv
.\venv\Scripts\activate
3. Instalar as dependências
Com o ambiente ativado (venv), instale todas as bibliotecas necessárias:

Bash
pip install -r requirements.txt
4. Configurar variáveis de ambiente
Crie o seu arquivo de ambiente local fazendo uma cópia do exemplo que deixei no repositório:

Bash
cp .env.example .env
(No Windows, você pode simplesmente copiar e colar o arquivo .env.example na mesma pasta e renomear a cópia para .env).

5. Iniciar a API e o Banco de Dados
Para dar a partida no servidor, rode o comando abaixo na raiz do projeto:

Bash
python run.py
A API estará rodando por padrão em [http://127.0.0.1:5000](http://127.0.0.1:5000).
Nota: Ao rodar este comando, o sistema automaticamente verifica o banco de dados (SQLite) e já realiza uma carga inicial de dados (seeding) com usuários e produtos para facilitar os seus testes. Não é necessário rodar scripts de banco manualmente.

Documentação e Testes
Swagger / OpenAPI
Com a aplicação rodando, você pode acessar a documentação interativa dos contratos da API (Swagger) pelo navegador na rota: [http://127.0.0.1:5000/api/docs](http://127.0.0.1:5000/api/docs). Lá estão os schemas, status codes esperados e os formatos padronizados de erro.

Coleção de Testes (Postman)
Na raiz do repositório, você vai encontrar um arquivo .json com a coleção completa de testes (ex: testes_postman.json ou Raizes do Nordeste - Testes API.postman_collection.json).

Para testar o fluxo:

Abra o Postman e clique em Import.

Selecione o arquivo .json que está na pasta do projeto.

A coleção possui 12 cenários mapeados em sequência (positivos e negativos), cobrindo desde autenticação e regras de negócio até falhas de pagamento e controle de estoque.

Importante: Lembre-se de rodar primeiro a rota de Login (T02) para obter o Token JWT. Copie esse token e insira na aba Authorization (como Bearer Token) das próximas requisições protegidas.

Segurança e Privacidade (LGPD)
A arquitetura e as regras de negócio foram pensadas respeitando as diretrizes de segurança e a Lei Geral de Proteção de Dados:

Finalidade e Minimização: Coletamos apenas dados estritamente necessários (nome e e-mail) no momento do cadastro. A finalidade é unicamente a identificação do cliente no fluxo de pedidos (Base Legal: Execução de Contrato).

Armazenamento Seguro: As senhas dos usuários nunca são armazenadas em texto plano. Utilizo o algoritmo de hash do werkzeug.security para garantir a proteção total das credenciais no banco de dados.

Privacidade nos Contratos: Os endpoints que retornam dados de usuário foram modelados para omitir hashes de senha e outros dados sensíveis nas respostas (Responses JSON).

Controle de Acesso e Autorização: O sistema possui proteção rigorosa em rotas sensíveis utilizando tokens JWT. Ele valida não apenas a autenticação, mas a autorização baseada em perfis (role). Por exemplo, clientes não têm permissão para atualizar status de produção da cozinha ou alterar estoque, limitando significativamente a superfície de ataques.