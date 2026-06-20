import random
import pandas as pd

TOTAL_ATLETAS = 200

nomes_masculinos = [
    "Bruno", "Carlos", "Eduardo", "Gabriel", "Igor", "Kaio",
    "Marcos", "Otávio", "Rafael", "Thiago", "William", "Rodrigo"
]

nomes_femininos = [
    "Ana", "Daniela", "Fernanda", "Helena", "Juliana", "Larissa",
    "Natália", "Patrícia", "Sabrina", "Vanessa", "Yasmin", "Beatriz"
]

sobrenomes = [
    "Silva", "Souza", "Oliveira", "Santos", "Pereira", "Costa", "Almeida", "Ribeiro",
    "Carvalho", "Gomes", "Martins", "Rocha", "Barbosa", "Moura", "Dias", "Freitas"
]

faixas = [
    (18, 24, "18-24"),
    (25, 29, "25-29"),
    (30, 34, "30-34"),
    (35, 39, "35-39"),
    (40, 44, "40-44"),
    (45, 49, "45-49"),
    (50, 54, "50-54"),
    (55, 59, "55-59"),
    (60, 80, "60+")
]

premios_geral = {
    1: ("R$ 10.000", "Sim", "Ouro"),
    2: ("R$ 5.000", "Sim", "Prata"),
    3: ("R$ 3.000", "Sim", "Bronze"),
    4: ("R$ 1.500", "Sim", "Sim"),
    5: ("R$ 1.000", "Sim", "Sim")
}

premios_pcd = {
    1: "R$ 2.000",
    2: "R$ 1.000",
    3: "R$ 500"
}

categorias_pcd = ["Cadeirante", "Def. Visual", "Amputados", "Não"]

# Gera um nome completo de acordo com o sexo
def gerar_nome(sexo):
    if sexo == "Masculino":
        nome = random.choice(nomes_masculinos)
    else:
        nome = random.choice(nomes_femininos)

    return nome + " " + random.choice(sobrenomes)

# Define a faixa etária com base na idade
def definir_faixa(idade):
    for minimo, maximo, faixa in faixas:
        if minimo <= idade <= maximo:
            return faixa

# Gera um tempo aleatório para o atleta
def gerar_tempo():
    # tempo em minutos
    return round(random.uniform(35, 120), 2)

# Define a premiação por faixa etária
def medalha_faixa(posicao):
    if posicao == 1:
        return "Troféu + Medalha"
    elif posicao in [2, 3]:
        return "Medalha"
    return ""

# Lista que vai armazenar os atletas
atletas = []

# Conjunto usado para evitar nomes repetidos
nomes_usados = set()

# Número inicial dos atletas
i = 1

# Gera atletas até atingir o total definido
while len(atletas) < TOTAL_ATLETAS:
    idade = random.randint(18, 75)
    sexo = random.choice(["Masculino", "Feminino"])
    pcd = random.choices(categorias_pcd, weights=[3, 3, 3, 91])[0]
    nome = gerar_nome(sexo)

    # Se o nome já foi usado, gera outro atleta
    if nome in nomes_usados:
        continue

    nomes_usados.add(nome)

    # Adiciona o atleta na lista
    atletas.append({
    "Número": i,
    "Nome": nome,
    "Sexo": sexo,
    "Idade": idade,
    "Faixa Etária": definir_faixa(idade),
    "Categoria PcD": pcd,
    "Tempo": gerar_tempo()
    })

    i += 1

# Cria uma tabela com os atletas
df = pd.DataFrame(atletas)

# Ordena os atletas pelo menor tempo
df = df.sort_values(by="Tempo").reset_index(drop=True)

print("LISTA DE ATLETAS")
print(df)

print("\n>>> PREMIAÇÃO GERAL - MASCULINO E FEMININO <<<")

# Lista da premiação geral
geral = []

# Separa os vencedores gerais por sexo
for sexo in ["Masculino", "Feminino"]:
    vencedores = df[df["Sexo"] == sexo].head(5)

    for posicao, (_, atleta) in enumerate(vencedores.iterrows(), start=1):
        dinheiro, trofeu, medalha = premios_geral[posicao]

        geral.append({
            "Sexo": sexo,
            "Colocação": f"{posicao}º lugar",
            "Nome": atleta["Nome"],
            "Idade": atleta["Idade"],
            "Tempo": atleta["Tempo"],
            "Dinheiro": dinheiro,
            "Troféu": trofeu,
            "Medalha Especial": medalha
        })

# Cria a tabela da premiação geral
df_geral = pd.DataFrame(geral)
print(df_geral)

print("\n>>> PREMIAÇÃO POR FAIXA ETÁRIA <<<")

# Lista da premiação por faixa etária
resultado_faixas = []

# Percorre sexo e faixa etária para premiar os melhores
for sexo in ["Masculino", "Feminino"]:
    for _, _, faixa in faixas:
        grupo = df[
            (df["Sexo"] == sexo) &
            (df["Faixa Etária"] == faixa)
        ].head(3)

        for posicao, (_, atleta) in enumerate(grupo.iterrows(), start=1):
            resultado_faixas.append({
                "Sexo": sexo,
                "Faixa Etária": faixa,
                "Colocação": f"{posicao}º lugar",
                "Nome": atleta["Nome"],
                "Idade": atleta["Idade"],
                "Tempo": atleta["Tempo"],
                "Premiação": medalha_faixa(posicao)
            })

# Cria a tabela da premiação por faixa etária
df_faixas = pd.DataFrame(resultado_faixas)
print(df_faixas)

print("\n>>> PREMIAÇÃO PcD <<<")

# Lista da premiação PcD
resultado_pcd = []

# Percorre cada categoria PcD
for categoria in ["Cadeirante", "Def. Visual", "Amputados"]:
    grupo = df[df["Categoria PcD"] == categoria].head(3)

    for posicao, (_, atleta) in enumerate(grupo.iterrows(), start=1):
        resultado_pcd.append({
            "Categoria": categoria,
            "Colocação": f"{posicao}º lugar",
            "Nome": atleta["Nome"],
            "Sexo": atleta["Sexo"],
            "Idade": atleta["Idade"],
            "Tempo": atleta["Tempo"],
            "Dinheiro": premios_pcd[posicao]
        })

# Cria a tabela da premiação PcD
df_pcd = pd.DataFrame(resultado_pcd)
print(df_pcd)

print("\n>>> SIMULAÇÃO FINALIZADA <<<")

# Mostra o resumo final da simulação
print("Total de atletas:", TOTAL_ATLETAS)
print("Atletas masculinos:", len(df[df["Sexo"] == "Masculino"]))
print("Atletas femininos:", len(df[df["Sexo"] == "Feminino"]))
print("Atletas PcD:", len(df[df["Categoria PcD"] != "Não"]))
