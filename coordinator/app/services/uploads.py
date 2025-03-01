import csv
import io
import asyncio
from fastapi import APIRouter, UploadFile, File, BackgroundTasks, HTTPException
from app.logic import task_manager
from app.logic.output_writer import output_writer

router = APIRouter()


async def process_hashes_and_write_output(hashes: list, file_name: str) -> None:

    output_rows = []
    for hash_value in hashes:
        result = await task_manager.process_hash_task(hash_value)
        if result and result.get("found"):
            cracked = result.get("phone_number", "Not Found")
        else:
            cracked = "Not Found"
        output_rows.append([hash_value, cracked])
    output_writer(output_rows, file_name)


def sync_process_hashes_and_write_output(hashes: list, file_name: str) -> None:
    asyncio.run(process_hashes_and_write_output(hashes, file_name))


@router.post("/")
async def upload_file(
    file: UploadFile = File(...), background_tasks: BackgroundTasks = None
):
    if file.content_type != "text/csv":
        raise HTTPException(
            status_code=400, detail="Invalid file type. Please upload a CSV file."
        )

    content = await file.read()
    file_data = io.StringIO(content.decode("utf-8"))
    reader = csv.reader(file_data)
    hashes = [row[0] for row in reader if row]

    if not hashes:
        raise HTTPException(status_code=400, detail="No valid hashes found in file.")

    background_tasks.add_task(
        sync_process_hashes_and_write_output, hashes, file.filename
    )

    return {"message": "Tasks scheduled", "hashes": hashes}
