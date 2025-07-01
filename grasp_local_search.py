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

    def two_swap_improvement(self, solution: List[pd.Series], candidates: pd.DataFrame, 
                        total_cost: float, max_budget: float) -> Tuple[List[pd.Series], float]:
        if len(solution) < 2:
            return solution, total_cost
        improved = True
        iteration = 0
        max_iterations = 100
        while improved and iteration < max_iterations:
            improved = False
            iteration += 1
            solution_indices = [item.name for item in solution]
            outside_candidates = candidates[~candidates.index.isin(solution_indices)]
            for i in range(len(solution)):
                for j in range(i+1, len(solution)):
                    s1, s2 = solution[i], solution[j]
                    s1_cost, s2_cost = s1["Custo (R$ mil)"], s2["Custo (R$ mil)"]
                    s1_prio, s2_prio = s1["Prioridade"], s2["Prioridade"]
                    for idx1, c1 in outside_candidates.iterrows():
                        for idx2, c2 in outside_candidates.iterrows():
                            if idx1 >= idx2:
                                continue
                            new_cost = total_cost - (s1_cost + s2_cost) + c1["Custo (R$ mil)"] + c2["Custo (R$ mil)"]
                            if new_cost <= max_budget:
                                new_prio = c1["Prioridade"] + c2["Prioridade"]
                                old_prio = s1_prio + s2_prio
                                if new_prio > old_prio:
                                    # Faz a troca e sai dos loops
                                    solution[i] = c1
                                    solution[j] = c2
                                    total_cost = new_cost
                                    improved = True
                                    print(f"Iteração {iteration}: Objetivo = {sum(item['Prioridade'] for item in solution)}")
                                    break
                        if improved:
                            break
                    if improved:
                        break
                if improved:
                    break
            if not improved:
                print("Sem melhoria na função objetivo, encerrando busca local.")
        if iteration == max_iterations:
            print("Atingiu o número máximo de iterações no two_swap_improvement.")
        return solution, total_cost
    
    def best_improvement(self, solution: List[pd.Series], candidates: pd.DataFrame, 
                         total_cost: float, max_budget: float) -> Tuple[List[pd.Series], float]:
        """Busca local Best Improvement: tenta todas as trocas 1-por-1 e faz a melhor possível por iteração."""
        if not solution:
            return solution, total_cost
        improved = True
        while improved:
            improved = False
            best_delta = 0
            best_i = None
            best_candidate = None
            for i in range(len(solution)):
                current_item = solution[i]
                current_cost = current_item["Custo (R$ mil)"]
                current_prio = current_item["Prioridade"]
                available_candidates = candidates[~candidates.index.isin([item.name for item in solution])]
                for _, candidate in available_candidates.iterrows():
                    new_cost = total_cost - current_cost + candidate["Custo (R$ mil)"]
                    delta_prio = candidate["Prioridade"] - current_prio
                    if new_cost <= max_budget and delta_prio > best_delta:
                        best_delta = delta_prio
                        best_i = i
                        best_candidate = candidate
            if best_i is not None and best_candidate is not None:
                solution[best_i] = best_candidate
                total_cost = total_cost - solution[best_i]["Custo (R$ mil)"] + best_candidate["Custo (R$ mil)"]
                improved = True
        return solution, total_cost 

    def solve(self, df: pd.DataFrame, max_budget: float, method_chosed: int) -> Tuple[pd.DataFrame, float, float]:
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
            

            # Busca local com first improvement
            if(method_chosed == 1):
                solution, total_cost = self.first_improvement(solution, df, total_cost, max_budget)

            # Busca local com 2-swap
            if(method_chosed == 2):
                solution, total_cost = self.two_swap_improvement(solution, df, total_cost, max_budget)
            
            # Busca local com best improvement
            if(method_chosed == 3):
                solution, total_cost =  self.best_improvement(solution, df, total_cost, max_budget)

            
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
        #df = pd.read_csv("solution_viavel.csv")
        df = pd.read_csv("nova_iguacu_dataset_heuristica_100.csv")
        #df = pd.read_csv("nova_iguacu_dataset_heuristica_1000.csv")
        #df = pd.read_csv("nova_iguacu_dataset_heuristica_10000.csv")
        """
        Resultados Obtidos:
            - First improvement:
                    * dataset 100   : Tempo de execução da ultima tentativa:  0:00:10
                    * dataset 1000  : Tempo de execução da ultima tentativa:  0:14:04
                    * dataset 10000 : Tempo de execução da ultima tentativa:  18:51:12

            - Two swap:
                    * dataset 100   : Tempo de execução da ultima tentativa:  19:02:24
                    * dataset 1000  : Tempo de execução da ultima tentativa:
                    * dataset 10000 : Tempo de execução da ultima tentativa:   
            
            - Best Improvement:
                    * dataset 100   : Tempo de execução da ultima tentativa:  0:00:05
                    * dataset 1000  : Tempo de execução da ultima tentativa:  0:04:31
                    * dataset 10000 : Tempo de execução da ultima tentativa:  3:21:31

        Para o dataset de 10.000 instâncias no first improvement, os dados obtidos foram:
                    *   Total de bueiros a serem instalados: 36
                    *   Custo total da solução: R$ 798.00 mil
                    *   Valor da função objetivo: 39258.19.

        Para o dataset de 10.000 instâncias no best improvement, os dados obtidos foram:
                    *   Total de bueiros a serem instalados: 36
                    *   Custo total da solução: R$ 799.00 mil
                    *   Valor da função objetivo: 39269.19
        """
                    
        max_budget = 800
        alpha = 0.3
        max_iterations = 100

        """ Método de Busca Local a ser usado:
            1 : first improvement,
            2 : two swap,
            3 : best improvement 
        """
        method_chosed = 2


        start_time = time.time()
        
        solver = GRASPSolver(alpha=alpha, max_iterations=max_iterations)
        solution, total_cost, objective_value = solver.solve(df, max_budget, method_chosed)

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