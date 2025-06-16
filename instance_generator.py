import pandas as pd
import numpy as np
from datetime import datetime

def generate_neighborhoods(base_neighborhoods, num_generic):
    """Gera lista de bairros combinando bairros reais com genéricos"""
    generic_neighborhoods = [f"Bairro {i+1}" for i in range(num_generic)]
    return base_neighborhoods + generic_neighborhoods

def generate_dataset(num_instances, base_neighborhoods, real_population):
    """Gera um dataset com o número especificado de instâncias"""
    if num_instances > len(base_neighborhoods):
        neighborhoods = generate_neighborhoods(base_neighborhoods, num_instances - len(base_neighborhoods))
    else:
        neighborhoods = base_neighborhoods[:num_instances]

    min_pop = min(real_population.values())
    max_pop = max(real_population.values())
    
    extended_max_pop = max_pop * 2

    current_time = datetime.now()
    np.random.seed(int(current_time.timestamp()))

    population = {
        neighborhood: real_population.get(neighborhood, np.random.randint(min_pop, extended_max_pop + 1))
        for neighborhood in neighborhoods
    }

    df = pd.DataFrame({
        "Bairro": neighborhoods,
        "População": [population[b] for b in neighborhoods]
    })

    df["Criticidade"] = np.random.randint(1, 11, size=len(df))  # 1-10
    df["Impacto (m2)"] = np.random.randint(500, 3000, size=len(df))  # 500-3000
    df["Custo (R$ mil)"] = np.random.randint(20, 150, size=len(df))  # 20-150

    return df[["Bairro", "População", "Criticidade", "Impacto (m2)", "Custo (R$ mil)"]]

base_neighborhoods = [
    "Austin", "Belmonte", "Belo Vale", "Humanitá", "Biquinha", "Boa Esperança",
    "Botujuru", "Brás de Pina", "Cachoeira Grande", "Cabral", "Cabuçu", "Califórnia",
    "Centro", "Cidade Olímpica", "Coroado", "Da Prata", "Donana", "Dona Elvira",
    "Dona Eulália", "Engenheiro Pedreira", "Fazenda da República", "Gato Grande",
    "Geraldo", "Guarujá", "Jardim Guandu", "Jardim Toronto", "Lote XV", "Miguel Couto",
    "Montese", "Moquetá", "Nova Aurora", "Nova Belém", "Nova Era", "Nova Posse",
    "Parque Fluminense", "Parque Nova Iguaçu", "Parque Presidente Vargas",
    "Ceramica", "Posse", "Quintino", "Riachão", "Riachinho", "Santa Eugênia",
    "Santa Inês", "Santa Rita", "Corumba", "São Bento", "Santo Antônio",
    "Santo Elias", "Carmari", "Tingui", "Tingui Mirim", "Tinguá",
    "Três Bocas", "Vila de Cava", "Vila da Sapê", "Vila São João", "Vila Tinguá",
    "Vila União", "Zumbi", "Bairro da Luz", "Comendador Soares", "Morro do Barão",
    "Morro do Castro", "Morro do Escorrega", "Morro do Fogueteiro", "Morro do São João",
]

real_population = {
    "Centro": 25806,
    "Bairro da Luz": 23823,
    "Moquetá": 7106,
    "Comendador Soares": 23431,
    "Austin": 23216,
    "Miguel Couto": 6831,
    "Tinguá": 4094,
    "Cabuçu": 29731,
    "Posse": 10921,
    "Vila de Cava": 16413
}

sizes = [100, 1000, 10000]
for size in sizes:
    df = generate_dataset(size, base_neighborhoods, real_population)
    csv_path = f"nova_iguacu_dataset_heuristica_{size}.csv"
    df.to_csv(csv_path, index=False)
    print(f"Dataset com {size} instâncias gerado e salvo em '{csv_path}'")
    print(f"Estatísticas do dataset {size}:")
    print(f"População: min={df['População'].min()}, max={df['População'].max()}, média={df['População'].mean():.2f}")
    print(f"Criticidade: min={df['Criticidade'].min()}, max={df['Criticidade'].max()}, média={df['Criticidade'].mean():.2f}")
    print(f"Impacto: min={df['Impacto (m2)'].min()}, max={df['Impacto (m2)'].max()}, média={df['Impacto (m2)'].mean():.2f}")
    print(f"Custo: min={df['Custo (R$ mil)'].min()}, max={df['Custo (R$ mil)'].max()}, média={df['Custo (R$ mil)'].mean():.2f}\n")