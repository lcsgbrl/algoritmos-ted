"""
testes.py — Testes unitários para GrafoRedeSocial
Execute com: python -m pytest testes.py -v
"""

import pytest
from src.grafo import GrafoRedeSocial


@pytest.fixture
def rede_simples():
    """Fixture: grafo básico para todos os testes."""
    g = GrafoRedeSocial()
    for nome in ["Ana", "Bruno", "Carla", "Diego", "Eva"]:
        g.adicionar_pessoa(nome)
    g.adicionar_amizade("Ana", "Bruno")
    g.adicionar_amizade("Ana", "Carla")
    g.adicionar_amizade("Bruno", "Diego")
    g.adicionar_amizade("Carla", "Diego")
    # Eva está isolada (sem amigos)
    return g


class TestVerticosArestas:
    def test_adicionar_pessoa(self, rede_simples):
        assert "Ana" in rede_simples.adjacencia

    def test_nao_duplica_pessoa(self, rede_simples):
        total_antes = len(rede_simples.adjacencia)
        rede_simples.adicionar_pessoa("Ana")
        assert len(rede_simples.adjacencia) == total_antes

    def test_amizade_bidirecional(self, rede_simples):
        assert rede_simples.sao_amigos("Ana", "Bruno")
        assert rede_simples.sao_amigos("Bruno", "Ana")

    def test_sem_auto_loop(self, rede_simples):
        rede_simples.adicionar_amizade("Ana", "Ana")
        assert not rede_simples.sao_amigos("Ana", "Ana")

    def test_remover_amizade(self, rede_simples):
        rede_simples.remover_amizade("Ana", "Bruno")
        assert not rede_simples.sao_amigos("Ana", "Bruno")
        assert not rede_simples.sao_amigos("Bruno", "Ana")

    def test_remover_pessoa_remove_arestas(self, rede_simples):
        rede_simples.remover_pessoa("Ana")
        assert "Ana" not in rede_simples.adjacencia
        assert "Ana" not in rede_simples.adjacencia.get("Bruno", set())
        assert "Ana" not in rede_simples.adjacencia.get("Carla", set())


class TestConsultas:
    def test_amigos_de(self, rede_simples):
        assert rede_simples.amigos_de("Ana") == {"Bruno", "Carla"}

    def test_amigos_em_comum(self, rede_simples):
        comum = rede_simples.amigos_em_comum("Ana", "Diego")
        assert comum == {"Bruno", "Carla"}

    def test_grau(self, rede_simples):
        assert rede_simples.grau("Ana") == 2
        assert rede_simples.grau("Diego") == 2

    def test_grau_isolado(self, rede_simples):
        assert rede_simples.grau("Eva") == 0

    def test_mais_popular(self, rede_simples):
        # Ana, Bruno, Carla e Diego têm grau 2; Eva tem 0
        pessoa, grau = rede_simples.pessoa_mais_popular()
        assert grau == 2


class TestBFS:
    def test_distancias_bfs(self, rede_simples):
        dist = rede_simples.bfs("Ana")
        assert dist["Ana"] == 0
        assert dist["Bruno"] == 1
        assert dist["Carla"] == 1
        assert dist["Diego"] == 2

    def test_bfs_nao_alcanca_isolado(self, rede_simples):
        dist = rede_simples.bfs("Ana")
        assert "Eva" not in dist  # Eva está isolada

    def test_caminho_mais_curto(self, rede_simples):
        caminho = rede_simples.caminho_mais_curto("Ana", "Diego")
        assert caminho[0] == "Ana"
        assert caminho[-1] == "Diego"
        assert len(caminho) == 3  # Ana → Bruno/Carla → Diego

    def test_caminho_mesmo_vertice(self, rede_simples):
        assert rede_simples.caminho_mais_curto("Ana", "Ana") == ["Ana"]

    def test_sem_caminho_vertice_isolado(self, rede_simples):
        caminho = rede_simples.caminho_mais_curto("Ana", "Eva")
        assert caminho == []


class TestConexidade:
    def test_componentes_desconexos(self, rede_simples):
        comps = rede_simples.componentes_conexos()
        assert len(comps) == 2  # {Ana,Bruno,Carla,Diego} e {Eva}

    def test_grafo_nao_conexo(self, rede_simples):
        assert not rede_simples.esta_conectado()

    def test_grafo_conexo_apos_unir(self, rede_simples):
        rede_simples.adicionar_amizade("Ana", "Eva")
        assert rede_simples.esta_conectado()
