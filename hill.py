"""
Cifra de Hill generalizada

- Funciona em Z_m (ex.: m = 26 para letras, m = 256 para bytes/ASCII).
- Matriz-chave de ordem n x n, validada por det(K) coprimo com m.
- Padding no estilo PKCS7: cada byte de preenchimento guarda a quantidade
  de bytes adicionados, o que permite removê-lo sem ambiguidade.
- Verificação de integridade e geração de relatório (relatorio_hill.txt).
"""

# ----------------------------------------------------------------------
# 1) MATEMÁTICA BÁSICA
# ----------------------------------------------------------------------
def mdc(a, b):
    """Máximo divisor comum (Algoritmo de Euclides)."""
    a, b = abs(a), abs(b)
    while b != 0:
        a, b = b, a % b
    return a


def euclides_estendido(a, b):
    """Retorna (g, x, y) tal que a*x + b*y = g = mdc(a, b)."""
    x0, y0, x1, y1 = 1, 0, 0, 1
    while b != 0:
        q = a // b
        a, b = b, a - q * b
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1
    return a, x0, y0


def inverso_modular(a, m):
    """Inverso de a em Z_m, ou None se mdc(a, m) != 1."""
    a = a % m
    g, x, _ = euclides_estendido(a, m)
    if g != 1:
        return None
    return x % m


def passos_euclides(a, m):
    """Texto com as divisões sucessivas do Euclides (para o relatório)."""
    linhas = []
    x, y = m, a % m
    while y != 0:
        q, r = x // y, x % y
        linhas.append(f"    {x} = {q} * {y} + {r}")
        x, y = y, r
    return linhas

# ----------------------------------------------------------------------
# 2) ÁLGEBRA DE MATRIZES (só com inteiros, sem divisão)
# ----------------------------------------------------------------------
def menor(M, i, j):
    """Submatriz de M sem a linha i e sem a coluna j."""
    return [linha[:j] + linha[j + 1:] for k, linha in enumerate(M) if k != i]

def determinante(M):
    """Determinante por expansão de cofatores na 1ª linha (recursivo)."""
    n = len(M)
    if n == 1:
        return M[0][0]
    if n == 2:
        return M[0][0] * M[1][1] - M[0][1] * M[1][0]
    total = 0
    for j in range(n):
        total += ((-1) ** j) * M[0][j] * determinante(menor(M, 0, j))
    return total

def matriz_cofatores(M):
    n = len(M)
    if n == 1:
        return [[1]]
    return [[((-1) ** (i + j)) * determinante(menor(M, i, j))
             for j in range(n)] for i in range(n)]


def transposta(M):
    return [list(col) for col in zip(*M)]


def matriz_adjunta(M):
    """Adjunta = transposta da matriz de cofatores."""
    return transposta(matriz_cofatores(M))


def inversa_modular(M, m):
    """K^-1 = det^-1 * adj(K) (mod m). Retorna None se não for invertível."""
    det = determinante(M) % m
    det_inv = inverso_modular(det, m)
    if det_inv is None:
        return None
    adj = matriz_adjunta(M)
    return [[(det_inv * x) % m for x in linha] for linha in adj]


def multiplica_matrizes(A, B, m):
    n = len(A)
    return [[sum(A[i][k] * B[k][j] for k in range(n)) % m
             for j in range(n)] for i in range(n)]


def eh_identidade(M):
    n = len(M)
    return all(M[i][j] == (1 if i == j else 0)
               for i in range(n) for j in range(n))


def multiplica_matriz_vetor(M, v, m):
    """Calcula (M * v) mod m."""
    return [sum(M[i][j] * v[j] for j in range(len(v))) % m
            for i in range(len(M))]


# ----------------------------------------------------------------------
# 3) TEXTO <-> NÚMEROS
# ----------------------------------------------------------------------
def texto_para_numeros(texto, m):
    """m=26: A..Z -> 0..25 (ignora o que não for letra). m=256: bytes UTF-8."""
    if m == 26:
        nums = []
        for c in texto.upper():
            if 'A' <= c <= 'Z':
                nums.append(ord(c) - ord('A'))
        return nums
    return list(texto.encode("utf-8"))


def numeros_para_texto(nums, m):
    if m == 26:
        return "".join(chr(x + ord('A')) for x in nums)
    return bytes(nums).decode("utf-8", errors="replace")


def aplicar_padding(nums, n):
    """PKCS7: adiciona k valores iguais a k (1 <= k <= n).
    Se a mensagem já é múltipla de n, adiciona um bloco inteiro."""
    k = n - (len(nums) % n)
    return nums + [k] * k


