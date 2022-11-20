import os


ROOT_PATH = os.path.join(os.path.dirname(__file__), os.path.pardir, os.path.pardir)
SEEDS_DIRNAME = "seeds"
DBT_PROJECT_DIRNAME = "dbt_project"


def get_seed_file_path(seed_file_name: str, seed_type: str) -> str:
    return os.path.join(ROOT_PATH, SEEDS_DIRNAME, seed_type, f"{seed_file_name}.csv")
