-- Estrutura do banco de dados (SQLite)
CREATE TABLE IF NOT EXISTS tarefas (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo      TEXT    NOT NULL,
    descricao   TEXT    NOT NULL DEFAULT '',
    prioridade  TEXT    NOT NULL DEFAULT 'media'
                CHECK (prioridade IN ('baixa', 'media', 'alta')),
    concluida   INTEGER NOT NULL DEFAULT 0 CHECK (concluida IN (0, 1)),
    criada_em   TEXT    NOT NULL DEFAULT (datetime('now', 'localtime'))
);
