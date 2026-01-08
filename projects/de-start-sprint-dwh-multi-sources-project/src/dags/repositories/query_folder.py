from pathlib import Path


class QueryFolder:
    def __init__(self):
        self.sql_dir = Path(__file__).parent.parent / "sql"

    def load_sql_file(self, filename: str) -> str:
        """load sql file"""
        file_path = self.sql_dir / filename
        if not file_path.exists():
            raise FileNotFoundError(f"SQL file not found: {file_path}")
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read().strip()
