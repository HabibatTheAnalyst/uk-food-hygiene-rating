import csv
import os
import xml.etree.ElementTree as ET

import psycopg2
import requests
from dotenv import load_dotenv
from psycopg2.extras import execute_values

load_dotenv()

DESCRIPTORS_URL = "https://ratings.food.gov.uk/open-data-resources/lookupData/ScoreDescriptors.xml"
CSV_FILENAME = "csvs/score_descriptors.csv"
TABLE_NAME = "score_descriptors"
DB_URL_ENV_VAR = "SUPABASE_DB_URL"

FIELD_MAP = {
    "description": "Description",
    "id": "Id",
    "score": "Score",
    "scorecategory": "ScoreCategory",
}

INT_COLUMNS = {"id", "score"}

def fetch_descriptors(url=DESCRIPTORS_URL):
    # Download the lookup XML and return the descriptor elements
    response = requests.get(url, timeout=60)
    response.raise_for_status()
    print(f"Response status: {response.status_code}")
    root = ET.fromstring(response.content)
    return root.findall("./scoreDescriptors/scoreDescriptors")

def build_rows(descriptors):
    return [
        {
            col: (descriptor.findtext(path) or "").strip()
            for col, path in FIELD_MAP.items()
        }
        for descriptor in descriptors
    ]

def write_csv(rows, filename=CSV_FILENAME):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, mode="w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=list(FIELD_MAP.keys()))
        writer.writeheader()
        writer.writerows(rows)

def _clean_value(col, value):
    # Blanks become None/NULL; id and score become integers
    if value == "":
        return None
    if col in INT_COLUMNS:
        try:
            return int(value)
        except ValueError:
            return None
    return value

def get_connection():
    db_url = os.environ.get(DB_URL_ENV_VAR)
    if not db_url:
        raise RuntimeError(
            f"Set the {DB_URL_ENV_VAR} environment variable to your Supabase connection string."
        )
    return psycopg2.connect(db_url)

def create_table(cur):
    cur.execute(
        f"""
        CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
            id INTEGER PRIMARY KEY,
            description TEXT,
            score INTEGER NOT NULL,
            scorecategory TEXT NOT NULL,
            UNIQUE (scorecategory, score)
        );
        """
    )

def push_to_supabase(rows):
    # Upsert: new descriptors are added, changed ones are updated, nothing is duplicated
    columns = list(FIELD_MAP.keys())
    values = [[_clean_value(col, row[col]) for col in columns] for row in rows]

    conn = get_connection()
    try:
        with conn, conn.cursor() as cur:
            create_table(cur)
            execute_values(
                cur,
                f"""
                INSERT INTO {TABLE_NAME} ({', '.join(columns)}) VALUES %s
                ON CONFLICT (id) DO UPDATE SET
                    description = EXCLUDED.description,
                    score = EXCLUDED.score,
                    scorecategory = EXCLUDED.scorecategory
                """,
                values,
            )
    finally:
        conn.close()

def main():
    descriptors = fetch_descriptors()
    rows = build_rows(descriptors)

    write_csv(rows)
    print(f"Scraping done. {len(rows)} total rows. CSV saved to {CSV_FILENAME}.")

    push_to_supabase(rows)
    print(f"Pushed {len(rows)} rows to Supabase table '{TABLE_NAME}'.")

if __name__ == "__main__":
    main()