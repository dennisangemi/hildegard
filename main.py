import json
import os

def define_env(env):
    """
    This is the hook for defining variables, macros and filters
    
    - variables: the dictionary that contains the environment variables
    - macro: a decorator function, to declare a macro.
    """
    
    @env.macro
    def load_json(filepath):
        """
        Load JSON data from a file
        """
        # Assume paths are relative to the docs directory
        base_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "")
        full_path = os.path.join(base_path, filepath)
        
        try:
            with open(full_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            return [{"error": f"Could not load JSON file: {str(e)}"}]
    
    @env.macro
    def filter_by_momento(canti, tipo_momento):
        """
        Filter canti based on momento liturgico
        """
        result = []
        for canto in canti:
            momenti = canto.get('momento', '').split(',')
            
            if tipo_momento == 'ingresso' and any(m in ['14', '21', '24', '32'] for m in momenti):
                result.append(canto)
            elif tipo_momento == 'offertorio' and any(m in ['4', '11'] for m in momenti):
                result.append(canto)
            elif tipo_momento == 'comunione' and any(m in ['5', '16', '31'] for m in momenti):
                result.append(canto)
            elif tipo_momento == 'congedo' and any(m in ['14', '21'] for m in momenti):
                result.append(canto)
                
        return result
