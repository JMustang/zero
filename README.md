# Estudando backend com dunossauro

Este projeto utiliza FastAPI para criação de uma API backend moderna e rápida. Abaixo estão as principais ferramentas utilizadas no desenvolvimento:

## Ferramentas

- **FastAPI**  
  Framework web moderno para construção de APIs em Python, com tipagem forte e validação automática.

- **Poetry**  
  Gerenciador de dependências e ambientes virtuais para Python, facilitando o controle de pacotes e scripts.

- **Ruff**  
  Ferramenta de linting e formatação de código Python, garantindo qualidade e padronização do código.

- **Pytest**  
  Framework de testes para Python, utilizado para criar e rodar testes automatizados.

- **pytest-cov**  
  Plugin do Pytest para medir a cobertura de testes do código.

- **Taskipy**  
  Ferramenta para automatizar tarefas via comandos definidos no `pyproject.toml`.

## Scripts Úteis

Os principais comandos podem ser executados via Poetry ou Taskipy:

- `task lint` — Executa o Ruff para checagem de lint.
- `task format` — Formata o código com Ruff.
- `task run` — Inicia o servidor FastAPI em modo desenvolvimento.
- `task test` — Executa os testes com Pytest e gera relatório de cobertura.
- `task pre_format` — Corrige automaticamente problemas de lint antes de formatar.
- `task pre_test` — Executa o lint antes dos testes.
- `task post_test` — Gera relatório HTML de cobertura após os testes.
