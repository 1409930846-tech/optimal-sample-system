"""
Optimal Samples Selection System - Core Algorithm Module
"""
import itertools
import random
from typing import List, Set, Tuple

try:
    from db_manager import DatabaseManager
except ImportError:
    class DatabaseManager:
        def save_results(self, m, n, k, j, s, results_list):
            return f"{m}-{n}-{k}-{j}-{s}-1-{len(results_list)}.db"

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

    def optimal_cover(self, samples: List[int], k: int, j: int, s: int) -> List[List[int]]:
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
            uncovered = set(self.generate_all_j_subsets(samples, j))
            selected_groups = []

            while uncovered:
                target_j = random.choice(list(uncovered))
                candidates = self._get_candidate_k_groups(target_j, all_samples_set, k, s)

                best_candidates = []
                best_covered_count = -1

                for candidate in candidates:
                    covered_by_cand = self._generate_covered_j_subsets(candidate, all_samples_set, j, s)
                    newly_covered = uncovered.intersection(covered_by_cand)
                    count = len(newly_covered)

                    if count > best_covered_count:
                        best_covered_count = count
                        best_candidates = [(candidate, newly_covered)]
                    elif count == best_covered_count:
                        best_candidates.append((candidate, newly_covered))

                best_candidate, best_covered_set = random.choice(best_candidates)

                selected_groups.append(list(best_candidate))
                uncovered -= best_covered_set

            if best_global_groups is None or len(selected_groups) < len(best_global_groups):
                best_global_groups = selected_groups

        best_global_groups.sort()
        return best_global_groups

    def validate_parameters(self, m: int, n: int, k: int, j: int, s: int, samples: List[int]) -> tuple[bool, str]:
        if not (self.MIN_SAMPLE <= m <= self.MAX_SAMPLE):
            return False, f"m must be within {self.MIN_SAMPLE}-{self.MAX_SAMPLE}"
        if not (7 <= n <= 25):
            return False, "n must be between 7 and 25."
        if not (4 <= k <= 7):
            return False, "k must be between 4 and 7."
        if not (3 <= s <= 7):
            return False, "s must be between 3 and 7."
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


def run_algorithm(m: int, n: int, k: int, j: int, s: int, selected_samples: List[int]) -> tuple[List[List[int]], str, str]:
    algo = OptimalSampleAlgorithm()

    valid, msg = algo.validate_parameters(m, n, k, j, s, selected_samples)
    if not valid:
        return [], msg, ""

    try:
        result_groups = algo.optimal_cover(selected_samples, k, j, s)
    except Exception as e:
        return [], f"Algorithm error: {str(e)}", ""

    try:
        filename = db.save_results(m, n, k, j, s, result_groups)
    except Exception as e:
        return result_groups, f"Algorithm completed but save failed: {str(e)}", ""

    return result_groups, f"Algorithm completed! Generated {len(result_groups)} optimal groups of {k}-element samples.", filename


if __name__ == "__main__":
    print("=" * 60)
    print("Test Example 3: n=8, k=6, j=4, s=4")
    print("=" * 60)

    samples = [1, 2, 3, 4, 5, 6, 7, 8]
    res, info, _ = run_algorithm(45, 8, 6, 4, 4, samples)

    print(info)
    print("\nGenerated groups:")
    for idx, g in enumerate(res, 1):
        print(f"Group {idx}: {g}")

    print("\nVerifying coverage...")
    algo = OptimalSampleAlgorithm()
    all_j = list(algo.generate_all_j_subsets(samples, 4))
    covered_count = 0
    uncovered_examples = []

    for j_sub in all_j:
        is_covered = False
        for group in res:
            if algo.is_k_group_cover_j_subset(group, j_sub, 4):
                is_covered = True
                break
        if is_covered:
            covered_count += 1
        else:
            if len(uncovered_examples) < 5:
                uncovered_examples.append(j_sub)

    print(f"Coverage: {covered_count}/{len(all_j)} j-subsets")
    if uncovered_examples:
        print(f"Uncovered examples: {uncovered_examples}")
