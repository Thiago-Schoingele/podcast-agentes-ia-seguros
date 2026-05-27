# Podcast Agentes de IA Seguros

Projeto educacional da DIO para o desafio de criação de um podcast técnico com apoio de IA generativa.

O tema central do podcast é segurança em agentes de IA, com foco em boas práticas, riscos, validação e organização segura dos materiais produzidos durante o processo criativo.

## Ferramentas Planejadas

- ChatGPT: criação estratégica, prompts, roteiro e capa/imagem.
- ElevenLabs: geração da narração em áudio.
- Codex: organização técnica, revisão, validação e preparação segura do repositório.
- GitHub: entrega final do projeto.

## Adaptação do Fluxo Original

O desafio original utiliza MidJourney e CapCut em partes do fluxo de criação. Este projeto adapta essa etapa para usar ChatGPT na criação visual e Codex na organização, revisão e refinamento técnico do repositório.

Esta adaptação está documentada para deixar claro quais ferramentas estão planejadas para este projeto, sem afirmar o uso de ferramentas que não foram utilizadas.

## Nome do Podcast

Nome definido:

**Segurança em Agentes de IA**

Subtítulo:

**LLMs, APIs e Automações Seguras na Prática**

O nome foi definido após dois promptings: um prompt inicial de geração de nomes e um prompt de correção para remover opções genéricas e chegar a uma opção mais direta e precisa.

## Episódio 01

**Título:** Por que agentes de IA precisam de segurança desde o início

**Status:** roteiro, narração final e capa validados.

O episódio 01 foi criado com apoio do ChatGPT, otimizado para narração no ElevenLabs e validado após duas gerações de áudio. A primeira versão ficou longa demais, enquanto a versão final ficou com aproximadamente 4min27s e foi aprovada como áudio final.

A capa foi criada com dois promptings: um prompt inicial de composição visual e um prompt de correção para ajustar a paleta dark tech magenta/violeta.

Arquivos finais:

- [Roteiro final](script/episodio-01-roteiro-final.md)
- [Áudio final](output/episodio-01-seguranca-em-agentes-de-ia.mp3)
- [Capa final](assets/capa-podcast-seguranca-em-agentes-de-ia.png)

Nenhum arquivo sensível foi incluído nesta etapa.

## Estrutura do Repositório

```text
README.md
.gitignore
.github/
  workflows/
    ci.yml
prompts/
  01-prompt-nome-podcast.md
  01-1-prompt-correcao-nome-podcast.md
  02-prompt-roteiro-episodio-01.md
  02-1-prompt-ajuste-narracao-elevenlabs.md
  02-2-prompt-otimizacao-roteiro-elevenlabs.md
  02-3-prompt-reducao-roteiro-tempo-elevenlabs.md
  03-prompt-capa-podcast.md
  03-1-prompt-correcao-capa-paleta-fiap-sentrya.md
script/
  episodio-01-roteiro-final.md
assets/
  capa-podcast-seguranca-em-agentes-de-ia.png
output/
  episodio-01-seguranca-em-agentes-de-ia.mp3
docs/
  validacao-audio-elevenlabs.md
  validacao-capa-podcast.md
scripts/
  validate_repository.py
```

## Status do Projeto

Estrutura inicial criada, nome oficial do podcast definido e episódio 01 com roteiro, narração final e capa validados.

O projeto ainda está em construção. Etapas futuras podem incluir validações adicionais, organização final e configuração de CI em momento posterior.

## Validação automatizada

Este repositório inclui uma GitHub Actions CI leve para validar a estrutura do projeto.

A validação verifica:
- presença dos arquivos obrigatórios;
- existência da capa final e do áudio final;
- ausência de arquivos sensíveis;
- ausência de arquivos temporários ou desnecessários;
- organização mínima esperada para entrega educacional.

A CI não usa secrets, não chama APIs externas e não faz deploy.

Validação local:

```bash
python scripts/validate_repository.py
```

## Aviso de Segurança

Este repositório não deve conter chaves de API, tokens, credenciais, arquivos `.env`, dados pessoais sensíveis ou prints de contas de ferramentas como ElevenLabs, ChatGPT ou GitHub.

Também não devem ser adicionados PDFs ou materiais internos da DIO, arquivos de sistema, caches, logs ou configurações locais.