def remover_padding(nums, n):
    """Lê o último valor k e remove k elementos (com validação)."""
    if not nums:
        raise ValueError("mensagem vazia")
    k = nums[-1]
    if k < 1 or k > n or k > len(nums) or nums[-k:] != [k] * k:
        raise ValueError("padding inválido")
    return nums[:-k]


def dividir_em_blocos(nums, n):
    return [nums[i:i + n] for i in range(0, len(nums), n)]


# ----------------------------------------------------------------------
# 4) CIFRAR / DECIFRAR
# ----------------------------------------------------------------------
def processar_blocos(blocos, M, m):
    """Aplica M a cada bloco (serve tanto para cifrar com K quanto
    para decifrar com K^-1)."""
    return [multiplica_matriz_vetor(M, b, m) for b in blocos]


def juntar(blocos):
    return [x for b in blocos for x in b]


def checksum(nums):
    """Soma de verificação simples e ponderada pela posição."""
    s = 0
    for i, x in enumerate(nums):
        s = (s + (i + 1) * (x + 1)) % 1000003
    return s


# ----------------------------------------------------------------------
# 5) ENTRADA DE DADOS
# ----------------------------------------------------------------------
def ler_inteiro(prompt, minimo):
    while True:
        try:
            v = int(input(prompt))
            if v >= minimo:
                return v
            print(f"  Digite um inteiro >= {minimo}.")
        except ValueError:
            print("  Valor inválido. Digite um número inteiro.")

def ler_matriz(n, m):
    """Lê a matriz linha por linha (números separados por espaço)."""
    print(f"Digite a matriz-chave {n}x{n}, uma linha por vez, "
          f"com {n} números separados por espaço.")
    while True:
        M = []
        for i in range(n):
            while True:
                partes = input(f"  Linha {i + 1}: ").split()
                try:
                    linha = [int(p) % m for p in partes]
                except ValueError:
                    print("  Use apenas números inteiros.")
                    continue
                if len(linha) != n:
                    print(f"  A linha precisa ter exatamente {n} números.")
                    continue
                M.append(linha)
                break
        return M


# ----------------------------------------------------------------------
# 6) PROGRAMA PRINCIPAL
# ----------------------------------------------------------------------
def fmt_matriz(M):
    return "\n".join("    " + "  ".join(f"{x:4d}" for x in linha) for linha in M)


