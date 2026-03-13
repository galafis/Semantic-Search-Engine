# Semantic Search Engine

Motor de busca semantica utilizando TF-IDF e similaridade por cosseno.

Semantic search engine using TF-IDF vectorization and cosine similarity.

[![Python](https://img.shields.io/badge/Python-3.9+-3776AB.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.0+-000000.svg)](https://flask.palletsprojects.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg?logo=docker)](Dockerfile)

[Portugues](#portugues) | [English](#english)

---

## Portugues

### Visao Geral

Motor de busca que implementa recuperacao de informacao semantica:

- **Vetorizacao TF-IDF**: Transforma documentos em vetores ponderados por frequencia de termo e frequencia inversa de documento.
- **Similaridade por Cosseno**: Rankeia resultados pela similaridade angular entre vetores de consulta e documento.
- **Documentos Similares**: Encontra documentos relacionados dado um documento de referencia.

### Arquitetura

```mermaid
graph TD
    A[Consulta do Usuario] --> B[Flask API]
    B --> C[TFIDFVectorizer]
    C --> D[Tokenizacao e Normalizacao]
    D --> E[Calculo TF-IDF]
    E --> F[Vetor da Consulta]
    F --> G[Similaridade por Cosseno]
    G --> H[Ranking de Resultados]
    H --> I[JSON Response]

    style B fill:#0d1117,color:#c9d1d9,stroke:#58a6ff
    style C fill:#161b22,color:#c9d1d9,stroke:#8b949e
    style G fill:#161b22,color:#c9d1d9,stroke:#8b949e
```

### Inicio Rapido

```bash
git clone https://github.com/galafis/Semantic-Search-Engine.git
cd Semantic-Search-Engine
pip install -r requirements.txt
python app.py
```

### Endpoints

| Metodo | Rota | Descricao |
|--------|------|-----------|
| POST | `/api/search` | Buscar documentos por consulta |
| POST | `/api/index` | Indexar novos documentos |
| GET | `/api/similar/<doc_id>` | Encontrar documentos similares |
| GET | `/api/stats` | Estatisticas do motor |

### Estrutura do Projeto

```
Semantic-Search-Engine/
├── app.py              # API Flask e motor de busca
├── requirements.txt
├── LICENSE
└── README.md
```

---

## English

### Overview

Search engine implementing semantic information retrieval:

- **TF-IDF Vectorization**: Transforms documents into vectors weighted by term frequency and inverse document frequency.
- **Cosine Similarity**: Ranks results by angular similarity between query and document vectors.
- **Similar Documents**: Finds related documents given a reference document.

### Architecture

```mermaid
graph TD
    A[User Query] --> B[Flask API]
    B --> C[TFIDFVectorizer]
    C --> D[Tokenization and Normalization]
    D --> E[TF-IDF Calculation]
    E --> F[Query Vector]
    F --> G[Cosine Similarity]
    G --> H[Result Ranking]
    H --> I[JSON Response]

    style B fill:#0d1117,color:#c9d1d9,stroke:#58a6ff
    style C fill:#161b22,color:#c9d1d9,stroke:#8b949e
    style G fill:#161b22,color:#c9d1d9,stroke:#8b949e
```

### Quick Start

```bash
git clone https://github.com/galafis/Semantic-Search-Engine.git
cd Semantic-Search-Engine
pip install -r requirements.txt
python app.py
```

### Tests

```bash
python -m pytest tests/ -v
```

---

## Autor / Author

**Gabriel Demetrios Lafis**
- GitHub: [@galafis](https://github.com/galafis)
- LinkedIn: [Gabriel Demetrios Lafis](https://linkedin.com/in/gabriel-demetrios-lafis)

## Licenca / License

MIT License - veja [LICENSE](LICENSE) / see [LICENSE](LICENSE).
