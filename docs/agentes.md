# Como os agentes funcionam (e como melhorá-los)

## O que é um subagente no Claude Code

Um subagente é um arquivo Markdown em `.claude/agents/` com:
- **frontmatter (cabeçalho YAML):** `name`, `description` (quando usar), `tools` (quais ferramentas ele pode usar) e `model`;
- **corpo:** o *system prompt*, ou seja, as instruções permanentes do agente.

Quando o Claude principal (o **orquestrador**) chama um subagente, ele roda numa **janela de contexto separada**. Começa do zero, lê só o que o prompt dele manda ler e devolve um resumo. Vantagens:
1. **Especialização:** cada um tem regras próprias (o validador é cético e o implementador não opina).
2. **Contexto limpo:** o validador não é "contaminado" pelo entusiasmo do estrategista.
3. **Permissões mínimas:** o validador não deveria editar estratégias; o estrategista não escreve em `src/`.

A **skill** `.claude/skills/ciclo/SKILL.md` é a receita que o orquestrador segue para encadear os três. Você dispara com `/ciclo WIN$N M5 3 daytrade`.

## O fluxo

```
            ┌──────────────┐  hipótese .md   ┌───────────────┐  módulo .py  ┌────────────┐
 relatórios │ estrategista │ ──────────────▶ │ implementador │ ───────────▶ │ validador  │
 anteriores │   (opus)     │                 │   (sonnet)    │              │  (opus)    │
  ───────▶  └──────────────┘                 └───────────────┘              └─────┬──────┘
     ▲                                                                            │
     └──────────────── report.md com "O que testar a seguir" ◀────────────────────┘
```

A memória do ciclo **são os arquivos**: `research/hypotheses/*.md`, `reports/*/report.md` e `research/registry.jsonl`. Nenhum agente lembra de nada entre execuções; tudo o que importa precisa estar escrito.

## Por que cada modelo
- **estrategista = opus:** criatividade e leitura crítica de relatórios.
- **implementador = sonnet:** tarefa bem especificada, mais rápida e barata.
- **validador = opus:** precisa achar falhas sutis (look-ahead escondido, concentração).

Troque à vontade e compare.

## Como melhorar os agentes (o seu laboratório dentro do laboratório)

1. **Leia os relatórios e as hipóteses depois de cada ciclo.** Quando um agente errar, a correção vira uma regra no prompt dele. Ex.: se o implementador usou `rank()` na série inteira, acrescente isso à lista de proibições.
2. **Uma mudança por vez** no prompt, e rode o ciclo de novo. É o mesmo método científico das estratégias.
3. **Exemplos valem mais que regras.** Quando houver uma boa hipótese, cite o arquivo dela no prompt do estrategista como modelo.
4. **Teste o validador com estratégias "trapaceiras" de propósito** (com look-ahead, ou que só ganham num dia). Se ele deixar passar, o prompt precisa melhorar.
5. **Versione os prompts no git.** Assim dá para ver qual versão do agente produziu qual resultado.

## RAG com PDFs: vale a pena?

RAG (*Retrieval-Augmented Generation*, geração aumentada por recuperação) busca trechos relevantes de documentos e os injeta no contexto do modelo.

**Recomendação em etapas:**
1. **Agora (sem RAG):** coloque os PDFs em `knowledge/pdfs/` (fora do git, por direitos autorais) e peça ao Claude para gerar **fichas de leitura** em `knowledge/notas/<livro>.md`: conceitos, regras testáveis e armadilhas citadas. O estrategista já lê `knowledge/` e usa `Grep`. Para poucas dezenas de documentos isso funciona muito bem, e as fichas são revisáveis por você.
2. **Depois, se a biblioteca crescer (dezenas de livros/papers):** um RAG local de verdade (ex.: extrair texto com `pypdf`, gerar embeddings, que são vetores numéricos de significado, e guardar em `chromadb` ou `sqlite-vec`), exposto como uma ferramenta que o estrategista chama. Bom projeto de portfólio por si só.

O ganho real não é "o modelo saber mais", e sim **ancorar** as hipóteses em ideias com histórico, em vez de só minerar padrões.

## Outros agentes que fariam sentido

| Agente | Função | Quando criar |
|---|---|---|
| **auditor** (advogado do diabo) | Revisa o trabalho do validador: tenta achar look-ahead e erros de lógica que ele deixou passar; revisa mudanças no motor | Quando o volume de estratégias crescer, ou antes de qualquer holdout |
| **pesquisador** | Lê `knowledge/` e produz fichas; sugere famílias de estratégias da literatura | Assim que você trouxer os PDFs |
| **analista de dados** | Checa qualidade dos dados: buracos, rolagem de contratos, barras de leilão, horário de verão | Logo depois do primeiro `fetch` real; dados ruins invalidam tudo |
| **relator** | Consolida vários ciclos num relatório executivo (para portfólio e entrevista) | Quando houver alguns ciclos rodados |

Comece com os três. Adicione um agente quando perceber uma **falha recorrente** que um papel dedicado resolveria. Agente demais vira burocracia.
