# – Criptografia Avançada com Matrizes (Cifra de Hill Generalizada) 
Trabalho da disciplina Vetores, Geometria Analítica e Algebra Linear (SPOMVAL).
Integrantes do grupo: Valeska Felipe de Almeida, Marcus Vinicius de Souza Moraes Pedro, Ana Julia Dias Medina
---

## Manual do usuário

### Requisitos

- Python 3 instalado.
- Nenhuma biblioteca adicional.

### Como executar

No terminal, dentro da pasta do projeto:

```bash
python hill.py
```

### Passo a passo de uso

**1. Informe o módulo `m`**

Define o conjunto de valores usado na cifra.

| Valor | Uso |
|---|---|
| `26` | Apenas letras de A a Z. Espaços, acentos e símbolos são descartados. |
| `256` | Qualquer caractere (acentos, números, símbolos), tratado como bytes. |

**2. Informe a ordem `n` da matriz**

Tamanho da matriz-chave e dos blocos. Exemplos: `2` (matriz 2×2), `3` (3×3), `4` (4×4). O valor de `n` deve ser menor que `m`.

**3. Digite a matriz-chave**

O programa pede uma linha por vez. Digite os `n` números da linha separados por espaço.

```
Linha 1: 3 3
Linha 2: 2 5
```

O programa calcula o determinante e verifica se a matriz é **invertível módulo m**. Se não for, mostra um erro e pede uma nova matriz.

> Dica para `m = 256`: o determinante precisa ser **ímpar**.

**4. Digite a mensagem**

Escreva o texto a ser cifrado e pressione Enter.

**5. Veja o resultado**

O programa mostra na tela:

- a mensagem original;
- a mensagem cifrada (em letras para `m = 26`, em hexadecimal para `m = 256`);
- a mensagem decifrada;
- o resultado da verificação de integridade.

### O relatório (`relatorio_hill.txt`)

Gerado a cada execução, contém:

1. Parâmetros (`m` e `n`) e a matriz-chave
2. Validação da chave (determinante e MDC)
3. Cálculo da matriz inversa modular, passo a passo
4. Fluxo de transformação dos blocos (texto → números → padding → blocos → cifrado → decifrado)
5. Exemplo detalhado das contas do primeiro bloco
6. Resultado da verificação de integridade

> Cada execução **sobrescreve** o relatório anterior. Para guardá-lo, copie ou renomeie o arquivo antes de rodar de novo.

### Mensagens e o que fazer

| Mensagem | Significado | O que fazer |
|---|---|---|
| `Valor inválido. Digite um número inteiro.` | O valor digitado não é um número inteiro. | Digite apenas dígitos. |
| `Digite um inteiro >= ...` | O número é menor que o mínimo aceito (`m ≥ 2`, `n ≥ 1`). | Digite um valor maior. |
| `A ordem n precisa ser menor que m` | `n` é igual ou maior que `m`. | Escolha um `n` menor. |
| `A linha precisa ter exatamente n números.` | Quantidade errada de números na linha da matriz. | Digite exatamente `n` números separados por espaço. |
| `Use apenas números inteiros.` | A linha da matriz tem letras ou símbolos. | Digite apenas números inteiros. |
| `ERRO: det(K) não é coprimo com m.` | A matriz não tem inversa módulo `m`, então não serviria para decifrar. | Digite outra matriz. |
| `Mensagem vazia (ou sem letras A-Z...)` | Nenhuma letra aproveitável foi digitada (para `m = 26`). | Digite um texto com letras de A a Z. |
| `Aviso: com m=26 só as letras A-Z são usadas` | Algum caractere foi descartado. | Para texto livre, use `m = 256`. |
| `Integridade: FALHOU` | A mensagem decifrada é diferente da original. | Execute novamente e confira os dados digitados. |

---

## Estrutura de arquivos

```
Cifra-de-Hill/
├── hill.py
├── relatorio_hill.txt
├── relatorio_hill2.txt
├── CRIPTOGRAFIA.pdf
└── README.md
```

| Arquivo | Descrição |
|---|---|
| `hill.py` | _programa que executa a criptografia de hill_ |
| `relatorio_hill.txt` | _relatorio gerado pelo programa hill.py, com a palavra de exemplo HELP_ |
| `relatorio_hill2.txt` | _relatorio gerado pelo programa hill.py com a palavra de exemplo BORBOLETA_ |
| `CRIPTOGRAFIA.pdf` | _documento com os conceitos de algebra linear utilizados para o desenvolvimento da criptografia de Hill, no programa hill.py_ |
| `README.md` | _manual do usuário_ |
| _(outro arquivo)_ | _(preencher)_ |