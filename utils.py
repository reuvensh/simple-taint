import time
from pathlib import Path


def file_write(item_id: str, file_content: str) -> bool:
    # writes to file - danger of directory traversal
    if Path("items", f"{item_id}").exists():
        with open(Path("items", f"@{item_id}"), "w") as f:  # sink
            time.sleep(1)
            f.write(file_content)
        return True
    else:
        time.sleep(0.1)
        return False
