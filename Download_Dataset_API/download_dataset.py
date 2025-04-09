import requests
import json
import pandas as pd

# === API Configuration ===
url = "https://apithunder.makecontact.space/SearchRecord"
CS_API_KEY = "1abnshqn1rmv243kbuq6i5bq6xyfdexpx58un5kc6qllp"

headers = {
    "Content-Type": "application/x-www-form-urlencoded",
    "x-api-key": CS_API_KEY
}

# === Initiative & Dataset Config ===
initiatives = [
    # Ipoh
    {"initiative_id": "1764", "dataset_id": ""},
    # Cheras
    {"initiative_id": "1763", "dataset_id": ""},
    # JB
    {"initiative_id": "1758", "dataset_id": ""},
    # Kedah
    {"initiative_id": "1797", "dataset_id": ""},
    # KL
    {"initiative_id": "1765", "dataset_id": ""},
    # Melaka
    {"initiative_id": "1766", "dataset_id": ""},
    # Miri
    {"initiative_id": "1808", "dataset_id": ""},
    # Penang
    {"initiative_id": "1757", "dataset_id": ""},
    # Sabah
    {"initiative_id": "1767", "dataset_id": ""},
    # Sarawak
    {"initiative_id": "1768", "dataset_id": ""},
    # Selangor
    {"initiative_id": "1769", "dataset_id": ""},
    # Seremban
    {"initiative_id": "1770", "dataset_id": ""},
    # Telemarketing
    {"initiative_id": "1772", "dataset_id": ""},
]

# === Download Data for Each Initiative ===
for item in initiatives:
    initiative_id = item["initiative_id"]
    dataset_id = item["dataset_id"]

    # Dynamically set the column name for original_id
    dynamic_column = f"cs_{initiative_id}_original_id"
    desired_columns = [
        "OutcomeName", "DataSetName", "Id", dynamic_column, "OutcomeId",
        "OutcomeUpdateDateTime", "CallId", "Assigned", "Attempts", "record_id",
        "upload_date", "region", "applied_date", "source_platform", "applicant_name",
        "ads_role", "clean_role", "hunt", "phone_number", "applied_email", "reject_reason",
        "applicant_age", "applicant_education_level", "applicant_expected_salary",
        "interview_date", "interview_time", "interview_type", "interviewer",
        "interview_additional_note", "applicant_sales_experience", "applicant_work_experience_year",
        "applicant_notice_period", "created_time", "clean_ads", "omni_platform", "whatsapp_outcome"
    ]

    all_records = []
    page = 1
    more_records = True

    print(f"\n🚀 Fetching Initiative {initiative_id} (Dataset {dataset_id})...")

    while more_records:
        payload = {
            "datasetid": dataset_id,
            "initiativeid": initiative_id,
            "jsondata": '{}',
            "activeonly": "true",
            "page": str(page)
        }

        response = requests.post(url, headers=headers, data=payload)

        if response.status_code == 200:
            try:
                data = response.json()
                records = data.get("info", {}).get("records", [])
                meta = data.get("info", {}).get("info", {})

                for record in records:
                    record["OutcomeName"] = record.get("Outcome", "")
                    record["DataSetName"] = "TM Applicant Dataset"

                all_records.extend(records)
                print(f"📥 Page {page} fetched. Total records so far: {len(all_records)}")

                if meta.get("more_records") == "1":
                    page += 1
                else:
                    more_records = False

            except json.JSONDecodeError:
                print("❌ Invalid JSON on page", page)
                break
        else:
            print(f"❌ HTTP Error {response.status_code} on page {page}")
            break

    # === Save to CSV ===
    if all_records:
        df = pd.DataFrame(all_records)

        # Add missing columns if needed
        for col in desired_columns:
            if col not in df.columns:
                df[col] = ""

        # Ensure the correct column header appears
        df = df.rename(columns={dynamic_column: dynamic_column})
        df = df[desired_columns]

        output_file = fr"C:\Users\Omniuser\Downloads\Data Download - Initiative _ {initiative_id} - All Data Sets.csv"
        df.to_csv(output_file, index=False)
        print(f"✅ Saved: {output_file} (Total records: {len(df)})")
    else:
        print(f"⚠️ No records found for Initiative {initiative_id}.")
