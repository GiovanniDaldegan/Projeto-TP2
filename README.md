# Projeto-TP2
Projeto da disciplina Técnicas de Programação 2 do semestre 2025/1.

Este projeto tem como finalidade aplicar as técnicas estudadas em aula de
metodologias ágeis, desenvolvimento orientado a testes, análise de requisitos,
confecção de diagramas, entre outras.

A aplicação desenvolvida consiste em um site de gerenciamento de compras e
compartilhamento de preços, na qual seus usuários podem buscar produtos para
planejar suas compras, consultar preços atualizados por outros usuários,
gerenciar listas de compras, etc.

Para isso, desenvolvemos o servidor utilizando Python e as bibliotecas Flask e
Flask-SocketIO para estabelecer a conexão por web-sockets; e a aplicação do
cliente usando JavaScript e SocketIO.

#### Link para o repositório do projeto no GitHub
https://github.com/GiovanniDaldegan/Projeto-TP2

## Como executar o projeto

### Opção 1: Menu interativo (Mais fácil)
```bash
# Menu Python (recomendado)
python3 dev.py

# Ou menu Bash
./setup.sh
```

### Opção 2: Usando comandos diretos
```bash
# Configurar ambiente
python3 dev.py setup

# Iniciar servidor
python3 dev.py server

# Executar testes
python3 dev.py test

# Ver status do projeto
python3 dev.py status

# Menu interativo
python3 dev.py menu
```

### Opção 3: Usando Makefile
```bash
# Configurar ambiente
make setup

# Iniciar servidor
make dev

# Executar testes
make test

# Ver todos os comandos disponíveis
make help
```

### Opção 4: Usando script bash
```bash
# Configurar ambiente
./setup.sh

# Ativar ambiente virtual
source .venv/bin/activate

# Iniciar servidor
python aplicação/app.py

# Executar testes
python aplicação/test/test_db_controller.py
```

### Opção 5: Manual
```bash
# 1. Criar ambiente virtual
python3 -m venv .venv

# 2. Ativar ambiente virtual
source .venv/bin/activate

# 3. Instalar dependências
pip install -r requirements.txt

# 4. Executar servidor
cd aplicação
python app.py

# 5. Executar testes (em outro terminal)
cd aplicação
python test/test_db_controller.py
```

### Acessar a aplicação
- URL: http://localhost:5000
- Também pode ser acessada no endereço IP e porta exibidos no terminal durante
o início da execução

## Executar testes

### Teste geral (com verificação de cobertura)
```bash
pytest --cov-config=aplicação/test/.coveragerc --cov=aplicação aplicação/test/test_db.py
```

### Teste de requisições
```bash
# 1. Iniciar servidor
python aplicação/app.py test

# 2. Executar testes em outro servidor
pytest --cov-config=aplicação/test/.coveragerc aplicação/test/test_requests.py
```

## Documentação
Para gerar a documentação da aplicação, é necessário instalar o Doxygen.
Com o software instalado, execute `doxygen` na raiz do repositório e serão
geradas as páginas da documentação. Acesse em:
`artefatos/docs/html/index.html`.

## Estrutura do projeto
```
Projeto-TP2/
├── aplicação/                # Código da aplicação Flask
│   ├── app.py                # Arquivo principal do servidor
│   ├── modules/              # Módulos Python
│   │   ├── db_controller.py  # Controlador do banco de dados
│   │   ├── i_*.py            # Interfaces SocketIO
│   │   └── utils.py          # Utilitários
│   ├── static/               # Arquivos estáticos (CSS, JS, imagens)
│   ├── templates/            # Templates HTML
│   ├── test/                 # Testes unitários
│   └── databases/            # Banco de dados SQLite
├── artefatos/                # Documentação e artefatos
├── requirements.txt          # Dependências Python
├── dev.py                    # Script de desenvolvimento
├── setup.sh                  # Script de configuração
├── Makefile                  # Automação de tarefas
└── README.md                 # Este arquivo
```

## Dependências
- **Flask**: Framework web
- **Flask-SocketIO**: Suporte a WebSockets
- **python-socketio**: Cliente SocketIO para testes
- **SQLite**: Banco de dados (built-in do Python)

## Tecnologias utilizadas
- **Backend**: Python + Flask + Flask-SocketIO
- **Frontend**: HTML + CSS + JavaScript + SocketIO
- **Banco de dados**: SQLite
- **Documentação**: Doxygen

## Backlog
Funcionalidades em ordem de prioridade:

- [x] Página de pesquisa de produtos
- [ ] Lista de compras
- [ ] Cadastro de produto
- [ ] Registro de cliente
- [ ] Avaliação de produto
- [ ] Indicações de supermercados baseadas no carrinho
- [ ] Histórico de sessões de compras
- [ ] Lista de produtos não comprados -> indicação de onde comprar
- [ ] Recomendação de compra baseado no histórico
- [ ] Listar preços anteriores de um dado produto
- [ ] Localização do produto dentro do supermercado
- [ ] Medição de confiabilidade do preço apresentado

## Padrões do projeto
O arquivo [Padrões_do_projeto.md](artefatos/Padrões_do_projeto.md) explica:
- Qual o diretório adequado para cada tipo de arquivo
- Como cada arquivo deve ser nomeado
- Como documentar o código
- Como redigir os relatórios (devem ser atualizados a cada sessão de trabalho)
- O que deve estar presente na especificação final do projeto

## Desenvolvido por:
- Davi Sousa
- Giovanni Daldegan
- Márcio Vieira
- Nirva Neves
- Ricardo Nabuco
- Rodrigo Rafik Menêzes de Moraes
- Rute Fernandes
- Tauã Valentim de Albuquerque Martins Frade
