import pandas as pd
import random
import numpy as np
from typing import List, Tuple
import time
from datetime import timedelta

class GRASPSolver:
    def __init__(self, alpha: float = 0.3, max_iterations: int = 100):
        """
        alpha: Parâmetro de aleatorização (0 a 1)
        max_iterations: Número máximo de iterações do GRASP
        """
        self.alpha = alpha
        self.max_iterations = max_iterations
        self.best_solution = None
        self.best_cost = float('-inf')
        self.best_total_cost = 0

    def calculate_priority(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        df["Prioridade"] = (df["Impacto (m2)"] * df["Criticidade"]) / df["Custo (R$ mil)"]
        return df

    def build_restricted_candidate_list(self, candidates: pd.DataFrame, max_budget: float) -> pd.DataFrame:
        """Constrói a lista de candidatos"""
        sorted_candidates = candidates.sort_values(by="Prioridade", ascending=False)
        
        min_priority = sorted_candidates["Prioridade"].min()
        max_priority = sorted_candidates["Prioridade"].max()
        threshold = max_priority - self.alpha * (max_priority - min_priority)
        
        candidates_list = sorted_candidates[sorted_candidates["Prioridade"] >= threshold]
        
        candidates_list = candidates_list[candidates_list["Custo (R$ mil)"] <= max_budget]
        
        return candidates_list

    def first_improvement(self, solution: List[pd.Series], candidates: pd.DataFrame, 
                         total_cost: float, max_budget: float) -> Tuple[List[pd.Series], float]:
        """Realiza a busca local First Improvement"""

        improved = True
        while improved:
            improved = False
            for i in range(len(solution)):
                current_item = solution[i]
                current_cost = current_item["Custo (R$ mil)"]
                
                available_candidates = candidates[~candidates.index.isin([item.name for item in solution])]
                
                for _, candidate in available_candidates.iterrows():
                    new_cost = total_cost - current_cost + candidate["Custo (R$ mil)"]
                    if new_cost <= max_budget:
                        if candidate["Prioridade"] > current_item["Prioridade"]:
                            solution[i] = candidate
                            total_cost = new_cost
                            improved = True
                            break
                
                if improved:
                    break
        
        return solution, total_cost

    def solve(self, df: pd.DataFrame, max_budget: float) -> Tuple[pd.DataFrame, float, float]:
        """        
        df: DataFrame com os dados dos bairros
        max_budget: Orçamento máximo disponível
        """
        if df.empty:
            raise ValueError("O DataFrame de entrada está vazio")

        df = self.calculate_priority(df)
        
        for _ in range(self.max_iterations):
            solution = []
            total_cost = 0
            candidates = df.copy()
            
            while not candidates.empty:
                rcl = self.build_restricted_candidate_list(candidates, max_budget - total_cost)
                
                if rcl.empty:
                    break
                    
                available_candidates = rcl[~rcl.index.isin([item.name for item in solution])]
                chosen = available_candidates.sample(n=1).iloc[0]
                
                if total_cost + chosen["Custo (R$ mil)"] <= max_budget:
                    solution.append(chosen)
                    total_cost += chosen["Custo (R$ mil)"]
                
                candidates = candidates[candidates.index != chosen.name]
            
            # Busca local de first improvement
            solution, total_cost = self.first_improvement(solution, df, total_cost, max_budget)
            
            if solution:
                solution_value = sum(item["Prioridade"] for item in solution)
                if solution_value > self.best_cost:
                    self.best_solution = solution
                    self.best_cost = solution_value
                    self.best_total_cost = total_cost
        
        if not self.best_solution:
            return pd.DataFrame(), 0, 0
        
        df_solution = pd.DataFrame(self.best_solution)
        
        return df_solution, self.best_total_cost, self.best_cost

def main():
    try:        
        # Escolhe o dataset a ser utilizado
        #df = pd.read_csv("nova_iguacu_dataset_heuristica_100.csv")
        #df = pd.read_csv("nova_iguacu_dataset_heuristica_1000.csv") # Tempo de execução da ultima tentativa:  0:14:04
        df = pd.read_csv("nova_iguacu_dataset_heuristica_10000.csv") # Tempo de execução da ultima tentativa:  18:51:12

        """ Para o dataset de 10.000 instâncias, os dados obtidos foram:
                            Total de bueiros a serem instalados: 36
                            Custo total da solução: R$ 798.00 mil
                            Valor da função objetivo: 39269.19.
        """
                    
        max_budget = 800
        alpha = 0.3
        max_iterations = 100

        start_time = time.time()
        
        solver = GRASPSolver(alpha=alpha, max_iterations=max_iterations)
        solution, total_cost, objective_value = solver.solve(df, max_budget)

        end_time = time.time()
        execution_time = end_time - start_time
        
        if solution.empty:
            print("Nenhuma solução viável foi encontrada")
            return
        
        mean_cost_sewer = 20  # custo médio de um bueiro em mil reais
        solution["Qtd_Bueiros"] = (solution["Custo (R$ mil)"] / mean_cost_sewer).round().astype(int)
        
        print("\nSolução GRASP - Heurística de Construção")
        print(solution[[
            "Bairro", "População", "Criticidade", "Impacto (m2)", 
            "Custo (R$ mil)", "Qtd_Bueiros", "Prioridade"
        ]])
        
        print(f"\nTotal de bueiros a serem instalados: {solution['Qtd_Bueiros'].sum()}")
        print(f"Custo total da solução: R$ {total_cost:.2f} mil")
        print(f"Valor da função objetivo: {objective_value:.2f}")
        print(f"\nTempo de execução: {timedelta(seconds=int(execution_time))}")
        
        solution.to_csv("solution_grasp.csv", index=False)
        print("\nArquivo salvo como 'solution_grasp.csv'")
        
    except Exception as e:
        print(f"Erro durante a execução: {str(e)}")

if __name__ == "__main__":
    main() 