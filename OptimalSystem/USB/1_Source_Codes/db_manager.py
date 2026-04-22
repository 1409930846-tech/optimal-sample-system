import os
import json
import glob


class DatabaseManager:
    def __init__(self, db_folder=None):
        if db_folder is None:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            parent_dir = os.path.dirname(current_dir)
            self.db_folder = os.path.join(parent_dir, "2_DB_Files")
        else:
            self.db_folder = db_folder

        if not os.path.exists(self.db_folder):
            os.makedirs(self.db_folder)

    @staticmethod
    def _validate_samples(samples):
        for group in samples:
            for num in group:
                if not (isinstance(num, int) and 1 <= num <= 54):
                    raise ValueError(f"Error: Invalid sample value {num} (must be 1-54)")
        return True

    def save_results(self, m, n, k, j, s, results_list):
        self._validate_samples(results_list)

        y = len(results_list)

        search_pattern = os.path.join(self.db_folder, f"{m}-{n}-{k}-{j}-{s}-*-*.db")
        existing_files = glob.glob(search_pattern)

        x = 1
        if existing_files:
            x_values = []
            for f in existing_files:
                filename = os.path.basename(f).replace('.db', '')
                parts = filename.split('-')
                if len(parts) >= 7:
                    x_values.append(int(parts[5]))
            if x_values:
                x = max(x_values) + 1

        file_name = f"{m}-{n}-{k}-{j}-{s}-{x}-{y}.db"
        file_path = os.path.join(self.db_folder, file_name)

        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(results_list, f)

        print(f"File saved: {file_name}")
        return file_name

    def get_file_list(self):
        files = glob.glob(os.path.join(self.db_folder, "*.db"))
        file_names = [os.path.basename(f).replace('.db', '') for f in files]
        file_names.sort(reverse=True)
        return file_names

    def execute_file(self, filename):
        if not filename.endswith('.db'):
            filename += '.db'
        file_path = os.path.join(self.db_folder, filename)
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []

    def delete_file(self, filename):
        if not filename.endswith('.db'):
            filename += '.db'
        file_path = os.path.join(self.db_folder, filename)
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"Deleted file: {filename}")
            return True
        return False
