# UI_SPEC.md — Interface do Tricolink

## Identidade
- Base shadcn/ui + Tailwind; ícones lucide-react; fonte via `next/font` (Inter ou Plus Jakarta Sans para títulos).
- Tokens (CSS variables, tema claro e escuro):
  - `--tc-blue-950 #071A4D` · `--tc-blue-800 #0B2E85` · `--tc-blue-700 #0A3DA8` · `--tc-blue-600 #1450C8` · `--tc-blue-100 #E6EEFC`
  - `--tc-red-600 #D6141F` · `--tc-red-700 #B10F18`
  - `--tc-white #FFFFFF` · `--tc-bg #F6F8FC` · `--tc-text #0B1530` · `--tc-muted #5B6785`
  - Escuro: fundo `#081330`, superfícies `#0E1D45`, texto `#EAF0FF`.
- Uso: **azul** = cor primária (links, títulos de destaque, foco); **vermelho** = ação principal ("Encurtar" / CTA) e erros; **branco** domina os fundos. Contraste mínimo AA.
- Faixa tricolor sutil (azul | branco | vermelho) de 3–4px no topo da página ou do hero como detalhe de marca.
- Bordas arredondadas (`rounded-xl`), sombras suaves, espaçamento generoso, animações discretas respeitando `prefers-reduced-motion`.

## Navbar (replicar a do AImaginator)
> **Anexo obrigatório do dono do projeto:** o componente da navbar do AImaginator (ex.: `Navbar.tsx`) será anexado ao prompt P05. **Se o anexo existir, siga-o à risca** (estrutura, espaçamento, comportamento, mobile). Se não existir, use esta especificação:
- Esquerda: **logo Tricolink** (ícone de elo/atalho + wordmark) no canto superior esquerdo → ao lado, o **seletor de idiomas** (dropdown com os 11 idiomas, nome nativo, idioma atual destacado, teclado acessível).
- Direita: item **Links** (leva a `/links`; para deslogado, leva a `/login?next=/links`) e o bloco de conta igual ao do AImaginator (botão **Entrar** quando deslogado; avatar com menu **Account / Sair** quando logado) e demais controles que o AImaginator tiver (ex.: alternador de tema).
- **Remover** a rota "Galeria". **Trocar** "Estúdio" por **"Links"**.
- Mobile: menu hambúrguer (Sheet), mesmo conteúdo. RTL (árabe): espelhar com propriedades lógicas.
- Sticky no topo, fundo translúcido com blur, item ativo destacado, `aria-current="page"`.

## Landing (`/[locale]`)
1. **Hero**: título forte, subtítulo, **barra de inserção de URL** com botão vermelho "Encurtar". Resultado aparece abaixo: link curto + botão **Copiar** (feedback "Copiado!") + link "Ver estatísticas" (logado). Erros inline (URL inválida, cota excedida com contagem regressiva a partir de `Retry-After`).
2. **Demonstração**: mock do painel (dados fictícios fixos), inspirado no Bitly: cartão do link (curto, destino, criado em), gráfico de cliques (Recharts), tabelas de **países**, **origens** e **dispositivos**. Rótulo "Exemplo ilustrativo".
3. **Três blocos de recursos** (texto + visual, alternando lados): link curto rápido, estatísticas claras e controle (editar destino e expirar).
4. **FAQ** em sanfona acessível (8 perguntas): o que é e como funciona; é grátis; por que encurtar; é seguro; como encurtar; posso personalizar o código; o link expira; vocês guardam meu IP (não).
5. **CTA final** ("Crie sua conta grátis") e **rodapé** (links, copyright, sem seletor de idioma).
6. **Voltar ao topo**: botão flutuante no canto inferior direito, com cursor de mão, exibido depois que o título da demonstração ("Seus links em um só lugar") sai da viewport.
Anônimo pode encurtar (com cota menor); ao exceder ou querer histórico → convite para criar conta.

## Login (`/[locale]/login`)
Card central; abas **Entrar / Criar conta**; botão **Continuar com o Google**; validação inline; mostrar/ocultar senha; link de volta; tratamento de 429 (mostrar tempo de espera). Respeitar `next` (validado).

## Account (`/[locale]/account`)
Perfil (nome de exibição, e-mail somente leitura, idioma preferido), preferências (tema), botão Sair. Layout simples em cartões.

## Links (`/[locale]/links`) — substitui "Estúdio"
- Lista do usuário: **código gerado + link curto** ao lado da **URL original** (truncada com tooltip), cliques, data, ações (copiar, abrir, editar, excluir).
- Busca, paginação por cursor ("carregar mais"), estado vazio com CTA, skeletons, confirmação de exclusão, diálogo de edição (título, destino, expiração; código não editável).
- Cabeçalho com total de cliques (30 dias). Clique na linha abre `/links/[code]`.

## Detalhe (`/[locale]/links/[code]`)
Cartão de detalhes + seletor de período (7/30/90 dias) + gráfico de cliques + tabelas países/origens/dispositivos (mesmos componentes da demo da landing).

## Estados e qualidade
Loading (skeleton), vazio, erro (com retry), offline. Responsivo 320px → 1440px+. Sem layout shift. Lighthouse alvo: ≥95 Performance/A11y/Best Practices/SEO na landing.
