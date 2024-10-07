# essay_answers

## Resumo do Projeto

Neste projeto, criaremos uma aplicação que recebe um ensaio e algumas perguntas do usuário e retorna as respostas a essas perguntas. Este serviço estará disponível ao usuário através de endpoints de API.

## Se você é da MOST e está avaliando meu código, LEIA ISTO!!

1) Tudo o que você precisa saber sobre o projeto está explicado objetiva e claramente aqui.
2) Por favor, siga o [tutorial rápido](./quick_tutorial.ipynb) quando chegar à seção [Uso](#uso).
3) No final deste README, há a seção [*Extra: Reimplementação usando um novo modelo*](#extra-reimplementação-usando-um-novo-modelo) que aborda o **Desafio Extra para Aventureiros**, exposto no ponto **4.** da descrição do desafio.
4) Minhas informações de contato:
      - Nome: Daniel Oliveira Barbosa
      - Email: `danielolibar@gmail.com`
      - Cell: `(33)99994-2000`
      - [Github](https://github.com/ddgob): https://github.com/ddgob
      - [Linkedin](https://www.linkedin.com/in/danieloliveirabarbosa/): [https://www.linkedin.com/in/danieloliveirabarbosa](https://www.linkedin.com/in/danieloliveirabarbosa/)
      - Universidade: UFMG

## Design do Projeto e Decisões Técnicas

### Arquitetura de Classes

O projeto segue uma arquitetura modular com estruturas de classes claramente definidas. Abaixo está um diagrama simplificado ilustrando como os diferentes componentes interagem:

<div align="center">
	<img src="./diagram.png">
</div>

- **SentenceEmbedding**: Esta classe representa uma sentença e sua respectiva incorporação (embedding), fornecendo métodos para calcular a similaridade cosseno e encontrar a sentença mais similar.
- **SentenceTransformer (BERT)**: Esta classe (importada de uma biblioteca externa) permite o uso do modelo BERT `all-mpnet-base-v2`.
- **Encoder**: Esta classe é responsável por codificar as sentenças do ensaio e as perguntas em embeddings usando o modelo BERT descrito anteriormente.
- **TestPreProcessor**: Esta classe pré-processa o ensaio dividindo-o em parágrafos e sentenças, identificando subtítulos e organizando o texto para análise posterior.
- **AnswerService**: A classe de serviço que lida com a lógica central de encontrar respostas para as perguntas comparando embeddings das perguntas com embeddings do ensaio e subtítulos.
- **EssayAnswersAPI**: Esta classe encapsula a lógica da API e fornece o endpoint `/answers` (e outros) para receber o ensaio e as perguntas, coordenando o processo de validação e geração de respostas.

- **AnswerServiceSpan e BertForQuestionAnswering**: Estas classes serão descritas na seção [*Extra: Reimplementação usando um novo modelo*](#extra-reimplementação-usando-um-novo-modelo).

### Modelo Usado para Criar Embeddings

O modelo `all-mpnet-base-v2` da biblioteca SentenceTransformer foi escolhido para gerar embeddings devido ao seu alto desempenho em tarefas como similaridade de sentenças e resposta a perguntas. Este modelo baseado em BERT captura relações complexas entre palavras, produzindo embeddings compactos que permitem correspondência eficiente e precisa de perguntas. A facilidade de uso da biblioteca SentenceTransformer e a eficiência do modelo pré-treinado o tornam ideal para esta tarefa.

### Medida de Similaridade Usada para Comparar Embeddings

A similaridade cosseno foi escolhida devido ao seu foco no ângulo entre vetores em vez de sua magnitude, otimizando para similaridade semântica dos embeddings. Além disso, o uso difundido do BERT e similaridade cosseno em conjunto torna a similaridade cosseno a medida de similaridade ideal.

### Abordagens para Dividir o Ensaio em Sentenças

Primeiro, optamos por não considerar os títulos/subtítulos do ensaio como possíveis respostas à pergunta. Isso evita o caso em que a resposta a uma pergunta é um subtítulo que contém palavras que estão na pergunta (o que a torna muito similar à pergunta), mas não fornece nenhuma informação concreta para responder à questão.

A partir disso, criamos duas abordagens sobre como dividir o ensaio em sentenças, cada uma com seus prós e contras:

#### 1. Analisando todas as sentenças que não são subtítulos

Esta primeira solução consiste em incorporar todas as sentenças (que não são subtítulos) e então buscar a sentença com embedding mais similar à pergunta.

- **Pró:** esta abordagem é minuciosa e garante que a sentença retornada como resposta seja a mais similar possível para uma determinada pergunta.
- **Contra:** esta abordagem tem uma complexidade computacional maior devido à necessidade de incorporar e comparar todas as sentenças que não são subtítulos.

**Importante:** para usar esta abordagem, você deve usar o endpoint `/answers` que é descrito na seção [Referência da API](#referência-da-api).

#### 2. Analisando apenas as sentenças sob o subtítulo mais similar

Esta segunda solução consiste em:
1) Incorporar apenas os subtítulos do ensaio.
2) Buscar o subtítulo que é mais similar à pergunta.
3) Então, incorporar apenas as sentenças que estão sob o subtítulo mais similar encontrado na etapa anterior.
4) Finalmente, buscar a sentença sob o subtítulo encontrado na etapa 2) que é mais similar à pergunta.

