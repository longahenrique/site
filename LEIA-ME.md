# Site henriquelonga.pt

O site é gerado automaticamente. Cada vez que guardas uma alteração neste repositório (um *commit*), o GitHub corre o gerador e publica o site novo, em um ou dois minutos.

## Como publicar um artigo de opinião

1. Abre a pasta **artigos**.
2. Carrega em **Add file › Create new file**.
3. No nome, escreve o endereço do artigo, sem acentos nem espaços e a acabar em `.md`.
   Exemplo: `habitacao-e-juventude.md`. O endereço do artigo no site passa a ser `henriquelonga.pt/opiniao/habitacao-e-juventude`.
4. Copia o conteúdo do ficheiro **_modelo.md** (está na mesma pasta), cola-o e preenche.
5. Carrega em **Commit changes** (a opção "Commit directly to the main branch").
6. Espera um ou dois minutos e abre o site.

### O que cada linha quer dizer

| Linha | O que escrever |
|---|---|
| `titulo` | O título do artigo. |
| `data` | A data de publicação, assim: `2026-09-16` (ano-mês-dia, com os zeros). |
| `meio` | O nome do jornal ou da publicação, como aparece nas listas e nos filtros. |
| `linha` | A frase por baixo do título. Escreve `{data}` onde queres a data. Exemplo: `Publicado n’O Setubalense em {data}.` |
| `link` | (opcional) O endereço do artigo original. |
| `link-texto` | (opcional) O texto do botão para o original. Exemplo: `Ler no Diário do Distrito`. |
| `descricao` | (opcional) Uma frase curta, para o Google e para as partilhas. |

Depois da segunda linha `---`, escreve o texto. Cada parágrafo é separado por **uma linha em branco**. Para itálico, põe um asterisco de cada lado: `*assim*`.

### O que se atualiza sozinho

A página do artigo, a lista de artigos (com a pesquisa e os filtros), os três artigos da página inicial, os "Outros artigos", o feed RSS, o mapa do site e a imagem de partilha com o título.

## Como corrigir ou apagar um artigo

- **Corrigir:** abre o ficheiro em **artigos**, carrega no lápis, altera e faz **Commit changes**.
- **Apagar:** abre o ficheiro, carrega no caixote do lixo e faz **Commit changes**.

## Se aparecer um erro

Vai ao separador **Actions**. Cada publicação é uma linha:
- círculo laranja: está a ser publicada;
- visto verde: publicada;
- **X vermelho**: houve um erro. Abre essa linha, depois **build**, e o passo **Gerar o site**. A mensagem diz em português o que está mal (por exemplo, uma data escrita de maneira errada). Corrige o ficheiro e faz outro commit.

## O que há neste repositório

- `artigos/` : os artigos de opinião (um ficheiro por artigo).
- `gerador/` : o programa que monta o site. Não é preciso mexer.
- `fotos-originais/` : as fotografias da galeria, em tamanho original.
- `fonts/` : os tipos de letra do site.
- `og-image.jpg` : a imagem de partilha da página inicial.
- `CNAME` : liga o endereço henriquelonga.pt a este site. **Não apagar.**

As outras páginas (biografia, programa, galeria, imprensa, avisos) continuam a ser alteradas com a ajuda de quem mantém o gerador.
