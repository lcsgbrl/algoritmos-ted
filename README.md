# 🔗 Rede de Contatos — Grafo Não-Direcionado

> **Disciplina:** Estrutura de Dados — Grafos  
> **Autores:** Alexandre Amorim · Emerson Castro · Marcos Yan  

---

## 📌 Sobre o projeto

Implementação de uma **rede social simplificada** usando um **grafo não-direcionado e não-ponderado** com **lista de adjacência**.

O conceito de rede social é intuitivo: pessoas são **vértices**, e amizades são **arestas**. Como amizades são mútuas, o grafo é **não-direcionado** (se A conhece B, B conhece A). Como todas as conexões têm o mesmo "peso", o grafo é **não-ponderado**.

---

## 🗂️ Estrutura do projeto

```
rede-social-grafo/
├── src/
│   └── grafo.py          ← Implementação da classe GrafoRedeSocial
├── visualizacao/
│   └── index.html        ← Visualização interativa no navegador
├── main.py               ← Demonstração de todas as operações
├── testes.py             ← Testes unitários (pytest)
└── README.md
```

---

## 🧠 Conceitos implementados

| Conceito | Onde |
|---|---|
| Lista de adjacência | `dict` com `set` de vizinhos |
| Grafo não-direcionado | `adicionar_amizade` insere nos dois sentidos |
| Grafo não-ponderado | Nenhum peso é armazenado |
| **BFS** (busca em largura) | Distância mínima entre pessoas |
| **DFS** (busca em profundidade) | Detecta componentes conexos |
| Caminho mais curto | BFS com rastreamento de predecessores |
| Grau do vértice | `len(adj[pessoa])` |

---

## ▶️ Como executar

### Pré-requisitos
- Python 3.10+

### Demonstração completa
```bash
python main.py
```

### Testes unitários
```bash
pip install pytest
python -m pytest testes.py -v
```

### Visualização interativa
Abra o arquivo `visualizacao/index.html` diretamente no navegador.  
Clique em qualquer nó para ver as **distâncias BFS** a partir dele.

---

## 🔍 Exemplo de saída

```
LISTA DE ADJACÊNCIA
Alexandre  │ Bruno → Emerson → Marcos → Patricia
Emerson    │ Alexandre → Bruno → Marcos
...

BFS a partir de Alexandre:
  Alexandre     ★  0 conexões
  Emerson       ●  1 conexão
  Marcos        ●  1 conexão
  Bruno         ●●  2 conexões
  Diego         ●●  2 conexões
```

---

## 📊 Complexidade

| Operação | Complexidade |
|---|---|
| Adicionar vértice | O(1) |
| Adicionar aresta | O(1) |
| Verificar amizade | O(1) — `set` |
| BFS / DFS | O(V + E) |
| Amigos em comum | O(min(grau_A, grau_B)) |

> **V** = número de pessoas · **E** = número de amizades

---

## 📐 Representação visual

```
Alexandre ─── Emerson ─── Bruno
    │               │          │
  Marcos          Marcos     Carla
    │
  Carla

Patricia ─── Diego
```

A lista de adjacência é ideal para **grafos esparsos** (poucas arestas em relação ao número máximo possível), que é o caso típico de redes sociais reais.
