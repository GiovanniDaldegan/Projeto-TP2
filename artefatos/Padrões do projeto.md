## Estrutura do projeto

```
Projeto-TP2
│
├── README.md
├── LEIAME.txt
├── LICENSE
├── Doxyfile
│
├── aplicação/
│   │
│   ├── app.py                  # setup da aplicação (servidor)
│   │
│   ├── templates/              # páginas HTML fornecidas pelo servidor
│   │
│   ├── static/                 # elementos do cliente que serão requisitados
│   │   │                       # (códigos, imagens, etc.)
│   │   ├── style.css
│   │   │
│   │   ├── scripts/
│   │   ├── img/
│   │   └── fonts/
│   │
│   ├── modules/                # módulos do servidor
│   │
│   └── test/                   # módulos de teste do servidor
│
└── artefatos/
    │
    ├── Especificação.pdf
    ├── Padrões do projeto.md   # padrões utilizados
    │
    ├── diagramas/
    │
    ├── revisões/               # laudos de revisão
    │
    └── docs/                   # documentação Doxygen
```


## Desenvolvimento web com SocketIO

Os clientes e o servidor se comunicam através de objetos SocketIO
(Flask-SocketIO no servidor, SocketIO em JS nos clientes), que permitem enviar
eventos customizados e objetos e receber esses eventos por listeners para se
comunicar.

Para enviar um evento  um objeto (precisa ser serializável para JSON):
```py
socketio.emit("evento-customizado", {
  "search_term"   : "Miojo",
  "filters"       : ["Construção", "Comida instantânea"]
})
```


Em Python, o servidor precisa de um listener assim para receber o evento
```py
@socketio.on("evento-customizado")
def funcao_do_evento(data):
    # processar o evento
```

Em JavaScript, o cliente recebe o evento com
```js
socketio.on("evento-customizado", (product_list) => {
    // proessar o evento
});
```


### Frontend
O índice da aplicação (`templates/index.html`) precisa importar esse script do
SocketIO:
https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.0.1/socket.io.js

Todo arquivo (imagem, estilo CSS, até os scripts JS usados na página) que o
front precisar ele precisa fazer uma requisição ao servidor usando a função
`url_for()`. Todos esses arquivos, incluindo todos os scripts do cliente, devem
ficar na pasta `static` (cada um na sua devida sub-pasta).

Exemplo:
```html
<script src="{{ url_for('static', filename='scripts/index.js') }}"><script/>
```

### Backend
O índice da aplicação fica na pasta "templates" e deve ter uma rota definida
para o Flask, da seguinte forma:

```py
@app.route("/")
def index():
    return render_template("index.html")
```

Cada módulo do servidor deve estar na pasta "modules" e ser devidamente
importado pelo app.py.

- Se for um módulo interno e essencial no setup da aplicação, como o módulo de
  BD, deve ser inicializado **antes dos listeners**

- Se for um módulo com listeners, deve ser importado depois da criação do
  socketio.



## Formatação e documentação de código (apenas Python)

Diretórios:   `kebab-case` <br>
Arquivos:     `snake_case` <br>
<br>
Formatação e estilo (PEP8): <br>
Módulos:      `snake_case` <br>
Classes:      `PascalCase` <br>
Funções:      `snake_case` <br>
Variáveis:    `snake_case` <br>
Constantes:   `SCREAMING_SNAKE_CASE`


#### Cabeçalho de módulo
```py
"""! @package nome_modulo
    Descrição breve.

    Descrição detalhada
"""
```

#### Cabeçalho de classe
```py
class ProductList:
    """! Descrição breve.

    Descrição detalhada.
    """
```

#### Cabeçalhos de função
```py
def nome_funcao(arg0, arg1):
    """! Descrição breve

    Descrição detalhada.

    @param  arg0  Descrição parâmetro 0.
    @param  arg1  Descrição parâmetro 1.

    @return  var_retorno  Variável de retorno.

    Assertivas de entrada
      - condicao0
    Assertivas de saída
      - condicao1
      - condicao2
    """
```

Exemplos:
```py
def ListProducts(nome, filtros):
    """! Envia para o cliente uma lista de os produtos cadastrados.
    
    @param  nome     Nome pesquisado.
    @param  filtros  Filtros aplicados.
    """
```
```py
def __init__(self):
    """! Construtor da classe"""
```

### Assertivas de entrada e saída

(condição)

Exs.:
- !GetAccount()
- len(productList) >= 0
- key é uma chave válida.   # pode ser que precise ser mais descritiva



# Laudos de revisão



# Relatórios
```
DATA        | HORAS |  TIPO TAREFA   |  DESCRIÇÃO DA TAREFA REALIZADA
AAAA.MM.DD  |  HHh  |  tipo          |  descrição
```

Exemplo:
```
DATA        | HORAS |  TIPO TAREFA             |  DESCRIÇÃO DA TAREFA REALIZADA
2025.06.17  |  02h  |  revisar especificações  |  função de pesquisar produtos não precisa de
            |       |                          |  adivinhar nomes escrito errado
            |       |                          |  
            |  01h  |  fazer diagramas         |  modelar o subsistema de pesquisa de produto
            |       |                          |  
2025.06.18  |  10h  |  revisar projetos        |  paradas
```

Tipos de tarefa:
  - Geral
    - estudar aulas e laboratórios relacionados
    - gerenciar a construção do software

  - Modelagem e especificação
    - projetar
    - revisar projetos
    - fazer diagramas
    - especificar os módulos
    - especificar as funções
    - revisar especificações

  - Implementação
    - codificar módulo
    - revisar código do módulo
    - rodar o verificador estático e retirar warnings

  - Testes
    - redigir casos de teste
    - revisar casos de teste
    - realizar os testes

  - Cobertura e documentação
    - instrumentar verificando a cobertura
    - documentar com Doxygen



## Especificação e descrição do projeto

"Estórias" de usuário (EUs):
- perspectiva do usuário
- numeradas no formato EU001

Diagramas de caso de uso
- detalham ações do usuário e respostas do sistema a ele
- `<<include>>`: casos de uso utilizados
- `<<extends>>`: casos de uso englobados
- interfaces: interfaces utilizadas

Detalhamento de cada caso de uso
- nome, tipo (primário, secundário, opcional), descrição
- atores
- referências (EUs)
- pré-condições: assertivas prévias ao caso de uso
- fluxo de eventos:
  - principal (típico),
  - alternativos (esperado mas variante do típico),
  - atípicos (erros, cancelamento pelo usuário, etc.)
- pós-condições: assertivas posteriores ao caso de uso
- pontos de extensão: casos de uso que que são englobados pelo caso de uso em
  questão
- casos de uso incluídos: casos de uso utilizados `<<include>>`
- outros requisitos (interfaces)
- ações do ator VS resposta do sistema (colunas separadas)

Diagramas de fluxo de dados (DFD)
- entidades externas (retângulo): podem ser duplicados para evitar cruzamento de
  linhas
- fluxo de dados (setas unilaterais com nome do dado): contém só um tipo de dado
- armazenamento de dados (retângulo com lado direito aberto)
- processos (elipses ou retangulos arredondados):
  - precisam de um fluxo de dados chegando e outro saindo
  - nomeados como "`<verbo> <objeto>`", "Valida ingresso"
