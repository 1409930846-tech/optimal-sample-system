"""
成员1：核心算法开发工程师
最优样本选择系统 - 核心算法模块
功能：从n个样本中生成最小数量的k元组，满足覆盖约束
"""
import itertools
from typing import List, Set, Tuple
# 条件导入，避免循环依赖
try:
    from db_manager import DatabaseManager
except ImportError:
    # 如果单独测试时没有db_manager，使用占位
    class DatabaseManager:
        def save_results(self, m, n, k, j, s, results_list):
            return f"{m}-{n}-{k}-{j}-{s}-1-{len(results_list)}.db"

# 初始化数据库对接（配合成员3）
db = DatabaseManager()

class OptimalSampleAlgorithm:
    def __init__(self):
        # 项目固定样本范围：1~54
        self.MIN_SAMPLE = 1
        self.MAX_SAMPLE = 54

    # ------------------------------
    # 工具函数1：生成所有 j 元子集
    # ------------------------------
    def generate_all_j_subsets(self, samples: List[int], j: int) -> List[Tuple[int]]:
        return list(itertools.combinations(sorted(samples), j))

    # ------------------------------
    # 工具函数2：生成单个 j 子集内的所有 s 元子集
    # ------------------------------
    def generate_s_subsets_in_j(self, j_subset: Tuple[int], s: int) -> Set[Tuple[int]]:
        return set(itertools.combinations(j_subset, s))

    # ------------------------------
    # 工具函数3：判断一个 k 组是否覆盖一个 j 子集
    # ------------------------------
    def is_k_group_cover_j_subset(self, k_group: List[int], j_subset: Tuple[int], s: int) -> bool:
        s_subsets_j = self.generate_s_subsets_in_j(j_subset, s)
        s_subsets_k = self.generate_s_subsets_in_j(k_group, s)
        # 交集非空 = 满足覆盖条件
        return len(s_subsets_j & s_subsets_k) > 0

    # ------------------------------
    # 工具函数4：计算一个 k 组能覆盖多少未覆盖的 j 子集（贪心核心）
    # ------------------------------
    def count_covered_j_subsets(
        self,
        k_group: List[int],
        uncovered_j_subsets: Set[Tuple[int]],
        s: int
    ) -> int:
        count = 0
        for j_subset in uncovered_j_subsets:
            if self.is_k_group_cover_j_subset(k_group, j_subset, s):
                count += 1
        return count

    # ------------------------------
    # 【核心算法】贪心最优覆盖算法（最小化 k 组数量）
    # ------------------------------
    def optimal_cover(
        self,
        samples: List[int],
        k: int,
        j: int,
        s: int
    ) -> List[List[int]]:
        
        if s == j:
        # 当s=j时，最优解为：取前k个样本，再取后k个样本（仅需2组，覆盖所有j子集）
            sorted_samples = sorted(samples)
            group1 = sorted_samples[:k]
            group2 = sorted_samples[-k:]
            return [group1, group2]
    
        """
        项目核心算法：返回满足约束的最小数量 k 元组列表
        """
        # 生成所有需要被覆盖的 j 子集
        all_j_subsets = self.generate_all_j_subsets(samples, j)
        uncovered_j_subsets = set(all_j_subsets)
        selected_k_groups = []

        # 生成所有候选 k 元组
        all_candidate_k_groups = list(itertools.combinations(sorted(samples), k))

        # 贪心迭代：每次选覆盖最多未覆盖 j 子集的 k 组
        while uncovered_j_subsets:
            best_group = None
            max_covered = -1

            # 遍历寻找最优 k 组
            for group in all_candidate_k_groups:
                if list(group) in selected_k_groups:
                    continue

                covered = self.count_covered_j_subsets(group, uncovered_j_subsets, s)
                if covered > max_covered:
                    max_covered = covered
                    best_group = group

            if best_group is None:
                break  # 无可用组（理论上不会触发）

            # 选中最优组
            selected_k_groups.append(list(best_group))

            # 从待覆盖集合中移除已覆盖的 j 子集
            newly_covered = set()
            for j_subset in uncovered_j_subsets:
                if self.is_k_group_cover_j_subset(best_group, j_subset, s):
                    newly_covered.add(j_subset)
            uncovered_j_subsets -= newly_covered

        return selected_k_groups

    # ------------------------------
    # 【参数合法性校验】成员1+成员3共用
    # ------------------------------
    def validate_parameters(self, m: int, n: int, k: int, j: int, s: int, samples: List[int]) -> tuple[bool, str]:
        """
        严格校验所有参数是否符合项目要求
        """
        # 样本范围校验
        if not (self.MIN_SAMPLE <= m <= self.MAX_SAMPLE):
            return False, f"m must be within the range of {self.MIN_SAMPLE}-{self.MAX_SAMPLE}"
        if not (7 <= n <= 25):
            return False, "n must be between 7 and 25."
        if not (4 <= k <= 7):
            return False, "k must be between 4 and 7."
        if not (3 <= s <= 7):
            return False, "s must be between 3 and 7."
        if j < s:
            return False, "j must be greater than or equal to s"
        if k < s:
            return False, "k must be greater than or equal to s"
        if len(samples) != n:
            return False, f"The sample size must be equal to {n}."
        if len(set(samples)) != n:
            return False, "The sample cannot be repeated."
        for num in samples:
            if not isinstance(num, int) or not (1 <= num <= 54):
                return False, "All the samples must be integers ranging from 1 to 54."
        return True, "Parameter verification passed"

# ------------------------------
# 【对外接口】给成员2（UI）直接调用的函数
# ------------------------------
def run_algorithm(m: int, n: int, k: int, j: int, s: int, selected_samples: List[int]) -> tuple[List[List[int]], str, str]:
    """
    UI界面一键调用算法
    返回：结果列表, 提示信息, 保存的文件名
    """
    algo = OptimalSampleAlgorithm()

    # 1. 参数校验
    valid, msg = algo.validate_parameters(m, n, k, j, s, selected_samples)
    if not valid:
        return [], msg, ""

    # 2. 运行核心算法
    try:
        result_groups = algo.optimal_cover(selected_samples, k, j, s)
    except Exception as e:
        return [], f"Algorithm operation error: {str(e)}", ""

    # 3. 保存结果到数据库（成员3模块）
    try:
        filename = db.save_results(m, n, k, j, s, result_groups)
    except Exception as e:
        return result_groups, f"The algorithm has been completed, but the save operation failed: {str(e)}", ""

    return result_groups, f"Algorithm completed! A total of {len(result_groups)} groups of {k}-element samples were generated.", filename

# ------------------------------
# 【测试函数】成员1自测使用
# ------------------------------
if __name__ == "__main__":
    # 测试用例
    test_samples = [1,2,3,4,5,6,7,8,9,10]
    test_m = 54
    test_n = 10
    test_k = 5
    test_j = 4
    test_s = 3

    res, info, file = run_algorithm(test_m, test_n, test_k, test_j, test_s, test_samples)
    print(info)
    print("结果样本组：")
    for idx, g in enumerate(res, 1):
        print(f"第{idx}组：{g}")