import csv
import os
from typing import List


def output_writer(output_rows: List[List[str]], original_file_name: str) -> str:

    base_name = os.path.splitext(original_file_name)[0]
    output_file = f"cracked_{base_name}.csv"

    with open(output_file, mode="w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["hash", "cracked_password"])
        writer.writerows(output_rows)

    output_path = os.path.abspath(output_file)
    print(f"Output file written to {output_path}")
    return output_path
