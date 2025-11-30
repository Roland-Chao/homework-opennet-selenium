import json, os, glob
from library.logger import HandleLog

class FileHandler:
    def __init__(self):
        self.host = '[FileHandler]'
        self.log = HandleLog()
    
    def read_json_file(self, file_path) -> dict:
        # Prevent duplicate input of .json
        if file_path.endswith('.json'):
            file_path = file_path[:-5]
    
        try:
            with open(f'{file_path}.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
            return data
        except FileNotFoundError:
            self.log.error_log(f"{self.host} Read json Failed: '{file_path}.json' not found.")
            return {}
        except json.JSONDecodeError:
            self.log.error_log(f"{self.host} Read json Failed: '{file_path}.json' contains invalid JSON.")
            return {}
        except Exception as e:
            self.log.error_log(f"{self.host} Read json Failed: An unexpected error occurred: {e}")
            return {}

    def find_file_path(self, file_name, search_path='.'):
        matches = glob.glob(os.path.join(search_path, '**', file_name), recursive=True)
        
        if not matches:
            self.log.info_log(f"{self.host} Find_file_path: {file_name} not found.")
            return None
        
        if len(matches) > 1:
            raise RuntimeError(f"{self.host} Find_file_path: Multiple files found for {file_name}: {matches}")
        
        else:
            self.log.info_log(f"{self.host} Find_file_path: {file_name} found, {matches[0]}")
            file_path = os.path.abspath(matches[0])
            return file_path
    
    def check_file_exist(self, file_path):
        return os.path.exists(file_path)
    
    def remove_file(self, file_path: str):
        try:
            os.remove(file_path)
            self.log.info_log(f"File '{file_path}' removed successfully.")
        except FileNotFoundError:
            self.log.debug_log(f"File '{file_path}' does not exist.")
        except PermissionError:
            self.log.debug_log(f"Permission denied to remove '{file_path}'.")
        except Exception as e:
            self.log.debug_log(f"An error occurred: {e}")