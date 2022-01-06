import os
root_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def get_res(resource_name):
    return os.path.join(root_folder, "res", resource_name)
