"""
Rede de Contatos - Grafo Não-Direcionado e Não-Ponderado
Disciplina: Estrutura de Dados - Grafos
Autores: Alexandre Amorim, Emerson Castro, Marcos Yan
"""

from collections import deque


class GrafoRedeSocial:
    """
    Representação de uma rede social usando grafo não-direcionado
    com lista de adjacência.

    - Não-direcionado: se A conhece B, então B conhece A
    - Não-ponderado: todas as conexões têm o mesmo peso (amizade)
    - Lista de adjacência: estrutura eficiente para grafos esparsos
    """

    def __init__(self):
        # Dicionário: chave = pessoa, valor = conjunto de amigos
        self.adjacencia = {}

    # ------------------------------------------------------------------ #
    #  Operações básicas                                                   #
    # ------------------------------------------------------------------ #

    def adicionar_pessoa(self, nome: str) -> None:
        """Adiciona um vértice (pessoa) ao grafo."""
        if nome not in self.adjacencia:
            self.adjacencia[nome] = set()
            print(f"  ✔ Pessoa '{nome}' adicionada.")
        else:
            print(f"  ! '{nome}' já está na rede.")

    def remover_pessoa(self, nome: str) -> None:
        """Remove um vértice e todas as suas arestas."""
        if nome not in self.adjacencia:
            print(f"  ! '{nome}' não encontrado na rede.")
            return
        # Remove as referências nos outros vértices
        for amigo in self.adjacencia[nome]:
            self.adjacencia[amigo].discard(nome)
        del self.adjacencia[nome]
        print(f"  ✔ Pessoa '{nome}' removida da rede.")

    def adicionar_amizade(self, pessoa1: str, pessoa2: str) -> None:
        """Adiciona uma aresta (amizade) entre dois vértices."""
        if pessoa1 == pessoa2:
            print("  ! Uma pessoa não pode ser amiga de si mesma.")
            return
        for p in [pessoa1, pessoa2]:
            if p not in self.adjacencia:
                self.adicionar_pessoa(p)
        self.adjacencia[pessoa1].add(pessoa2)
        self.adjacencia[pessoa2].add(pessoa1)  # grafo não-direcionado!
        print(f"  ✔ Amizade criada: {pessoa1} ↔ {pessoa2}")

    def remover_amizade(self, pessoa1: str, pessoa2: str) -> None:
        """Remove uma aresta (amizade) entre dois vértices."""
        if pessoa1 not in self.adjacencia or pessoa2 not in self.adjacencia:
            print("  ! Uma ou ambas as pessoas não existem na rede.")
            return
        self.adjacencia[pessoa1].discard(pessoa2)
        self.adjacencia[pessoa2].discard(pessoa1)
        print(f"  ✔ Amizade removida: {pessoa1} ↮ {pessoa2}")

    def sao_amigos(self, pessoa1: str, pessoa2: str) -> bool:
        """Verifica se existe aresta entre dois vértices."""
        if pessoa1 not in self.adjacencia:
            return False
        return pessoa2 in self.adjacencia[pessoa1]

    # ------------------------------------------------------------------ #
    #  Consultas                                                           #
    # ------------------------------------------------------------------ #

    def amigos_de(self, nome: str) -> set:
        """Retorna o conjunto de vizinhos (amigos diretos) de um vértice."""
        if nome not in self.adjacencia:
            print(f"  ! '{nome}' não encontrado.")
            return set()
        return self.adjacencia[nome].copy()

    def amigos_em_comum(self, pessoa1: str, pessoa2: str) -> set:
        """Retorna a interseção dos vizinhos de dois vértices."""
        a1 = self.amigos_de(pessoa1)
        a2 = self.amigos_de(pessoa2)
        return a1 & a2

    def grau(self, nome: str) -> int:
        """Retorna o grau do vértice (nº de arestas que partem dele)."""
        if nome not in self.adjacencia:
            return 0
        return len(self.adjacencia[nome])

    def pessoa_mais_popular(self) -> tuple[str, int]:
        """Retorna o vértice de maior grau (mais conexões)."""
        if not self.adjacencia:
            return ("", 0)
        pessoa = max(self.adjacencia, key=lambda p: len(self.adjacencia[p]))
        return (pessoa, self.grau(pessoa))

    # ------------------------------------------------------------------ #
    #  Busca em largura (BFS) — encontra caminho mais curto               #
    # ------------------------------------------------------------------ #

    def bfs(self, origem: str) -> dict:
        """
        Busca em largura a partir de uma origem.
        Retorna dicionário com a distância (nº de conexões) até cada pessoa.
        """
        if origem not in self.adjacencia:
            print(f"  ! '{origem}' não encontrado.")
            return {}

        visitados = {origem: 0}
        fila = deque([origem])

        while fila:
            atual = fila.popleft()
            for vizinho in self.adjacencia[atual]:
                if vizinho not in visitados:
                    visitados[vizinho] = visitados[atual] + 1
                    fila.append(vizinho)

        return visitados

    def caminho_mais_curto(self, origem: str, destino: str) -> list:
        """
        Retorna o caminho mais curto (menor número de conexões)
        entre origem e destino usando BFS com rastreamento de predecessores.
        """
        if origem not in self.adjacencia or destino not in self.adjacencia:
            return []
        if origem == destino:
            return [origem]

        predecessores = {origem: None}
        fila = deque([origem])

        while fila:
            atual = fila.popleft()
            if atual == destino:
                break
            for vizinho in self.adjacencia[atual]:
                if vizinho not in predecessores:
                    predecessores[vizinho] = atual
                    fila.append(vizinho)

        if destino not in predecessores:
            return []  # Sem conexão (grafo desconexo)

        # Reconstrói o caminho
        caminho = []
        no = destino
        while no is not None:
            caminho.append(no)
            no = predecessores[no]
        return list(reversed(caminho))

    # ------------------------------------------------------------------ #
    #  Busca em profundidade (DFS) — detecta componentes conexos          #
    # ------------------------------------------------------------------ #

    def _dfs_recursivo(self, vertice: str, visitados: set) -> None:
        visitados.add(vertice)
        for vizinho in self.adjacencia[vertice]:
            if vizinho not in visitados:
                self._dfs_recursivo(vizinho, visitados)

    def componentes_conexos(self) -> list[set]:
        """
        Retorna lista de componentes conexos (grupos isolados de amigos).
        Um componente conexo = grupo onde todos estão conectados entre si
        (direta ou indiretamente).
        """
        visitados = set()
        componentes = []
        for pessoa in self.adjacencia:
            if pessoa not in visitados:
                grupo = set()
                self._dfs_recursivo(pessoa, grupo)
                componentes.append(grupo)
                visitados.update(grupo)
        return componentes

    def esta_conectado(self) -> bool:
        """Verifica se o grafo é conexo (todos alcançam todos)."""
        return len(self.componentes_conexos()) <= 1

    # ------------------------------------------------------------------ #
    #  Exibição                                                            #
    # ------------------------------------------------------------------ #

    def exibir_lista_adjacencia(self) -> None:
        """Imprime a lista de adjacência completa."""
        print("\n╔══════════════════════════════════════╗")
        print("║       LISTA DE ADJACÊNCIA            ║")
        print("╚══════════════════════════════════════╝")
        if not self.adjacencia:
            print("  (rede vazia)")
            return
        for pessoa in sorted(self.adjacencia):
            amigos = sorted(self.adjacencia[pessoa])
            conexoes = " → ".join(amigos) if amigos else "(sem amigos)"
            print(f"  {pessoa:<20} │ {conexoes}")

    def estatisticas(self) -> None:
        """Exibe um resumo estatístico do grafo."""
        n_vertices = len(self.adjacencia)
        # Em grafo não-direcionado, cada aresta é contada 2x na lista
        n_arestas = sum(len(v) for v in self.adjacencia.values()) // 2
        comps = self.componentes_conexos()
        popular, grau_max = self.pessoa_mais_popular()

        print("\n╔══════════════════════════════════════╗")
        print("║           ESTATÍSTICAS               ║")
        print("╚══════════════════════════════════════╝")
        print(f"  Pessoas (vértices) : {n_vertices}")
        print(f"  Amizades (arestas) : {n_arestas}")
        print(f"  Componentes conexos: {len(comps)}")
        print(f"  Grafo conectado?   : {'Sim' if len(comps) <= 1 else 'Não'}")
        if popular:
            print(f"  Mais popular       : {popular} ({grau_max} amigos)")
