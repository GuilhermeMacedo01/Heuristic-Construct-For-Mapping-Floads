import pandas as pd
import numpy as np
from datetime import datetime

neighborhoods = [
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

# Bairros com população real
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

min_pop = min(real_population.values())
max_pop = max(real_population.values())

current_time = datetime.now()
np.random.seed(int(current_time.timestamp()))

population = {
    neighborhood: real_population.get(neighborhood, np.random.randint(min_pop, max_pop + 1))
    for neighborhood in neighborhoods
}

df = pd.DataFrame({
    "Bairro": neighborhoods,
    "População": [population[b] for b in neighborhoods]
})

df["Criticidade"] = np.random.randint(1, 6, size=len(df))       
df["Impacto (m2)"] = np.random.randint(600, 1300, size=len(df))
df["Custo (R$ mil)"] = np.random.randint(30, 70, size=len(df))

df = df[
    ["Bairro", "População", "Criticidade", "Impacto (m2)", "Custo (R$ mil)"]
]

csv_path = "nova_iguacu_dataset_heuristica.csv"
df.to_csv(csv_path, index=False)

print(f"Dataset gerado e salvo em '{csv_path}'")