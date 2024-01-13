# Etymology DB

A graph database connecting words (vertices) by their etymological relationships (edges).

## Setup

1. Install Docker (+ Docker Compose)
2. Install Python 3.9+
3. Run `python transform.py` to pull and generate data files (in `./import`) and further instructions
4. Run `docker-compose up -d`
5. Open http://localhost:3000/ in your browser
6. View `import/README.md` and run each query as suggested

## Datasets used:

- [Etymological Wordnet](http://etym.org/), by Gerard de Melo

## Next Steps

- Include full bootstrapping script, including data load queries directly against graph
- Decorate words and edges with descriptions of relation if/where possible
- Improve and include basic Memgraph graph style
- Possibly a dedicated web UI for this project?
