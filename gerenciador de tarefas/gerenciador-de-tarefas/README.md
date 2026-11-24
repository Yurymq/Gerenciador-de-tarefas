# Gerenciador de Tarefas (Python + SQLite)

Aplicação de linha de comando para organizar tarefas, feita em **Python** com banco de dados **SQLite**. Cada tarefa tem título, descrição, prioridade (baixa, média ou alta) e status (pendente ou concluída).

O projeto separa as responsabilidades em camadas (banco de dados, interface de linha de comando e testes) e usa apenas a biblioteca padrão do Python, sem dependências externas.

## O que o projeto faz

- Cria, lista, busca, conclui e remove tarefas
- Ordena a lista mostrando primeiro as pendentes e, entre elas, as de maior prioridade
- Valida os dados (título vazio e prioridade inválida geram erro claro)
- Usa consultas SQL parametrizadas (`?`), evitando SQL injection
- Possui testes automatizados com `unittest`

## Tecnologias

- Python 3.8 ou superior
- SQLite (módulo `sqlite3`, já vem com o Python)
- `argparse` para a interface de linha de comando
- `unittest` para os testes

## Como executar

```bash
git clone https://github.com/Yurymq/gerenciador-de-tarefas.git
cd gerenciador-de-tarefas
```

Criar tarefas:

```bash
python main.py adicionar "Estudar SQL" -d "Revisar JOINs" -p alta
python main.py adicionar "Subir projeto no GitHub"
```

Listar, buscar, concluir e remover:

```bash
python main.py listar
python main.py listar --pendentes
python main.py listar -p alta
python main.py buscar sql
python main.py concluir 1
python main.py remover 2
```

Exemplo de saída do comando `listar`:

```
 ID  OK   PRIORIDADE  TÍTULO
  1  [ ]  alta        Estudar SQL
                     Revisar JOINs
  2  [x]  media       Subir projeto no GitHub
```

O banco é salvo no arquivo `tarefas.db`. Para usar outro arquivo, passe `--banco meu_banco.db` antes do comando.

## Como rodar os testes

```bash
python -m unittest -v
```

Os testes usam um banco em memória (`:memory:`), então não alteram seus dados reais.

## Estrutura do projeto

```
gerenciador-de-tarefas/
├── main.py              # ponto de entrada
├── tarefas/
│   ├── __init__.py
│   ├── cli.py           # comandos e saída no terminal
│   ├── db.py            # acesso ao banco (CRUD)
│   └── schema.sql       # estrutura da tabela
└── tests/
    └── test_db.py       # testes automatizados
```

## Banco de dados

```sql
CREATE TABLE tarefas (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo      TEXT    NOT NULL,
    descricao   TEXT    NOT NULL DEFAULT '',
    prioridade  TEXT    NOT NULL DEFAULT 'media'
                CHECK (prioridade IN ('baixa', 'media', 'alta')),
    concluida   INTEGER NOT NULL DEFAULT 0 CHECK (concluida IN (0, 1)),
    criada_em   TEXT    NOT NULL DEFAULT (datetime('now', 'localtime'))
);
```

## Próximos passos

- [ ] Adicionar data limite nas tarefas
- [ ] Editar o título e a descrição de uma tarefa
- [ ] Trocar o SQLite por MySQL
- [ ] Expor as funções como uma API REST

## Autor

**Yury Mendonça**, estudante de Engenharia de Software (UGB)
[GitHub](https://github.com/Yurymq) · yurymendonca88@gmail.com

## Licença

MIT. Veja o arquivo `LICENSE`.
