import logging
from dataclasses import dataclass
from enum import Enum, auto

from fastapi import FastAPI
from utils import file_write

app = FastAPI()

class Format(Enum):
    LOWERCASE = auto()
    UPPERCASE = auto()
    LEAVE_AS_IS = auto()

@dataclass
class DbWriteResult:
    success: bool
    message: str

@app.get("/add_item/{item_id}")
async def add_file_for_item(item_id: str, file_content: str, use_input_values: bool):  # source
    if use_input_values:
        write_result = log_and_write_to_file(item_id=item_id, file_content=file_content, format=Format.UPPERCASE)
    else:
        write_result = write_safe_data_to_file(item_id=item_id, file_content=file_content)
    return {"message": f"processed {item_id}. If a file was held for the item, we added this information to the file"}

def write_to_file(item_id: str, file_content_value: str, format: Format = Format.LEAVE_AS_IS) -> DbWriteResult:
    # writes the data to the database
    if format is Format.UPPERCASE:
        formatted_file_content = file_content_value.upper()
    elif format is Format.LOWERCASE:
        formatted_file_content = file_content_value.lower()
    else:
        formatted_file_content = file_content_value
    success = file_write(item_id=item_id, file_content=formatted_file_content)
    return DbWriteResult(success=success, message="db write performed")

def log_and_write_to_file(item_id: str, file_content: str, format: Format) -> DbWriteResult:
    # propagates the data on to the next function
    logging.info(f"writing to db about item", extra={"item_id": item_id})
    return write_to_file(item_id, file_content_value=file_content, format=format)

def write_safe_data_to_file(item_id: str, file_content: str) -> DbWriteResult:
    # doesn't write the risky (string) input to the database
    logging.info("ignoring the item input", extra={"item_id": item_id, "file_content_size": len(file_content)})
    return write_to_file(item_id="safe item", file_content_value="safe data")