- **Pró:** esta abordagem tem uma complexidade computacional menor devido a não precisar incorporar e pesquisar todas as sentenças do ensaio. Nesta abordagem, você pesquisaria apenas os subtítulos e depois as sentenças sob o subtítulo que é mais similar à pergunta.
- **Contra:** esta abordagem pode levar a respostas subótimas, pois não há garantia de que a sentença que melhor responde à pergunta estará sob o subtítulo que é mais similar à pergunta.

**Importante:** para usar esta abordagem, você deve usar o endpoint `/answers_based_on_subtitles` que é descrito na seção [Referência da API](#referência-da-api).

### Guia de Formatação e Estilo

- O código segue as diretrizes do [PEP8](https://pep8.org/) para Python.
- Foi escolhida uma largura máxima de linha de **90 caracteres** para melhorar a legibilidade em ambientes de edição modernos (especialmente devido ao uso de tipagem).
- Comentários seguem um limite de **72 caracteres** por linha para garantir clareza nas explicações sem linhas excessivamente longas.
- Classes, funções e variáveis seguem uma convenção de nomenclatura clara e consistente que visa legibilidade e clareza.

### Tratamento de Erros

Usamos tratamento de erros estruturado, garantindo que todos os endpoints da API retornem mensagens de erro significativas quando dados inválidos são recebidos.

- **400 Bad Request**: Este status é retornado quando o cliente envia dados malformados ou inválidos, como campos obrigatórios ausentes, um ensaio vazio ou perguntas formatadas incorretamente.
- **500 Internal Server Error**: Este status é retornado para quaisquer problemas inesperados que ocorram dentro do servidor ou lógica da aplicação, indicando que algo deu errado no lado do servidor.

### Gerenciamento de Dependências

- As dependências são gerenciadas usando `pipenv` para isolamento de ambiente e reprodutibilidade.
- O Docker é usado para gerenciamento consistente do ambiente.

### Logging

O projeto implementa logging em vários componentes para fornecer insights detalhados sobre as operações internas. O logging é usado para rastrear os seguintes processos:

- Pré-processamento de texto (divisão de parágrafos, identificação de subtítulos, etc.).
- Codificação de sentenças e geração de embeddings.
- Comparação de perguntas e ensaio para encontrar as respostas mais relevantes.
- Validação e manipulação de solicitações de API em `EssayAnswersAPI`.

## Pré-requisitos

### Docker

Certifique-se de ter o Docker instalado em sua máquina. O Docker lidará com a configuração do ambiente, incluindo dependências do sistema e instalações de pacotes Python.

### Dependências

Este projeto utiliza os seguintes pacotes Python, que são instalados automaticamente dentro do contêiner Docker:

- `flask`
- `gunicorn`
- `pybind11`
- `sentence-transformers`
- `numpy==1.24`
- `mypy`
- `pytest`
- `flask-testing`
- `torch`
- `requests`
- `ipykernel`

As dependências são gerenciadas usando `pipenv`. Você não precisa instalá-las manualmente, a menos que esteja executando a aplicação fora do Docker.

## Instalação

### Passo 1: Clone o repositório

```bash
git clone https://github.com/ddgob/essay_answers
cd essay_answers
```

### Passo 2: Construa o contêiner Docker

Construa e execute a aplicação usando o Docker:

```bash
docker build -t essay_answers .
docker run -d -p 8000:8000 --name essay_answers_api essay_answers
```

Este comando irá:

- Construir a imagem Docker usando o arquivo Dockerfile.
- Instalar dependências do sistema (por exemplo, cmake, g++, etc.).
- Instalar dependências Python usando pipenv.
- Construir o módulo necessário pybind11.
- Configurar o ambiente do contêiner e expor a porta 8000.

### Passo 3: Verifique se o contêiner está em execução

Você pode verificar se o contêiner está em execução e se a API está ouvindo em http://0.0.0.0:8000.

```bash
docker ps
```

Você deve ver o contêiner em execução com um nome semelhante a `essay_answers_api`.

## Uso

Uma vez que o contêiner esteja em execução, você pode começar a interagir com a API.

### Comece Aqui

A melhor maneira de ver e entender o uso da API e seus recursos é seguir este [tutorial rápido](./quick_tutorial.ipynb).

### Outra Opção (pior)

No entanto, se você não quiser entender completamente como a API funciona e não ver seus recursos, aqui está um exemplo de como enviar uma solicitação POST para o endpoint `/answers`.

#### Exemplo de Solicitação:

```bash
curl -X POST http://127.0.0.1:8000/answers \
    -H "Content-Type: application/json" \
    -d '{
            "essay": "Introduction to Trees.\nTrees are green. Trees have leaves. Trees are tall.\nConclusion\nI love trees. I want to buy five trees.", 
            "queries": ["What is the color of trees?", "How tall are trees?", "How many trees do I want to buy?"]
        }'
```

**Importante:** certifique-se de ter o `curl` instalado.

#### Exemplo de Resposta:

```bash
{
  "answers": ["Trees are green", "Trees are tall", "I want to buy five trees"]
}
```

**Nota:** o mesmo pode ser feito para usar o endpoint `/answers_based_on_subtitles`. Basta alterar o endereço da solicitação POST!

## Referência da API

- POST `/answers`
    - **Descrição:** Retorna as respostas às perguntas fornecidas com base no ensaio dado.
    - **Corpo da Solicitação:**
        - `essay` (string): O texto do ensaio.
        - `queries` (array de strings): Uma lista de perguntas relacionadas ao ensaio.
    - **Corpo da Resposta:**
        - `answers` (array de strings): Uma lista de respostas correspondentes às perguntas.

- POST `/answers_based_on_subtitles`
    - **Descrição:** Retorna as respostas às perguntas fornecidas, primeiro encontrando os subtítulos que melhor correspondem a elas e, em seguida, encontrando as sentenças dentro dos parágrafos correspondentes a esses subtítulos que melhor correspondem às perguntas.
    - **Corpo da Solicitação:**
        - `essay` (string): O texto do ensaio.
        - `queries` (array de strings): Uma lista de perguntas relacionadas ao ensaio.
    - **Corpo da Resposta:**
        - `answers` (array de strings): Uma lista de respostas correspondentes às perguntas.

- POST `/answers_span`
    - Consulte [Endpoint da API: `/answers_span`](#endpoint-da-api-answers_span).

## Testes

Para testar a aplicação, você pode executar o seguinte comando:

```bash
docker exec -it essay_answers_api python tests/run_checks.py
```

Isso executará o pytest em todos os testes implementados em `/tests` e também verificará a tipagem em todo o projeto usando `mypy`.

## *Extra: Reimplementação usando um novo modelo*

Além da resposta baseada em embeddings de sentenças, este projeto inclui resposta a perguntas baseada em span usando um modelo BERT específico para resposta a perguntas.

### Resposta a Perguntas Baseada em Span: `AnswerServiceSpan`

A classe `AnswerServiceSpan` aproveita o modelo `bert-large-uncased-whole-word-masking-finetuned-squad` para extrair a resposta exata de um ensaio identificando as posições inicial e final do trecho de resposta.

#### Como Funciona:
- **Modelo BERT**: O modelo BERT pré-treinado identifica trechos de resposta dentro de um ensaio.
- **Método**: O modelo recebe tanto o ensaio quanto a pergunta, retornando o trecho de texto que melhor responde à pergunta.
- **Caso de Uso**: Ideal para extração precisa de informações.

### Endpoint da API: `/answers_span`

Você pode usar este endpoint para enviar ensaios e perguntas, recebendo trechos específicos de texto como respostas.

#### Exemplo de Solicitação:

```bash
curl -X POST http://127.0.0.1:8000/answers_span \
    -H "Content-Type: application/json" \
    -d '{
            "essay": "The quick brown fox jumps over the lazy dog.",
            "queries": ["What does the quick brown fox jump over?"]
        }'
```

#### Exemplo de Resposta:

```json
{
  "answers": ["the lazy dog"]
}
```