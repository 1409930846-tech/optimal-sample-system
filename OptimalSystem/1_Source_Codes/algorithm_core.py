import itertools
import random
from typing import List, Set, Tuple

try:
    from db_manager import DatabaseManager
except ImportError:
    class DatabaseManager:
        def save_results(self, m, n, k, j, s, t, results_list):
            return f"{m}-{n}-{k}-{j}-{s}-{t}-{len(results_list)}.txt"

db = DatabaseManager()


class OptimalSampleAlgorithm:
    def __init__(self):
        self.MIN_SAMPLE = 1
        self.MAX_SAMPLE = 54

    def generate_all_j_subsets(self, samples: List[int], j: int) -> List[Tuple[int]]:
        return list(itertools.combinations(sorted(samples), j))

    def is_k_group_cover_j_subset(self, k_group: List[int], j_subset: Tuple[int], s: int) -> bool:
        
        
        return len(set(k_group).intersection(j_subset)) >= s

    def _generate_covered_j_subsets(self, candidate_k: tuple, all_samples_set: set, j: int, s: int) -> Set[Tuple[int]]:
        
        candidate_set = set(candidate_k)
        remaining_set = all_samples_set - candidate_set
        covered = []

        
        for i in range(s, min(j, len(candidate_k)) + 1):
            if j - i > len(remaining_set) or j - i < 0:
                continue
            
            for in_k in itertools.combinations(candidate_k, i):
                
                for out_k in itertools.combinations(remaining_set, j - i):
                    covered.append(tuple(sorted(in_k + out_k)))
        return set(covered)

    def _get_candidate_k_groups(self, target_j: tuple, all_samples_set: set, k: int, s: int, max_candidates=500) -> List[Tuple[int]]:
        
        target_set = set(target_j)
        remaining_set = all_samples_set - target_set
        candidates = []

        
        for i in range(s, min(len(target_j), k) + 1):
            if k - i > len(remaining_set) or k - i < 0:
                continue
            
            for in_target in itertools.combinations(target_j, i):
                
                for out_target in itertools.combinations(remaining_set, k - i):
                    candidates.append(tuple(sorted(in_target + out_target)))

        
        if len(candidates) > max_candidates:
            candidates = random.sample(candidates, max_candidates)

        return candidates

    def optimal_cover(self, samples: List[int], k: int, j: int, s: int, t: int = 1) -> List[List[int]]:
        
        sorted_samples = sorted(samples)
        all_samples_set = set(sorted_samples)
        
        best_global_groups = None
        
        
        total_j_subsets = len(self.generate_all_j_subsets(samples, j))
        if total_j_subsets <= 500:
            restarts = 100  
        elif total_j_subsets <= 3000:
            restarts = 30
        elif total_j_subsets <= 10000:
            restarts = 10
        else:
            restarts = 3    
            
        for _ in range(restarts):
            
            coverage_count = {j_subset: 0 for j_subset in self.generate_all_j_subsets(samples, j)}
            selected_groups = []
            
            while True:
                
                all_covered = all(count >= t for count in coverage_count.values())
                if all_covered:
                    break
                
                
                min_count = min(coverage_count.values())
                candidates_for_min = [j for j, count in coverage_count.items() if count == min_count]
                target_j = random.choice(candidates_for_min)
                
                
                candidates = self._get_candidate_k_groups(target_j, all_samples_set, k, s)
                
                best_candidates = []
                best_score = -1
                
                
                for candidate in candidates:
                    covered_by_cand = self._generate_covered_j_subsets(candidate, all_samples_set, j, s)
                    
                    score = sum(1 for j_sub in covered_by_cand if coverage_count[j_sub] < t)
                    
                    if score > best_score:
                        best_score = score
                        best_candidates = [(candidate, covered_by_cand)]
                    elif score == best_score:
                        best_candidates.append((candidate, covered_by_cand))
                
                if not best_candidates:
                    break
                    
                
                best_candidate, best_covered_set = random.choice(best_candidates)
                
                
                selected_groups.append(list(best_candidate))
                for j_sub in best_covered_set:
                    coverage_count[j_sub] += 1
            
            
            if best_global_groups is None or len(selected_groups) < len(best_global_groups):
                best_global_groups = selected_groups
                
        
        best_global_groups.sort()
        return best_global_groups
    

    def validate_parameters(self, m: int, n: int, k: int, j: int, s: int, t: int, samples: List[int]) -> tuple[bool, str]:
        if not (45 <= m <= 54):
            return False, f"m must be within 45-54"
        if not (7 <= n <= 25):
            return False, "n must be 7-25"
        if not (4 <= k <= 7):
            return False, "k must be 4-7"
        if not (3 <= s <= 7):
            return False, "s must be 3-7"
        
        
        if not isinstance(t, int) or t < 1:
            return False, "t must be a positive integer (t >= 1)"
        
        
        max_t = self._combination(j, s)
        if t > max_t:
            return False, f"t ({t}) cannot exceed C({j},{s}) = {max_t}"
        
        
        if s == j and t != 1:
            return False, f"When s = j, t must be 1 (C({j},{s}) = 1)"
        
        
        if not (s <= j <= k):
            return False, f"j ({j}) must be between s ({s}) and k ({k})"
            
        if k > n:
            return False, f"k ({k}) cannot be greater than n ({n})"
        if len(samples) != n:
            return False, f"Sample size must be {n}."
        if len(set(samples)) != n:
            return False, "Samples cannot have duplicates."
        for num in samples:
            if not isinstance(num, int) or not (1 <= num <= 54):
                return False, f"Samples must be integers {self.MIN_SAMPLE}-{self.MAX_SAMPLE}."
        return True, "Parameter verification passed"

    def _combination(self, n: int, r: int) -> int:
        
        if r > n or r < 0:
            return 0
        if r == 0 or r == n:
            return 1
        r = min(r, n - r)
        result = 1
        for i in range(r):
            result = result * (n - i) // (i + 1)
        return result


def run_algorithm(m: int, n: int, k: int, j: int, s: int, t: int, selected_samples: List[int], auto_save: bool = False) -> tuple[List[List[int]], str, str]:
    algo = OptimalSampleAlgorithm()

    valid, msg = algo.validate_parameters(m, n, k, j, s, t, selected_samples)
    if not valid:
        return [], msg, ""

    try:
        result_groups = algo.optimal_cover(selected_samples, k, j, s, t)
    except Exception as e:
        return [], f"Algorithm error: {str(e)}", ""

    filename = ""
    if auto_save:
        try:
            filename = db.save_results(m, n, k, j, s, t, result_groups)
        except Exception as e:
            return result_groups, f"Algorithm completed but save failed: {str(e)}", ""

    return result_groups, f"Algorithm completed! Generated {len(result_groups)} optimal groups of {k}-element samples.", filename

