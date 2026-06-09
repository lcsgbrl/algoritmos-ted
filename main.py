"""
main.py — Demonstração completa da Rede de Contatos
Executa todas as operações do grafo com saída detalhada.
"""

from src.grafo import GrafoRedeSocial


def separador(titulo: str) -> None:
    print(f"\n{'─' * 50}")
    print(f"  {titulo}")
    print(f"{'─' * 50}")


def main():
    print("=" * 52)
    print("   REDE DE CONTATOS — GRAFO NÃO-DIRECIONADO")
    print("   Estrutura de Dados · Grafos")
    print("=" * 52)

    rede = GrafoRedeSocial()

    # ------------------------------------------------------------------ #
    #  1. Adicionando pessoas                                              #
    # ------------------------------------------------------------------ #
    separador("1. ADICIONANDO PESSOAS (vértices)")
    for nome in ["Alexandre", "Emerson", "Marcos", "Patricia",
                 "Bruno", "Carla", "Diego"]:
        rede.adicionar_pessoa(nome)

    # ------------------------------------------------------------------ #
    #  2. Criando amizades                                                 #
    # ------------------------------------------------------------------ #
    separador("2. CRIANDO AMIZADES (arestas)")
    amizades = [
        ("Alexandre", "Emerson"),
        ("Alexandre", "Marcos"),
        ("Alexandre", "Patricia"),
        ("Emerson",   "Marcos"),
        ("Emerson",   "Bruno"),
        ("Marcos",    "Carla"),
        ("Patricia",  "Diego"),
        ("Bruno",     "Carla"),
    ]
    for p1, p2 in amizades:
        rede.adicionar_amizade(p1, p2)

    # ------------------------------------------------------------------ #
    #  3. Lista de adjacência                                              #
    # ------------------------------------------------------------------ #
    rede.exibir_lista_adjacencia()

    # ------------------------------------------------------------------ #
    #  4. Consultas básicas                                                #
    # ------------------------------------------------------------------ #
    separador("3. CONSULTAS BÁSICAS")

    print("\n  Amigos de Alexandre:")
    print(f"  → {rede.amigos_de('Alexandre')}")

    print("\n  Alexandre e Emerson são amigos?", rede.sao_amigos("Alexandre", "Emerson"))
    print("  Alexandre e Diego são amigos?  ", rede.sao_amigos("Alexandre", "Diego"))

    print("\n  Amigos em comum (Alexandre e Emerson):")
    print(f"  → {rede.amigos_em_comum('Alexandre', 'Emerson')}")

    print("\n  Amigos em comum (Alexandre e Bruno):")
    print(f"  → {rede.amigos_em_comum('Alexandre', 'Bruno')}")

    # ------------------------------------------------------------------ #
    #  5. BFS — Busca em largura                                           #
    # ------------------------------------------------------------------ #
    separador("4. BFS — DISTÂNCIAS A PARTIR DE ALEXANDRE")
    distancias = rede.bfs("Alexandre")
    for pessoa in sorted(distancias, key=distancias.get):
        graus = distancias[pessoa]
        barra = "●" * graus + "○" * (4 - graus)
        print(f"  {pessoa:<15} {barra}  {graus} conexão(ões)")

    # ------------------------------------------------------------------ #
    #  6. Caminho mais curto                                               #
    # ------------------------------------------------------------------ #
    separador("5. CAMINHO MAIS CURTO")

    pares = [
        ("Alexandre", "Diego"),
        ("Emerson", "Carla"),
        ("Alexandre", "Bruno"),
    ]
    for origem, destino in pares:
        caminho = rede.caminho_mais_curto(origem, destino)
        if caminho:
            print(f"\n  {origem} → {destino}")
            print("  Caminho: " + " → ".join(caminho))
            print(f"  Distância: {len(caminho) - 1} conexão(ões)")
        else:
            print(f"\n  {origem} e {destino}: sem caminho (grafo desconexo)")

    # ------------------------------------------------------------------ #
    #  7. Componentes conexos                                              #
    # ------------------------------------------------------------------ #
    separador("6. COMPONENTES CONEXOS (DFS)")
    componentes = rede.componentes_conexos()
    print(f"\n  Total de componentes: {len(componentes)}")
    for i, comp in enumerate(componentes, 1):
        print(f"  Componente {i}: {sorted(comp)}")

    # ------------------------------------------------------------------ #
    #  8. Adiciona vértice isolado para demonstrar grafo desconexo        #
    # ------------------------------------------------------------------ #
    separador("7. GRAFO DESCONEXO — VÉRTICE ISOLADO")
    rede.adicionar_pessoa("Fernanda")
    print("\n  Após adicionar 'Fernanda' sem amizades:")
    componentes = rede.componentes_conexos()
    print(f"  Total de componentes: {len(componentes)}")
    for i, comp in enumerate(componentes, 1):
        print(f"  Componente {i}: {sorted(comp)}")

    caminho = rede.caminho_mais_curto("Alexandre", "Fernanda")
    print(f"\n  Caminho Alexandre → Fernanda: {caminho if caminho else 'Impossível'}")

    # ------------------------------------------------------------------ #
    #  9. Remoção                                                          #
    # ------------------------------------------------------------------ #
    separador("8. REMOVENDO AMIZADE E PESSOA")
    rede.remover_amizade("Alexandre", "Emerson")
    rede.remover_pessoa("Diego")

    # ------------------------------------------------------------------ #
    #  10. Estatísticas finais                                             #
    # ------------------------------------------------------------------ #
    rede.estatisticas()
    print()


if __name__ == "__main__":
    main()