def main():
    print("=== Cifra de Hill Generalizada ===\n")

    # módulo e ordem
    m = ler_inteiro("Módulo m (26 = letras, 256 = ASCII/bytes): ", 2)
    n = ler_inteiro("Ordem n da matriz (ex.: 2, 3, 4): ", 1)

    if m == 26 and n > 25 or m == 256 and n > 255 or n >= m:
        print("A ordem n precisa ser menor que m (por causa do padding).")
        return

    # valida a matriz-chave
    while True:
        K = ler_matriz(n, m)
        det_bruto = determinante(K)
        det = det_bruto % m
        g = mdc(det, m)
        print(f"  det(K) = {det_bruto}  ->  {det} (mod {m});  mdc({det}, {m}) = {g}")
        if g == 1:
            print("  Matriz válida (invertível módulo m).\n")
            break
        print("  ERRO: det(K) não é coprimo com m. Informe outra matriz.\n")

    # Inversa modular (com conferência K * K^-1 = I)
    det_inv = inverso_modular(det, m)
    adj = matriz_adjunta(K)
    K_inv = inversa_modular(K, m)
    if not eh_identidade(multiplica_matrizes(K, K_inv, m)):
        print("Erro interno: K * K^-1 não deu a identidade.")
        return

    # Cifração e decifragem
    mensagem = input("Digite a mensagem: ")
    nums_orig = texto_para_numeros(mensagem, m)
    if not nums_orig:
        print("Mensagem vazia (ou sem letras A-Z, no caso de m=26).")
        return
    if m == 26 and numeros_para_texto(nums_orig, m) != mensagem.upper():
        print("Aviso: com m=26 só as letras A-Z são usadas "
              "(espaços, acentos e símbolos foram descartados).")

    nums_pad = aplicar_padding(nums_orig, n)
    blocos_claros = dividir_em_blocos(nums_pad, n)
    blocos_cifrados = processar_blocos(blocos_claros, K, m)
    nums_cifrados = juntar(blocos_cifrados)

    blocos_decifrados = processar_blocos(blocos_cifrados, K_inv, m)
    nums_decifrados = juntar(blocos_decifrados)

    try:
        nums_recuperados = remover_padding(nums_decifrados, n)
        texto_recuperado = numeros_para_texto(nums_recuperados, m)
        iguais = (nums_recuperados == nums_orig)
    except ValueError:
        nums_recuperados, texto_recuperado, iguais = [], "", False

    cs_orig = checksum(nums_orig)
    cs_rec = checksum(nums_recuperados)
    integro = iguais and cs_orig == cs_rec

    if m == 26:
        texto_cifrado = numeros_para_texto(nums_cifrados, m)
    else:
        texto_cifrado = " ".join(f"{x:02X}" for x in nums_cifrados)

    print("\n--- Resultado ---")
    print("Mensagem original :", mensagem)
    print("Mensagem cifrada  :", texto_cifrado)
    print("Mensagem decifrada:", texto_recuperado)
    print(f"Checksum original = {cs_orig} | decifrada = {cs_rec}")
    print("Integridade       :", "OK (mensagens idênticas)" if integro
          else "FALHOU (mensagens diferentes)")

    # Relatório
    r = []
    r.append("RELATÓRIO - CIFRA DE HILL GENERALIZADA")
    r.append("=" * 50)
    r.append(f"\n1. PARÂMETROS\n  Módulo m = {m}\n  Ordem n = {n}")
    r.append("\n2. MATRIZ-CHAVE K\n" + fmt_matriz(K))

    r.append("\n3. VALIDAÇÃO DA CHAVE")
    r.append(f"  det(K) = {det_bruto}  (mod {m}) = {det}")
    r.append(f"  mdc({det}, {m}) = {g}  -> coprimo, logo K é invertível.")

    r.append("\n4. CÁLCULO DA INVERSA MODULAR")
    r.append("  Fórmula: K^-1 = det(K)^-1 * adj(K)  (mod m)")
    r.append(f"\n  4.1 Inverso de det = {det} módulo {m} (Euclides):")
    r.extend(passos_euclides(det, m))
    r.append(f"    Retrocedendo, obtém-se det^-1 = {det_inv}  "
             f"(confere: {det} * {det_inv} = {det * det_inv} "
             f"≡ {(det * det_inv) % m} mod {m})")
    r.append("\n  4.2 Matriz de cofatores C[i][j] = (-1)^(i+j) * det(menor_ij):")
    r.append(fmt_matriz(matriz_cofatores(K)))
    r.append("\n  4.3 Adjunta = transposta dos cofatores:")
    r.append(fmt_matriz(adj))
    r.append(f"\n  4.4 K^-1 = {det_inv} * adj(K) (mod {m}):")
    r.append(fmt_matriz(K_inv))
    r.append("\n  4.5 Conferência: K * K^-1 (mod m) =")
    r.append(fmt_matriz(multiplica_matrizes(K, K_inv, m)))

    r.append("\n5. FLUXO DE TRANSFORMAÇÃO DO TEXTO")
    r.append(f"  Mensagem original: {mensagem}")
    r.append(f"  Em números ({len(nums_orig)}): {nums_orig}")
    k_pad = len(nums_pad) - len(nums_orig)
    r.append(f"  Padding (estilo PKCS7): +{k_pad} valores iguais a {k_pad}")
    r.append(f"  Após padding ({len(nums_pad)}): {nums_pad}")
    r.append(f"  Divisão em {len(blocos_claros)} bloco(s) de tamanho {n}")

    r.append("\n  Bloco claro  --(K)-->  Bloco cifrado  --(K^-1)-->  Decifrado")
    for bc, bk, bd in zip(blocos_claros, blocos_cifrados, blocos_decifrados):
        r.append(f"  {bc} -> {bk} -> {bd}")

    r.append("\n6. EXEMPLO DETALHADO (1º bloco)")
    b = blocos_claros[0]
    r.append(f"  P = {b}")
    for i in range(n):
        termos = " + ".join(f"{K[i][j]}*{b[j]}" for j in range(n))
        soma = sum(K[i][j] * b[j] for j in range(n))
        r.append(f"  C[{i}] = {termos} = {soma} ≡ {soma % m} (mod {m})")
    c = blocos_cifrados[0]
    r.append(f"  C = {c}")
    for i in range(n):
        termos = " + ".join(f"{K_inv[i][j]}*{c[j]}" for j in range(n))
        soma = sum(K_inv[i][j] * c[j] for j in range(n))
        r.append(f"  P'[{i}] = {termos} = {soma} ≡ {soma % m} (mod {m})")

    r.append("\n7. VERIFICAÇÃO DE INTEGRIDADE")
    r.append(f"  Mensagem cifrada : {texto_cifrado}")
    r.append(f"  Mensagem decifrada: {texto_recuperado}")
    r.append(f"  Comparação direta: {'iguais' if iguais else 'DIFERENTES'}")
    r.append(f"  Checksum original = {cs_orig}, decifrada = {cs_rec}")
    r.append(f"  Resultado: {'INTEGRIDADE OK' if integro else 'FALHA DE INTEGRIDADE'}")

    with open("relatorio_hill.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(r) + "\n")
    print("\nRelatório gerado em 'relatorio_hill.txt'.")


if __name__ == "__main__":
    main()