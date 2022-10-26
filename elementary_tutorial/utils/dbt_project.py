import os


ROOT_PATH = os.path.join(os.path.dirname(__file__), os.path.pardir)
SEEDS_DIRNAME = 'seeds'
DBT_PROJECT_DIRNAME = 'dbt_project'


def get_dbt_project_path(project_dir: str) -> str:
    return os.path.join(ROOT_PATH, project_dir, DBT_PROJECT_DIRNAME)


def get_seed_file_path(project_dir: str, seed_file_name: str, seed_type: str) -> str:
    dbt_project_path = get_dbt_project_path(project_dir)
    return os.path.join(dbt_project_path, SEEDS_DIRNAME, seed_type, f'{seed_file_name}.csv')
