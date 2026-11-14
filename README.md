# A função de cada método do programa
 
## Verificar a chave que o usuário passou
 
Para a chave servir, o determinante precisa ser coprimo com `m`. Isso exige três coisas:
 
| Nome | Função |
|---|---|
| `determinante(M)` | Calcula o número que decide se a matriz é invertível. É recursiva porque o determinante de uma matriz `n×n` é definido a partir de determinantes menores. |
| `menor(M, i, j)` | O `determinante` precisa "cortar" uma linha e uma coluna para chamar a si mesmo com uma matriz menor. Foi separada porque também é usada nos cofatores. |
| `mdc(a, b)` | Verifica se `det` e `m` são coprimos (`mdc == 1`). |
 
Se o teste falhar, o programa pede outra matriz. Sem essa etapa, uma mensagem que poderia ser cifrada que **nunca mais seria decifrar**.
 
---
 
## Decifrar a cifra
 
Decifrar é multiplicar por `K⁻¹`. Em aritmética comum a inversa usa divisão, mas **em Z_m não existe divisão**. Por isso o programa monta a inversa assim:
 
> K⁻¹ = det⁻¹ · adj(K) (mod m)
 
| Nome | Função |
|---|---|
| `euclides_estendido(a, b)` | Acha `x` tal que `a·x + b·y = mdc`. É a ferramenta que permite "dividir" em Z_m. |
| `inverso_modular(a, m)` | Usa o Euclides estendido para devolver o inverso de `a` ou `None` se ele não existir. Calcula o `det⁻¹` da fórmula. |
| `matriz_cofatores(M)` | Primeiro passo para a adjunta. Cada posição vira `(-1)^(i+j) · det(menor)`. |
| `transposta(M)` | A adjunta é a transposta dos cofatores. Fica separada porque é uma operação com sentido próprio. |
| `matriz_adjunta(M)` | Combina cofatores e transposta. |
| `inversa_modular(M, m)` | É a função final desta etapa. Junta tudo (`det`, `det⁻¹`, adjunta) e devolve `K⁻¹`, ou `None` se a matriz não for invertível. |
 
A cadeia de dependência é:
 
```
inversa_modular
 ├── determinante ──► menor
 ├── inverso_modular ──► euclides_estendido
 └── matriz_adjunta ──► matriz_cofatores ──► determinante, menor
                    └─► transposta
```
 
---
 
## Verifica se a inversa calculada está certa
 
| Nome | Função |
|---|---|
| `multiplica_matrizes(A, B, m)` | Multiplica `K · K⁻¹` módulo `m`. |
| `eh_identidade(M)` | Verifica se o resultado é a identidade. |
 
Essas duas funções não são necessárias para cifrar. Elas são um **teste de sanidade**: se a inversa estiver errada por algum bug, o programa avisa antes de gerar uma mensagem "cifrada" impossível de decifrar. Também alimentam o relatório (item 4.5).
 
---
 
## Transformação do texto para matriz
 
Matrizes só multiplicam números, e a mensagem é texto.
 
| Nome | Função |
|---|---|
| `texto_para_numeros(texto, m)` | Converte texto em lista de números. Com `m = 26` vira A=0...Z=25. Com `m = 256` vira os bytes UTF-8, o que permite acentos e símbolos. |
| `numeros_para_texto(nums, m)` | O caminho inverso, usado no final para mostrar a mensagem decifrada. |
 
Elas ficam isoladas para que o resto do programa trabalhe só com listas de números, **sem se preocupar com o alfabeto**. Trocar o alfabeto exigiria mexer só nessas duas funções.
 
---
 
## A mensagem não cabe em blocos de n
 
| Nome | Função |
|---|---|
| `aplicar_padding(nums, n)` | Completa o último bloco. Cada elemento acrescentado guarda **quantos** foram acrescentados. |
| `remover_padding(nums, n)` | Depois de decifrar, lê esse número, apaga o preenchimento e valida que ele está correto. Se o padding vier corrompido, levanta erro em vez de devolver lixo. |
| `dividir_em_blocos(nums, n)` | Quebra a lista em pedaços de tamanho `n`. Cada pedaço é um vetor que a matriz sabe multiplicar. |
| `juntar(blocos)` | O inverso: transforma a lista de blocos de volta em uma lista única, para remover o padding e converter em texto. |
 
A função de gravar a quantidade no próprio padding é evitar **ambiguidade**. Se o usuário preenchesse com `X`, ao decifrar não saberia se aquele `X` final era da mensagem ou do preenchimento.
 
---
 
## Cifrar e Decifrar
 
| Nome | Função |
|---|---|
| `multiplica_matriz_vetor(M, v, m)` | É o **núcleo da cifra**: `C = K·P mod m` para um bloco. |
| `processar_blocos(blocos, M, m)` | Aplica a multiplicação a cada bloco da lista. |
 
O mesmo código serve para cifrar e decifrar. Se passa `K`, cifra. Se passa `K⁻¹`, decifra. Isso evita duplicar lógica e reduz a chance de erro.
 
---
 
## Prova do resultado estar certo
 
| Nome | Função |
|---|---|
| `checksum(nums)` | Gera um número-resumo da mensagem. Comparar dois números é uma segunda verificação, além de comparar as listas. Como multiplica por posição, detectaria também uma troca de ordem. |
 
---
 
## Verificação de inteiros
 
| Nome | Função |
|---|---|
| `ler_inteiro(prompt, minimo)` | Pede `m` e `n` e **insiste** até receber um inteiro válido. Sem ela, digitar "abc" derrubaria o programa. |
| `ler_matriz(n, m)` | Lê `n` linhas com `n` números cada, valida o formato e já aplica `% m` nas entradas. |
 
Ficam separadas do `main()` porque o tratamento de erro de entrada é repetitivo e atrapalharia a leitura do fluxo principal.
 
---
 
## Passos descritos para o relatório
 
| Nome | Função |
|---|---|
| `passos_euclides(a, m)` | Devolve as divisões sucessivas em texto, para o relatório mostrar **como** o inverso do determinante foi achado. As outras funções só devolvem o resultado, sem mostrar o caminho. |
| `fmt_matriz(M)` | Formata matrizes com colunas alinhadas, para ficarem legíveis no relatório. |
 
---
 
## A função `main()`
 
**Coordena** as outras funções na ordem certa, trata o laço de "chave inválida, tente de novo" e monta o relatório.
 
```
ler_inteiro ─► ler_matriz ─► determinante + mdc ──(inválida? repete)
        │
        ▼
inversa_modular ─► multiplica_matrizes + eh_identidade (sanidade)
        │
        ▼
texto_para_numeros ─► aplicar_padding ─► dividir_em_blocos
        │
        ▼
processar_blocos(K)  ─► cifrado
processar_blocos(K⁻¹) ─► juntar ─► remover_padding ─► numeros_para_texto
        │
        ▼
checksum + comparação ─► relatório (passos_euclides, fmt_matriz)
```
- **Segurança e usabilidade:** `multiplica_matrizes` e `eh_identidade` (conferência da inversa), `ler_inteiro` e `ler_matriz` (entrada robusta).
Uma boa pergunta para se fazer em cada função é: "se eu a removesse, o que quebraria?". Se você souber responder isso para todas, vai conseguir defender o trabalho tranquilamente.
 
