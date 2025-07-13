#!/bin/bash

# Script de configuração do ambiente para o Projeto-TP2

# Função para mostrar o menu
show_menu() {
    clear
    echo "=================================================="
    echo "🎯 PROJETO-TP2 - MENU PRINCIPAL"
    echo "=================================================="
    echo "1. 🔧 Configurar ambiente virtual"
    echo "2. 🚀 Iniciar servidor"
    echo "3. 🧪 Executar todos os testes"
    echo "4. 🗄️ Testar apenas banco de dados"
    echo "5. 🌐 Testar apenas requisições (servidor deve estar rodando)"
    echo "6. 📊 Ver status do projeto"
    echo "7. 🧹 Limpar projeto"
    echo "8. ❓ Ajuda"
    echo "0. 🚪 Sair"
    echo "=================================================="
}

# Função para configurar ambiente
setup_environment() {
    echo "🔧 Configurando ambiente para Projeto-TP2..."

    # Verificar se Python está instalado
    if ! command -v python3 &> /dev/null; then
        echo "❌ Python3 não está instalado. Instale o Python3 primeiro."
        return 1
    fi

    # Criar ambiente virtual se não existir
    if [ ! -d ".venv" ]; then
        echo "📦 Criando ambiente virtual..."
        python3 -m venv .venv
        echo "✅ Ambiente virtual criado em .venv/"
    else
        echo "✅ Ambiente virtual já existe"
    fi

    # Ativar ambiente virtual
    echo "🔄 Ativando ambiente virtual..."
    source .venv/bin/activate

    # Instalar dependências
    echo "📥 Instalando dependências..."
    pip install --upgrade pip
    pip install -r requirements.txt

    echo "✅ Configuração completa!"
}

# Função para iniciar servidor
start_server() {
    if [ ! -d ".venv" ]; then
        echo "❌ Ambiente virtual não configurado. Execute a opção 1 primeiro."
        return 1
    fi
    
    echo "🚀 Iniciando servidor..."
    echo "📍 Acesse: http://localhost:5000"
    echo "💡 Pressione Ctrl+C para parar o servidor"
    
    source .venv/bin/activate
    cd aplicação
    python app.py
}

# Função para executar testes
run_tests() {
    if [ ! -d ".venv" ]; then
        echo "❌ Ambiente virtual não configurado. Execute a opção 1 primeiro."
        return 1
    fi
    
    source .venv/bin/activate
    cd aplicação
    
    case $1 in
        "all")
            echo "🧪 Executando todos os testes..."
            echo "🗄️ Teste do banco de dados:"
            python test/test_db_controller.py
            echo ""
            echo "🌐 Teste de requisições:"
            echo "⚠️ Certifique-se de que o servidor esteja rodando em localhost:5000"
            read -p "Pressione Enter para continuar ou Ctrl+C para cancelar..."
            python test/test_requests.py
            ;;
        "db")
            echo "🗄️ Executando teste do banco de dados..."
            python test/test_db_controller.py
            ;;
        "requests")
            echo "🌐 Executando teste de requisições..."
            echo "⚠️ Certifique-se de que o servidor esteja rodando em localhost:5000"
            read -p "Pressione Enter para continuar ou Ctrl+C para cancelar..."
            python test/test_requests.py
            ;;
    esac
}

# Função para mostrar status
show_status() {
    echo "📊 Status do projeto:"
    echo "📁 Diretório: $(pwd)"
    
    if [ -d ".venv" ]; then
        echo "🐍 Ambiente virtual: ✅ Existe"
        source .venv/bin/activate
        echo "🐍 Python: $(python --version 2>&1)"
        echo "📦 Pip: $(pip --version | cut -d' ' -f1-2)"
    else
        echo "🐍 Ambiente virtual: ❌ Não existe"
    fi
    
    if [ -f "aplicação/databases/tables.db" ]; then
        echo "🗄️ Banco de dados: ✅ Existe"
    else
        echo "🗄️ Banco de dados: ⚠️ Será criado no primeiro uso"
    fi
}

# Função para limpar projeto
clean_project() {
    echo "🧹 Limpando projeto..."
    read -p "❓ Tem certeza que deseja remover o ambiente virtual? (s/N): " confirm
    
    if [[ $confirm =~ ^[SsYy]$ ]]; then
        if [ -d ".venv" ]; then
            rm -rf .venv
            echo "✅ Ambiente virtual removido"
        fi
        
        find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
        find . -type f -name "*.pyc" -delete 2>/dev/null || true
        echo "✅ Arquivos temporários removidos"
        echo "✅ Limpeza concluída!"
    else
        echo "❌ Operação cancelada"
    fi
}

# Função para mostrar ajuda
show_help() {
    echo "============================================================"
    echo "📚 AJUDA - PROJETO-TP2"
    echo "============================================================"
    echo "🔧 Configurar ambiente: Cria .venv e instala dependências"
    echo "🚀 Iniciar servidor: Roda Flask em http://localhost:5000"
    echo "🧪 Testes: Executa testes do banco e/ou requisições"
    echo "📊 Status: Mostra informações do ambiente"
    echo "🧹 Limpar: Remove .venv e arquivos temporários"
    echo ""
    echo "📁 Estrutura do projeto:"
    echo "   aplicação/app.py - Servidor principal"
    echo "   aplicação/test/ - Testes unitários"
    echo "   aplicação/modules/ - Módulos Python"
    echo "   aplicação/static/ - CSS, JS, imagens"
    echo "   aplicação/templates/ - Templates HTML"
    echo ""
    echo "💡 Dicas:"
    echo "   - Execute 'Configurar ambiente' primeiro"
    echo "   - Para testes de requisições, inicie o servidor antes"
    echo "   - Use Ctrl+C para parar o servidor"
    echo "============================================================"
}

# Menu principal
main_menu() {
    while true; do
        show_menu
        read -p "👉 Escolha uma opção: " choice
        
        case $choice in
            1)
                setup_environment
                ;;
            2)
                start_server
                ;;
            3)
                run_tests "all"
                ;;
            4)
                run_tests "db"
                ;;
            5)
                run_tests "requests"
                ;;
            6)
                show_status
                ;;
            7)
                clean_project
                ;;
            8)
                show_help
                ;;
            0)
                echo "👋 Até logo!"
                exit 0
                ;;
            *)
                echo "❌ Opção inválida! Tente novamente."
                ;;
        esac
        
        echo ""
        read -p "⏸️ Pressione Enter para continuar..."
    done
}

# Verificar se foi chamado com parâmetros ou modo interativo
if [ $# -eq 0 ]; then
    # Modo interativo
    main_menu
else
    # Modo compatibilidade (comportamento original)
    setup_environment
fi
