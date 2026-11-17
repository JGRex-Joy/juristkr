# juristKR

AI assistant for the legislation of the Kyrgyz Republic. Ask a legal question in plain language and get an answer
grounded in specific articles of the codes, with citations you can verify.

> **Disclaimer:** this is a reference and portfolio project, not legal advice. Always check the official text of the law
> and consult a qualified lawyer.

**Status:** work in progress.

## Architecture

```
Browser (React) ──REST + SSE──▶ Go API ──gRPC stream──▶ AI service (Python) ──▶ LLM (Groq)
                                  │                          │
                           PostgreSQL, Redis               Qdrant ◀── ingestion worker
```

The Go service owns the product (users, auth, chats, rate limits, streaming to the browser).
The Python service owns the intelligence (retrieval, reranking, answer generation with citations).

- **Go API** (`services/api`) is the single entry point for the frontend. It streams answers to the browser via SSE.
- **AI service** (`services/ai`) is mostly stateless. It receives a question with chat context and streams back tokens
  and a list of cited articles.
- **Ingestion worker** (`services/ai`) parses the codes into article-level chunks with metadata, embeds them, and
  indexes them in Qdrant.
- **Contract** between Go and Python is gRPC with server streaming; `.proto` files in `proto/` are the source of truth.

## Tech stack

| Layer         | Tools                                                    |
|---------------|----------------------------------------------------------|
| API           | Go, chi, pgx + sqlc, goose, slog                         |
| Contract      | gRPC, protobuf, buf                                      |
| AI service    | Python 3.12+, uv, grpcio, Pydantic, LangGraph            |
| Retrieval     | Qdrant hybrid search (dense + sparse), bge-m3, bge-reranker-v2-m3 |
| LLM           | Groq, behind a provider interface                        |
| Evaluation    | custom dataset, recall@k, MRR, citation faithfulness     |
| Frontend      | React, Vite, TypeScript, Tailwind, TanStack Query        |
| Data          | PostgreSQL, Redis                                        |
| Infra         | Docker Compose, Makefile, GitHub Actions                 |

## Repository layout

```
juristkr/
├── proto/              # gRPC contracts
├── services/
│   ├── api/            # Go API
│   └── ai/             # Python: gRPC server, RAG, ingestion, eval
├── web/                # React frontend
├── data/               # source texts of the codes
├── deploy/             # docker-compose
└── .github/workflows/  # CI
```
