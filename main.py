import pandas as pd

df = pd.read_csv("nova_iguacu_dataset_heuristica.csv")

max_budget = 400 
limit_sewer = 5

# Calcular prioridade:
df["Prioridade"] = (df["Impacto (m³)"] * df["Criticidade"]) / df["Custo (R$ mil)"]

df_sorted = df.sort_values(by="Prioridade", ascending=False)

solution = []
total_cost = 0

for _, local in df_sorted.iterrows():
    local_cost = local["Custo (R$ mil)"]
    if (total_cost + local_cost <= max_budget) and (len(solution) < limit_sewer):
        solution.append(local)
        total_cost += local_cost

df_solution = pd.DataFrame(solution)

print("Solução Otimizada - Heurística de Construção")
print(df_solution[[
    "ID", "Bairro", "População", "Criticidade", "Impacto (m³)", 
    "Custo (R$ mil)", "Coordenadas", "Prioridade"
]])

df_solution.to_csv("solution_viavel.csv", index=False)
print("\nArquive ready'solution_viavel.csv'")
