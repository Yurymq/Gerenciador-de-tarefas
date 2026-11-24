"""Interface de linha de comando."""
import argparse
import sys

from .db import PRIORIDADES, RepositorioTarefas


def _imprimir(tarefas):
    if not tarefas:
        print("Nenhuma tarefa encontrada. Use 'adicionar' para criar a primeira.")
        return
    print(f"{'ID':>3}  {'OK':<3}  {'PRIORIDADE':<10}  TÍTULO")
    for t in tarefas:
        marca = "x" if t["concluida"] else " "
        print(f"{t['id']:>3}  [{marca}]  {t['prioridade']:<10}  {t['titulo']}")
        if t["descricao"]:
            print(f"{'':>21}{t['descricao']}")


def criar_parser():
    parser = argparse.ArgumentParser(
        prog="tarefas", description="Gerenciador de tarefas no terminal."
    )
    parser.add_argument("--banco", default="tarefas.db", help="arquivo do banco SQLite")
    sub = parser.add_subparsers(dest="comando", required=True)

    add = sub.add_parser("adicionar", help="cria uma tarefa")
    add.add_argument("titulo")
    add.add_argument("-d", "--descricao", default="")
    add.add_argument("-p", "--prioridade", choices=PRIORIDADES, default="media")

    lst = sub.add_parser("listar", help="mostra as tarefas")
    lst.add_argument("--pendentes", action="store_true", help="oculta as concluídas")
    lst.add_argument("-p", "--prioridade", choices=PRIORIDADES)

    bus = sub.add_parser("buscar", help="procura por texto")
    bus.add_argument("termo")

    con = sub.add_parser("concluir", help="marca como concluída")
    con.add_argument("id", type=int)

    rem = sub.add_parser("remover", help="apaga uma tarefa")
    rem.add_argument("id", type=int)
    return parser


def main(argv=None):
    args = criar_parser().parse_args(argv)
    repo = RepositorioTarefas(args.banco)
    try:
        if args.comando == "adicionar":
            novo_id = repo.adicionar(args.titulo, args.descricao, args.prioridade)
            print(f"Tarefa {novo_id} criada.")
        elif args.comando == "listar":
            _imprimir(repo.listar(args.pendentes, args.prioridade))
        elif args.comando == "buscar":
            _imprimir(repo.buscar(args.termo))
        elif args.comando == "concluir":
            ok = repo.concluir(args.id)
            print("Tarefa concluída." if ok else f"Não existe tarefa com id {args.id}.")
            return 0 if ok else 1
        elif args.comando == "remover":
            ok = repo.remover(args.id)
            print("Tarefa removida." if ok else f"Não existe tarefa com id {args.id}.")
            return 0 if ok else 1
    except ValueError as erro:
        print(f"Erro: {erro}", file=sys.stderr)
        return 1
    finally:
        repo.fechar()
    return 0
