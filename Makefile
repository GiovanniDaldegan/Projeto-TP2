# Makefile para Projeto-TP2

# Configurações
PYTHON = .venv/bin/python
PIP = .venv/bin/pip
VENV = .venv
APP_DIR = aplicação
TEST_DIR = $(APP_DIR)/test

# Cores para output
GREEN = \033[0;32m
YELLOW = \033[0;33m
RED = \033[0;31m
NC = \033[0m # No Color

.PHONY: help setup install clean dev test test-db test-requests server docs

help: ## Mostra esta mensagem de ajuda
	@echo "$(GREEN)Projeto-TP2 - Comandos disponíveis:$(NC)"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "$(YELLOW)%-15s$(NC) %s\n", $$1, $$2}'

setup: ## Configura o ambiente virtual e instala dependências
	@echo "$(GREEN)Configurando ambiente...$(NC)"
	@if [ ! -d "$(VENV)" ]; then \
		echo "Criando ambiente virtual..."; \
		python3 -m venv $(VENV); \
	fi
	@echo "Atualizando pip..."
	@$(PIP) install --upgrade pip
	@echo "Instalando dependências..."
	@$(PIP) install -r requirements.txt
	@echo "$(GREEN)✅ Ambiente configurado!$(NC)"

install: setup ## Alias para setup

clean: ## Remove o ambiente virtual e arquivos temporários
	@echo "$(RED)Removendo ambiente virtual...$(NC)"
	@rm -rf $(VENV)
	@echo "Removendo arquivos temporários..."
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@echo "$(GREEN)✅ Limpeza concluída!$(NC)"

dev: setup ## Inicia o servidor em modo desenvolvimento
	@echo "$(GREEN)Iniciando servidor...$(NC)"
	@echo "Acesse: http://localhost:5000"
	@cd $(APP_DIR) && $(PYTHON) app.py

server: dev ## Alias para dev

test: setup ## Executa todos os testes
	@echo "$(GREEN)Executando testes...$(NC)"
	@echo "Teste do banco de dados:"
	@cd $(APP_DIR) && $(PYTHON) test/test_db_controller.py
	@echo "$(YELLOW)Para teste de requisições, inicie o servidor primeiro com 'make dev'$(NC)"

test-db: setup ## Executa apenas os testes do banco de dados
	@echo "$(GREEN)Executando testes do banco de dados...$(NC)"
	@cd $(APP_DIR) && $(PYTHON) test/test_db_controller.py

test-requests: setup ## Executa testes de requisições (servidor deve estar rodando)
	@echo "$(GREEN)Executando testes de requisições...$(NC)"
	@echo "$(YELLOW)Certifique-se de que o servidor esteja rodando em localhost:5000$(NC)"
	@cd $(APP_DIR) && $(PYTHON) test/test_requests.py

docs: ## Gera documentação com Doxygen
	@echo "$(GREEN)Gerando documentação...$(NC)"
	@if command -v doxygen >/dev/null 2>&1; then \
		doxygen Doxyfile; \
		echo "$(GREEN)✅ Documentação gerada em: artefatos/docs/html/index.html$(NC)"; \
	else \
		echo "$(RED)❌ Doxygen não instalado. Instale com: sudo apt-get install doxygen$(NC)"; \
	fi

status: ## Mostra status do ambiente
	@echo "$(GREEN)Status do ambiente:$(NC)"
	@echo "Ambiente virtual: $(if $(wildcard $(VENV)),$(GREEN)✅ Existe$(NC),$(RED)❌ Não existe$(NC))"
	@if [ -d "$(VENV)" ]; then \
		echo "Python: $$($(PYTHON) --version 2>&1)"; \
		echo "Pip: $$($(PIP) --version 2>&1 | cut -d' ' -f1-2)"; \
	fi
	@echo "Banco de dados: $(if $(wildcard $(APP_DIR)/databases/tables.db),$(GREEN)✅ Existe$(NC),$(YELLOW)⚠️ Será criado no primeiro uso$(NC))"

format: setup ## Formata o código com Black
	@echo "$(GREEN)Formatando código com Black...$(NC)"
	@$(PYTHON) -m black $(APP_DIR)

coverage: setup ## Roda testes com relatório de cobertura
	@echo "$(GREEN)Executando testes com cobertura...$(NC)"
	@$(PYTHON) -m pytest --cov-config=aplicação/test/.coveragerc --cov=aplicação --cov-report=term --cov-report=html aplicação/test/test_db.py
	@echo "$(GREEN)✅ Relatório gerado em: htmlcov/index.html$(NC)"

dynapyt-db: setup ## Executa Dynapyt no teste do banco de dados
	@echo "$(GREEN)Executando análise dinâmica com Dynapyt...$(NC)"
	@.venv\Scripts\dynapyt.exe --policy dynapyt.policies.timing_analysis ./aplicação/test/test_db_controller.py || true


# Comandos de conveniência
run: dev ## Alias para dev
start: dev ## Alias para dev
serve: dev ## Alias para dev
