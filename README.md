# project-name

Remember to:

1. Replace all instances of `project-name` with the real name of the project
2. Replace all instances of `project_name` with the "package name" of the project
3. Rename the source code folder from `project_name` to your package name
4. Generate a lock file (`poetry install --with dev,tests,linters`)
5. Rewrite the `README.md`
6. If the project is not an executable, delete the files:
   * `src/project_name/main.py`
   * `src/project_name/logger.py`
   * `src/project_name/logger_config.toml`
   * `src/project_name/config.py`
   * `python-dotenv` and `tomli` as dependencies in `pyproject.toml` (unless otherwise needed)
