# API REST - Raízes do Nordeste

Backend desenvolvido em Python (Flask) para o Projeto Multidisciplinar (Trilha Back-End). O sistema gerencia o cadastro de unidades físicas, cardápio regionalizado, controle de estoque por loja e o fluxo de pedidos multicanal da rede.

## Requisitos de ambiente
- Python 3.10 ou superior
- Git
- Postman ou Insomnia (para execução da suíte de testes)

## Instruções para execução local

**1. Clonar o repositório**
`bash
git clone https://github.com/Deleste01/projeto-backend-raizes.git
cd projeto-backend-raizes
`

**2. Criar e ativar o ambiente virtual**
É recomendado rodar a aplicação em um ambiente virtual (venv) para isolar as dependências.
`bash
python3 -m venv venv
source venv/bin/activate
`

**3. Instalar dependências**
Com o ambiente ativado, instale as bibliotecas necessárias:
`bash
pip install -r requirements.txt
`

**4. Configurar variáveis de ambiente**
Crie o seu arquivo de ambiente local copiando o exemplo disponibilizado no repositório:
`bash
cp .env.example .env
`
*(Caso necessário, edite o arquivo `.env` para ajustar a SECRET_KEY do JWT ou configurações locais).*

**5. Banco de dados e Migrations**
O projeto utiliza SQLite para facilitar a execução e os testes locais. Para criar o banco e as tabelas, execute as migrations:
`bash
flask db upgrade
`
Para popular o banco com dados iniciais e facilitar os testes, rode o script de seed:
`bash
python app/infrastructure/seed.py
`

**6. Iniciar a API**
`bash
flask run
`
A API estará rodando por padrão em `http://127.0.0.1:5000`.

---

## Documentação e Testes

### Swagger / OpenAPI
Com a aplicação em execução, a documentação interativa dos contratos da API (Swagger) pode ser acessada através do navegador na rota: `/api/docs` *(ou a rota equivalente configurada na raiz da interface)*. Lá estão descritos os *schemas*, *status codes* esperados e o formato padrão de erro.

### Coleção de Testes (Postman)
Na raiz do repositório encontra-se o arquivo `testes_postman.json`. 
Para testar os fluxos:
1. Abra o Postman e vá em `Import`.
2. Selecione o arquivo `.json`.
3. A coleção possui mais de 10 cenários (positivos e negativos), cobrindo desde autenticação e validações de regras de negócio, até fluxo de pagamento negado e controle de estoque.
4. Lembre-se de rodar primeiro a rota de `Login` para obter o Token JWT e inseri-lo no cabeçalho das rotas protegidas.

---

## Segurança e Privacidade (LGPD)

A arquitetura e as regras de negócio foram pensadas respeitando as diretrizes de segurança e a Lei Geral de Proteção de Dados:

* **Finalidade e Minimização:** Coletamos apenas dados estritamente necessários (nome e e-mail) no momento do cadastro. A finalidade é unicamente a identificação do cliente no fluxo de pedidos (Base Legal: Execução de Contrato).
* **Armazenamento Seguro:** As senhas dos usuários nunca são armazenadas em texto plano. É utilizado um algoritmo de hash (através do *werkzeug.security*) para garantir a segurança da credencial no banco de dados.
* **Privacidade nos Contratos:** Os endpoints que retornam dados de usuário foram modelados para omitir hashes de senha e dados sensíveis nas respostas (Responses JSON).
* **Controle de Acesso e Autorização:** O sistema possui proteção em rotas sensíveis utilizando tokens JWT, validando não apenas a autenticação, mas a autorização baseada em perfis (`role`). Clientes não têm permissão para atualizar status de produção ou alterar estoque, limitando a superfície de ataques.