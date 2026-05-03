import os
import json
import glob


class DatabaseManager:
    def __init__(self, db_folder=None):
        """初始化：自动创建用于存放DB文件的文件夹"""
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
                    raise ValueError(f"Serious error: The sample contains data that is not 1-54. -> {num}")
        return True

    def save_results(self, m, n, k, j, s, t, results_list, execution_time=None):
        
        self._validate_samples(results_list)  

        groups = len(results_list)  

        
        file_name = f"{m}-{n}-{k}-{j}-{s}-{t}-{groups}.txt"
        file_path = os.path.join(self.db_folder, file_name)

        
        data = {
            'results': results_list,
            'execution_time': execution_time
        }
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f)

        print(f"File saved successfully: {file_name}")
        return file_name

    def get_file_list(self):
        
        files = glob.glob(os.path.join(self.db_folder, "*.txt"))
        file_names = [os.path.basename(f).replace('.txt', '') for f in files]
        file_names.sort(reverse=True)  
        return file_names

    def execute_file(self, filename):
        
        if not filename.endswith('.txt'):
            filename += '.txt'
        file_path = os.path.join(self.db_folder, filename)
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if isinstance(data, dict):
                return data.get('results', [])
            else:
                return data
        return []

    def delete_file(self, filename):
        
        if not filename.endswith('.txt'):
            filename += '.txt'
        file_path = os.path.join(self.db_folder, filename)
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"Successfully deleted file: {filename}")
            return True
        return False

    def save_result(self, param_values, results, execution_time=None):
        
        m = param_values.get('m')
        n = param_values.get('n')
        k = param_values.get('k')
        j = param_values.get('j')
        s = param_values.get('s')
        t = param_values.get('t')

        if all(v is not None for v in [m, n, k, j, s, t]):
            return self.save_results(m, n, k, j, s, t, results, execution_time)
        return None

    def get_all_records(self):
        
        files = glob.glob(os.path.join(self.db_folder, "*.txt"))
        records = []

        for file_path in files:
            filename = os.path.basename(file_path).replace('.txt', '')
            parts = filename.split('-')

            if len(parts) == 7:
                try:
                    m, n, k, j, s, t, groups = map(int, parts[:7])

                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)

                    
                    if isinstance(data, dict):
                        results = data.get('results', [])
                        execution_time = data.get('execution_time', None)
                    else:
                        results = data
                        execution_time = None

                    params = {'m': m, 'n': n, 'k': k, 'j': j, 's': s, 't': t}

                    records.append((filename, params, results, groups, execution_time))
                except (ValueError, IndexError):
                    continue

        
        records.sort(key=lambda x: x[0], reverse=True)
        return records

    def delete_record(self, record_id):
        
        if not record_id.endswith('.txt'):
            record_id += '.txt'
        file_path = os.path.join(self.db_folder, record_id)
        if os.path.exists(file_path):
            os.remove(file_path)
            return True
        return False


