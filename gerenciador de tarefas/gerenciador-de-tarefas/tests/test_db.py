import unittest

from tarefas import RepositorioTarefas


class TestRepositorioTarefas(unittest.TestCase):
    def setUp(self):
        # Banco em memória: cada teste começa do zero
        self.repo = RepositorioTarefas(":memory:")

    def tearDown(self):
        self.repo.fechar()

    def test_adicionar_e_listar(self):
        id_criado = self.repo.adicionar("Estudar SQL", "Revisar JOINs", "alta")
        tarefas = self.repo.listar()
        self.assertEqual(len(tarefas), 1)
        self.assertEqual(tarefas[0]["id"], id_criado)
        self.assertEqual(tarefas[0]["prioridade"], "alta")
        self.assertEqual(tarefas[0]["concluida"], 0)

    def test_titulo_vazio_gera_erro(self):
        with self.assertRaises(ValueError):
            self.repo.adicionar("   ")

    def test_prioridade_invalida_gera_erro(self):
        with self.assertRaises(ValueError):
            self.repo.adicionar("Teste", prioridade="urgentissima")

    def test_concluir(self):
        id_criado = self.repo.adicionar("Fazer commit")
        self.assertTrue(self.repo.concluir(id_criado))
        self.assertEqual(self.repo.listar()[0]["concluida"], 1)
        self.assertEqual(self.repo.listar(apenas_pendentes=True), [])

    def test_concluir_id_inexistente(self):
        self.assertFalse(self.repo.concluir(999))

    def test_remover(self):
        id_criado = self.repo.adicionar("Apagar depois")
        self.assertTrue(self.repo.remover(id_criado))
        self.assertEqual(self.repo.listar(), [])
        self.assertFalse(self.repo.remover(id_criado))

    def test_ordem_pendentes_e_prioridade(self):
        self.repo.adicionar("baixa", prioridade="baixa")
        id_alta = self.repo.adicionar("alta", prioridade="alta")
        id_feita = self.repo.adicionar("feita", prioridade="alta")
        self.repo.concluir(id_feita)
        titulos = [t["titulo"] for t in self.repo.listar()]
        self.assertEqual(titulos, ["alta", "baixa", "feita"])
        self.assertEqual(self.repo.listar()[0]["id"], id_alta)

    def test_buscar_por_titulo_e_descricao(self):
        self.repo.adicionar("Estudar Python", "listas e dicionários")
        self.repo.adicionar("Lavar o carro")
        self.assertEqual(len(self.repo.buscar("python")), 1)
        self.assertEqual(len(self.repo.buscar("dicionários")), 1)
        self.assertEqual(len(self.repo.buscar("xyz")), 0)


if __name__ == "__main__":
    unittest.main()
