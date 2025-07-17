import requests
import csv

ZAPIER_WEBHOOK_URL = "https://hooks.zapier.com/hooks/catch/23715689/u2kede0/"  # Replace with your actual Zap URL

def fetch_remoteok_jobs():
    print("Fetching jobs from RemoteOK...")
    try:
        response = requests.get("https://remoteok.com/api")
        jobs = response.json()[1:]  # Skip metadata
        job_list = []

        for job in jobs:
            job_data = {
                "job_title": job.get("position", ""),
                "company_name": job.get("company", ""),
                "job_url": job.get("url", ""),
                "tags": ", ".join(job.get("tags", [])),
                "location": job.get("location", ""),
                "date_posted": job.get("date", "")
            }

            job_list.append(job_data)

            # 🔥 Send to Zapier
            requests.post(ZAPIER_WEBHOOK_URL, json=job_data)

        print(f"Sent {len(job_list)} jobs to Google Sheets via Zapier.")

    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    fetch_remoteok_jobs()

