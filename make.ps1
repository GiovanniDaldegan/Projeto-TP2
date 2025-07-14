param (
    [string]$target = "help"
)

$VENV = ".venv"
$APP_DIR = "aplicacao"  # Mantenha sem acentos!

function Invoke-Format {
    if (-Not (Test-Path $APP_DIR)) {
        Write-Host "Erro: Diretorio '$APP_DIR' nao encontrado!" -ForegroundColor Red
        exit 1
    }
    & ".\$VENV\Scripts\python.exe" -m black $APP_DIR  # Note o & e .exe
}

function Invoke-Setup {
    python -m venv $VENV
    & ".\$VENV\Scripts\Activate.ps1"  # Ativação correta
    pip install -r requirements.txt
}