import csv
import os
import xml.etree.ElementTree as ET

import psycopg2
import requests
from dotenv import load_dotenv
from psycopg2.extras import execute_values

load_dotenv()

#direct bulk download for Reading Local Authority
BULK_URL = "https://ratings.food.gov.uk/OpenDataFiles/FHRS884en-GB.xml"
CSV_FILENAME = "csvs/reading_food_ratings.csv"
TABLE_NAME = "reading_food_ratings"

DB_URL_ENV_VAR = "SUPABASE_DB_URL"

FIELD_MAP = {
    "FHRSID": "FHRSID",
    "BusinessName": "BusinessName",
    "BusinessType": "BusinessType",
    "AddressLine1": "AddressLine1",
    "AddressLine2": "AddressLine2",
    "AddressLine3": "AddressLine3",
    "PostCode": "PostCode",
    "RatingValue": "RatingValue",
    "RatingDate": "RatingDate",
    "LocalAuthorityName": "LocalAuthorityName",
    "Hygiene": ".//Scores/Hygiene",
    "Structural": ".//Scores/Structural",
    "ConfidenceInManagement": ".//Scores/ConfidenceInManagement",
    "Longitude": ".//Geocode/Longitude",
    "Latitude": ".//Geocode/Latitude",
}

# Columns that should be numbers in the database (blank -> NULL, never 0)
INT_COLUMNS = {"FHRSID", "Hygiene", "Structural", "ConfidenceInManagement"}
FLOAT_COLUMNS = {"Longitude", "Latitude"}

def fetch_establishments(url=BULK_URL):
    #Download the FHRS XML and return the list of EstablishmentDetail elements.
    response = requests.get(url, timeout=60)
    response.raise_for_status()
    root = ET.fromstring(response.content)
    return root.findall(".//EstablishmentDetail")

def build_rows(establishments):
    # Turn XML elements into a list of dicts keyed by column name.
    return [
        {
            col: (est.findtext(path) or "").strip()
            for col, path in FIELD_MAP.items()
        }
        for est in establishments
    ]

def write_csv(rows, filename=CSV_FILENAME):
    #Write the rows to a CSV file
    with open(filename, mode="w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=list(FIELD_MAP.keys()))
        writer.writeheader()
        writer.writerows(rows)

def _clean_value(col, value):
    #for supabase: convert a csv style string to the right Python type. Blanks become None/NULL
    if value == "":
        return None
    try:
        if col in INT_COLUMNS:
            return int(value)
        if col in FLOAT_COLUMNS:
            return float(value)
    except ValueError:
        return None
    return value

def get_connection():
    #open a connection to Supabase using the URL stored in an environment variable
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
            id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
            FHRSID BIGINT NOT NULL,
            BusinessName TEXT,
            BusinessType TEXT,
            AddressLine1 TEXT,
            AddressLine2 TEXT,
            AddressLine3 TEXT,
            PostCode TEXT,
            RatingValue TEXT,
            RatingDate DATE,
            LocalAuthorityName TEXT,
            Hygiene INTEGER,
            Structural INTEGER,
            ConfidenceInManagement INTEGER,
            Longitude DOUBLE PRECISION,
            Latitude DOUBLE PRECISION,
            first_seen DATE NOT NULL DEFAULT CURRENT_DATE,
            UNIQUE NULLS NOT DISTINCT (FHRSID, RatingDate, RatingValue)
        );
        """
    )

def push_to_supabase(rows):
    columns = list(FIELD_MAP.keys())
    values = [[_clean_value(col, row[col]) for col in columns] for row in rows]

    conn = get_connection()
    try:
        with conn, conn.cursor() as cur:
            create_table(cur)
            cur.execute(f"SELECT COUNT(*) FROM {TABLE_NAME};")
            before = cur.fetchone()[0]

            execute_values(
                cur,
                f"""
                INSERT INTO {TABLE_NAME} ({', '.join(columns)}) VALUES %s
                ON CONFLICT (FHRSID, RatingDate, RatingValue) DO NOTHING
                """,
                values,
                page_size=1000,
            )

            cur.execute(f"SELECT COUNT(*) FROM {TABLE_NAME};")
            print(f"{cur.fetchone()[0] - before} new rating rows added.")
    finally:
        conn.close()

def main():
    establishments = fetch_establishments()
    rows = build_rows(establishments)

    write_csv(rows)
    print(f"Scraping done. {len(rows)} total rows. CSV saved to {CSV_FILENAME}.")

    push_to_supabase(rows)
    print(f"Pushed {len(rows)} rows to Supabase table '{TABLE_NAME}'.")

if __name__ == "__main__":
    main()