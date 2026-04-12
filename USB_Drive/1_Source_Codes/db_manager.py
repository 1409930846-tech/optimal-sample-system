import os
import json
import glob


class DatabaseManager:
    def __init__(self, db_folder=None):
        """初始化：自动创建用于存放DB文件的文件夹"""
        if db_folder is None:
            # 获取当前文件所在目录的绝对路径
            current_dir = os.path.dirname(os.path.abspath(__file__))
            # 获取上一级目录
            parent_dir = os.path.dirname(current_dir)
            # 2_DB_Files 放在上一级目录下
            self.db_folder = os.path.join(parent_dir, "2_DB_Files")
        else:
            self.db_folder = db_folder
        
        if not os.path.exists(self.db_folder):
            os.makedirs(self.db_folder)

    # 加上了 @staticmethod，消除了第一个黄色警告，显得非常专业！
    @staticmethod
    def _validate_samples(samples):
        """辅责任务：拦截错误数据，确保样本都是 1-54 的正整数"""
        for group in samples:
            for num in group:
                if not (isinstance(num, int) and 1 <= num <= 54):
                    raise ValueError(f"严重错误: 样本中包含非 1-54 的数据 -> {num}")
        return True

    def save_results(self, m, n, k, j, s, results_list):
        """主责任务：保存算法结果，自动生成 m-n-k-j-s-x-y.db 文件"""
        self._validate_samples(results_list)  # 存入前先安检

        y = len(results_list)  # y 就是跑出来的组数

        search_pattern = os.path.join(self.db_folder, f"{m}-{n}-{k}-{j}-{s}-*-*.db")
        existing_files = glob.glob(search_pattern)

        x = 1  # 默认第1次
        if existing_files:
            x_values = []
            for f in existing_files:
                filename = os.path.basename(f).replace('.db', '')
                parts = filename.split('-')
                if len(parts) >= 7:
                    x_values.append(int(parts[5]))  # 第6个数字就是x
            if x_values:
                x = max(x_values) + 1  # 自动+1

        # 拼接文件名
        file_name = f"{m}-{n}-{k}-{j}-{s}-{x}-{y}.db"
        file_path = os.path.join(self.db_folder, file_name)

        # 写入文件
        with open(file_path, 'w', encoding='utf-8') as f:
            # noinspection PyTypeChecker
            # ↑ 上面这行注释专门用来压制 PyCharm 的第二个黄色警告
            json.dump(results_list, f)

        print(f"File saved successfully: {file_name}")
        return file_name

    def get_file_list(self):
        """主责任务：把所有文件名发给界面，让界面显示列表"""
        files = glob.glob(os.path.join(self.db_folder, "*.db"))
        file_names = [os.path.basename(f).replace('.db', '') for f in files]
        file_names.sort(reverse=True)  # 最新的排前面
        return file_names

    def execute_file(self, filename):
        """主责任务：实现 EXECUTE，读取文件内容给界面展示"""
        if not filename.endswith('.db'):
            filename += '.db'
        file_path = os.path.join(self.db_folder, filename)
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []

    def delete_file(self, filename):
        """主责任务：实现 DELETE，删除文件"""
        if not filename.endswith('.db'):
            filename += '.db'
        file_path = os.path.join(self.db_folder, filename)
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"Successfully deleted file: {filename}")
            return True
        return False


# # ==========================================
# # 下面是测试代码。注意：if __name__ 必须顶在最左边（不缩进）！
# # ==========================================
# if __name__ == "__main__":
#     print("🚀 正在启动 成员3(数据模块) 的独立自测...\n")
#
#     # 初始化数据库
#     db = DatabaseManager("Test_DB_Folder")
#
#     # 模拟成员1(算法)生成的一组成功数据
#     fake_good_data = [
#         [1, 2, 3, 4, 5, 6],
#         [7, 8, 9, 10, 11, 12]
#     ]
#
#     # 模拟成员1生成的一组包含错误的数据
#     fake_bad_data = [
#         [1, 2, 'A', 4, 5, 6],
#         [99, 8, 9, 10, 11, 12]
#     ]
#
#     print("▶️ [测试1] 正常保存文件")
#     file1 = db.save_results(45, 9, 6, 5, 5, fake_good_data)
#     if file1 == "45-9-6-5-5-1-2.db":
#         print("   ✅ 测试通过！生成文件名格式完全正确。")
#     else:
#         print(f"   ❌ 测试失败！当前是: {file1}")
#
#     print("\n▶️ [测试2] x值自动递增测试")
#     file2 = db.save_results(45, 9, 6, 5, 5, fake_good_data)
#     if file2 == "45-9-6-5-5-2-2.db":
#         print("   ✅ 测试通过！成功识别历史记录，x自动变成了 2！")
#     else:
#         print(f"   ❌ 测试失败！当前是: {file2}")
#
#     print("\n▶️ [测试3] 防脏数据拦截测试")
#     try:
#         db.save_results(45, 9, 6, 5, 5, fake_bad_data)
#     except ValueError as e:
#         print(f"   ✅ 测试通过！成功拦截非法数据: {e}")
#
#     print("\n▶️ [测试4] 读取与列表获取测试")
#     print(f"   当前数据库列表: {db.get_file_list()}")
#     if db.execute_file(file1) == fake_good_data:
#         print(f"   ✅ 测试通过！成功从文件中读取出原始数据！")
#
#     print("\n▶️ [测试5] 删除文件测试")
#     db.delete_file(file1)
#     db.delete_file(file2)
#     if len(db.get_file_list()) == 0:
#         print("   ✅ 测试通过！数据库已清空！")