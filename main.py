import pandas as pd
import random

df = pd.read_csv("nova_iguacu_dataset_heuristica.csv")

print("\nColunas disponíveis no DataFrame:")
print(df.columns.tolist())

max_budget = 700 
mean_budget = df["Custo (R$ mil)"].mean() # Calcula o custo médio por bairro
print(f"\nOrçamento máximo: R$ {max_budget} mil")
print(f"Custo médio por bairro: R$ {mean_budget:.2f} mil")

df["Prioridade"] = (df["Impacto (m2)"] * df["Criticidade"]) / df["Custo (R$ mil)"]
df["Prioridade"] = df["Prioridade"] * (1 + random.uniform(-0.1, 0.1))  # Adiciona variação de ±10%

df_sorted = df.sort_values(by="Prioridade", ascending=False)

solution = []
total_cost = 0

candidates = df_sorted.copy()

while not candidates.empty:
    top_candidates = candidates.head(3)
    
    chosen = top_candidates.sample(n=1).iloc[0]
    
    if total_cost + chosen["Custo (R$ mil)"] <= max_budget:
        solution.append(chosen)
        total_cost += chosen["Custo (R$ mil)"]
    else:
        break
    
    candidates = candidates[candidates.index != chosen.name]

df_solution = pd.DataFrame(solution)

print("\nSolução Otimizada - Heurística de Construção")
print(df_solution[[
    "Bairro", "População", "Criticidade", "Impacto (m2)", 
    "Custo (R$ mil)", "Prioridade"
]])

df_solution.to_csv("solution_viavel.csv", index=False)
print("\nArquivo salvo como 'solution_viavel.csv'") 