#!/usr/bin/env python3
"""
Script de gerenciamento do projeto Projeto-TP2
Facilita as tarefas comuns de desenvolvimento
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path

class ProjectManager:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.venv_path = self.project_root / ".venv"
        self.python_path = self.venv_path / "bin" / "python"
        self.pip_path = self.venv_path / "bin" / "pip"
        self.app_path = self.project_root / "aplicação"
        
    def setup_venv(self):
        """Configura o ambiente virtual"""
        print("🔧 Configurando ambiente virtual...")
        
        if not self.venv_path.exists():
            print("📦 Criando ambiente virtual...")
            subprocess.run([sys.executable, "-m", "venv", str(self.venv_path)], check=True)
        else:
            print("✅ Ambiente virtual já existe")
        
        # Atualizar pip
        print("📥 Atualizando pip...")
        subprocess.run([str(self.pip_path), "install", "--upgrade", "pip"], check=True)
        
        # Instalar dependências
        print("📥 Instalando dependências...")
        requirements_file = self.project_root / "requirements.txt"
        if requirements_file.exists():
            subprocess.run([str(self.pip_path), "install", "-r", str(requirements_file)], check=True)
        
        print("✅ Ambiente configurado!")
    
    def run_server(self):
        """Executa o servidor Flask"""
        if not self.python_path.exists():
            print("❌ Ambiente virtual não configurado. Execute: python dev.py setup")
            return False
        
        print("🚀 Iniciando servidor...")
        print("📍 Acesse: http://localhost:5000")
        
        try:
            os.chdir(self.app_path)
            subprocess.run([str(self.python_path), "app.py"])
        except KeyboardInterrupt:
            print("\n🛑 Servidor interrompido")
        
        return True
    
    def run_tests(self, test_type="all"):
        """Executa os testes"""
        if not self.python_path.exists():
            print("❌ Ambiente virtual não configurado. Execute: python dev.py setup")
            return False
        
        print("🧪 Executando testes...")
        
        os.chdir(self.app_path)
        
        if test_type in ["all", "db"]:
            print("🗄️ Teste do banco de dados:")
            subprocess.run([str(self.python_path), "test/test_db_controller.py"])
        
        if test_type in ["all", "requests"]:
            print("🌐 Teste de requisições:")
            print("⚠️ Certifique-se de que o servidor esteja rodando em localhost:5000")
            try:
                subprocess.run([str(self.python_path), "test/test_requests.py"])
            except Exception as e:
                print(f"❌ Erro no teste de requisições: {e}")
                print("💡 Inicie o servidor primeiro com: python dev.py server")
        
        return True
    
    def clean(self):
        """Remove ambiente virtual e arquivos temporários"""
        print("🧹 Limpando projeto...")
        
        # Remover ambiente virtual
        if self.venv_path.exists():
            import shutil
            shutil.rmtree(self.venv_path)
            print("✅ Ambiente virtual removido")
        
        # Remover arquivos temporários
        for root, dirs, files in os.walk(self.project_root):
            # Remover __pycache__
            if "__pycache__" in dirs:
                shutil.rmtree(os.path.join(root, "__pycache__"))
            
            # Remover .pyc
            for file in files:
                if file.endswith('.pyc'):
                    os.remove(os.path.join(root, file))
        
        print("✅ Limpeza concluída!")
    
    def status(self):
        """Mostra status do projeto"""
        print("📊 Status do projeto:")
        print(f"📁 Diretório: {self.project_root}")
        print(f"🐍 Ambiente virtual: {'✅ Existe' if self.venv_path.exists() else '❌ Não existe'}")
        
        if self.python_path.exists():
            result = subprocess.run([str(self.python_path), "--version"], 
                                  capture_output=True, text=True)
            print(f"🐍 Python: {result.stdout.strip()}")
            
            result = subprocess.run([str(self.pip_path), "--version"], 
                                  capture_output=True, text=True)
            print(f"📦 Pip: {result.stdout.strip().split()[1]}")
        
        db_path = self.app_path / "databases" / "tables.db"
        print(f"🗄️ Banco de dados: {'✅ Existe' if db_path.exists() else '⚠️ Será criado no primeiro uso'}")
    
    def interactive_menu(self):
        """Menu interativo para gerenciar o projeto"""
        while True:
            print("\n" + "="*50)
            print("🎯 PROJETO-TP2 - MENU PRINCIPAL")
            print("="*50)
            print("1. 🔧 Configurar ambiente virtual")
            print("2. 🚀 Iniciar servidor")
            print("3. 🧪 Executar todos os testes")
            print("4. 🗄️ Testar apenas banco de dados")
            print("5. 🌐 Testar apenas requisições")
            print("6. 📊 Ver status do projeto")
            print("7. 🧹 Limpar projeto")
            print("8. ❓ Ajuda")
            print("0. 🚪 Sair")
            print("="*50)
            
            try:
                choice = input("👉 Escolha uma opção: ").strip()
                
                if choice == "1":
                    self.setup_venv()
                elif choice == "2":
                    print("\n💡 Pressione Ctrl+C para parar o servidor")
                    input("Pressione Enter para continuar...")
                    self.run_server()
                elif choice == "3":
                    self.run_tests("all")
                elif choice == "4":
                    self.run_tests("db")
                elif choice == "5":
                    print("\n⚠️ Certifique-se de que o servidor esteja rodando!")
                    input("Pressione Enter para continuar...")
                    self.run_tests("requests")
                elif choice == "6":
                    self.status()
                elif choice == "7":
                    confirm = input("❓ Tem certeza que deseja limpar o projeto? (s/N): ").strip().lower()
                    if confirm in ['s', 'sim', 'y', 'yes']:
                        self.clean()
                    else:
                        print("❌ Operação cancelada")
                elif choice == "8":
                    self.show_help()
                elif choice == "0":
                    print("👋 Até logo!")
                    break
                else:
                    print("❌ Opção inválida! Tente novamente.")
                
                if choice != "0":
                    input("\n⏸️ Pressione Enter para continuar...")
                    
            except KeyboardInterrupt:
                print("\n\n👋 Saindo...")
                break
            except Exception as e:
                print(f"❌ Erro: {e}")
                input("\n⏸️ Pressione Enter para continuar...")
    
    def show_help(self):
        """Mostra ajuda detalhada"""
        print("\n" + "="*60)
        print("📚 AJUDA - PROJETO-TP2")
        print("="*60)
        print("🔧 Configurar ambiente: Cria .venv e instala dependências")
        print("🚀 Iniciar servidor: Roda Flask em http://localhost:5000")
        print("🧪 Testes: Executa testes do banco e/ou requisições")
        print("📊 Status: Mostra informações do ambiente")
        print("🧹 Limpar: Remove .venv e arquivos temporários")
        print("\n📁 Estrutura do projeto:")
        print("   aplicação/app.py - Servidor principal")
        print("   aplicação/test/ - Testes unitários")
        print("   aplicação/modules/ - Módulos Python")
        print("   aplicação/static/ - CSS, JS, imagens")
        print("   aplicação/templates/ - Templates HTML")
        print("\n💡 Dicas:")
        print("   - Execute 'Configurar ambiente' primeiro")
        print("   - Para testes de requisições, inicie o servidor antes")
        print("   - Use Ctrl+C para parar o servidor")
        print("="*60)

def main():
    parser = argparse.ArgumentParser(description="Gerenciador do projeto Projeto-TP2")
    parser.add_argument("command", nargs='?', choices=["setup", "server", "test", "clean", "status", "menu"], 
                       help="Comando a ser executado")
    parser.add_argument("--test-type", choices=["all", "db", "requests"], default="all",
                       help="Tipo de teste a ser executado")
    
    args = parser.parse_args()
    
    manager = ProjectManager()
    
    # Se nenhum comando foi fornecido, abrir menu interativo
    if not args.command:
        manager.interactive_menu()
    elif args.command == "menu":
        manager.interactive_menu()
    elif args.command == "setup":
        manager.setup_venv()
    elif args.command == "server":
        manager.run_server()
    elif args.command == "test":
        manager.run_tests(args.test_type)
    elif args.command == "clean":
        manager.clean()
    elif args.command == "status":
        manager.status()

if __name__ == "__main__":
    main()
