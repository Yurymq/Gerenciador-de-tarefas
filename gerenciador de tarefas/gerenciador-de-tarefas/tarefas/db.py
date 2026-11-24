"""Camada de acesso ao banco de dados."""
import sqlite3
from pathlib import Path

PRIORIDADES = ("baixa", "media", "alta")
_SCHEMA = Path(__file__).with_name("schema.sql")


class RepositorioTarefas:
    """Cria, consulta e atualiza tarefas em um banco SQLite."""

    def __init__(self, caminho="tarefas.db"):
        self.conn = sqlite3.connect(caminho)
        self.conn.row_factory = sqlite3.Row
        self.conn.executescript(_SCHEMA.read_text(encoding="utf-8"))

    def adicionar(self, titulo, descricao="", prioridade="media"):
        """Insere uma tarefa e devolve o id criado."""
        titulo = (titulo or "").strip()
        if not titulo:
            raise ValueError("O título não pode ficar vazio.")
        if prioridade not in PRIORIDADES:
            raise ValueError(
                f"Prioridade inválida. Use: {', '.join(PRIORIDADES)}."
            )
        cursor = self.conn.execute(
            "INSERT INTO tarefas (titulo, descricao, prioridade) VALUES (?, ?, ?)",
            (titulo, descricao.strip(), prioridade),
        )
        self.conn.commit()
        return cursor.lastrowid

    def listar(self, apenas_pendentes=False, prioridade=None):
        """Lista tarefas: pendentes primeiro e, dentro delas, as mais urgentes."""
        consulta = "SELECT * FROM tarefas WHERE 1=1"
        parametros = []
        if apenas_pendentes:
            consulta += " AND concluida = 0"
        if prioridade:
            consulta += " AND prioridade = ?"
            parametros.append(prioridade)
        consulta += (
            " ORDER BY concluida,"
            " CASE prioridade WHEN 'alta' THEN 0 WHEN 'media' THEN 1 ELSE 2 END,"
            " id"
        )
        return self.conn.execute(consulta, parametros).fetchall()

    def buscar(self, termo):
        """Procura o termo no título ou na descrição."""
        padrao = f"%{termo}%"
        return self.conn.execute(
            "SELECT * FROM tarefas WHERE titulo LIKE ? OR descricao LIKE ? ORDER BY id",
            (padrao, padrao),
        ).fetchall()

    def concluir(self, id_tarefa):
        """Marca como concluída. Devolve False se o id não existir."""
        cursor = self.conn.execute(
            "UPDATE tarefas SET concluida = 1 WHERE id = ?", (id_tarefa,)
        )
        self.conn.commit()
        return cursor.rowcount > 0

    def remover(self, id_tarefa):
        """Apaga a tarefa. Devolve False se o id não existir."""
        cursor = self.conn.execute("DELETE FROM tarefas WHERE id = ?", (id_tarefa,))
        self.conn.commit()
        return cursor.rowcount > 0

    def fechar(self):
        self.conn.close()
