# 🚀 JackCompiler - UFMA 2026.1

![Python Version](https://img.shields.io/badge/python-3.13%2B-blue)
![Build Status](https://img.shields.io/badge/build-passing-brightgreen)

Projeto desenvolvido para a disciplina de **Compiladores** da Universidade Federal do Maranhão (UFMA). O objetivo é construir um compilador completo para a linguagem **Jack**, conforme especificado no curso *Nand2Tetris*.

---

## 👥 Integrantes
| Nome | Matrícula |
| :--- | :--- |
| **Anderson Almeida da Silveira** | 20240065590 |
| **Jeysraelly Almone da Silva** | 20250071222 |

---

## 🛠️ Tecnologias Utilizadas
* **Linguagem:** Python 3.13
* **Gerenciador de Pacotes:** `uv`
* **Framework de Testes:** `pytest`

---

### ⚙️ Instalação e Configuração

Siga os passos abaixo para preparar o ambiente de desenvolvimento:

1. **Clonar o repositório:**
   ```bash
   git clone https://github.com/andersonpog/jack-compiler.git
   cd jack-compiler
   ```

2. **Criar o Ambiente Virtual (.venv):**
   O `uv` gerencia o ambiente virtual de forma otimizada. Para criar e configurar a versão correta do Python, execute:
   ```bash
   uv venv
   ```

3. **Ativar o Ambiente Virtual:**
   Dependendo do seu sistema operacional, o comando de ativação muda:
    **Windows (PowerShell):**
     ```powershell
     .venv\Scripts\Activate.ps1
     ```
    **Linux / macOS:**
     ```bash
     source .venv/bin/activate
     ```

4. **Instalar Dependências:**
   Com o ambiente ativo, instale os pacotes necessários:
   ```bash
   uv pip install -r requirements.txt
   ```


---

## 🚀 Como Executar

O compilador processa arquivos `.jack` e gera as respectivas análises em formato XML.

```bash
# Sintaxe: python main.py <nome_do_arquivo_sem_extensao>
python main.py teste
```

### 📂 Saída Esperada
Ao executar o comando acima para um arquivo chamado `teste.jack`, o compilador gerará na mesma pasta:
* `testeT.xml`: Resultado da **Análise Léxica** (Tokens).
* `teste.xml`: Resultado da **Análise Sintática** (Parse Tree).

---

## 🧪 Executando os Testes

Para garantir que o compilador está seguindo as regras gramaticais e gerando o XML corretamente, execute a suíte de testes:

```bash
# Rodar todos os testes de forma detalhada
pytest tests/ -v

# Rodar testes específicos de um módulo
pytest tests/test_scanner.py -y
# Ou
pytest tests/test_parser.py -v
```

---

## 🏛️ Estrutura do Projeto
* `jack_tokenizer.py`: Responsável por quebrar o código em tokens.
* `TokenToXML.py` : Transforma a lista de tokens em um XML.
* `parser.py`: Realiza a análise sintática recursiva e gera o XML.
* `main.py`: Ponto de entrada do aplicativo.
* `tests/`: Pasta contendo os gabaritos e scripts de teste.


