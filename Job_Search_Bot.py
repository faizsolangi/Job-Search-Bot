# job_search_bot.py

import requests
import csv
from datetime import datetime

# Define APIs to query
APIS = {
    "RemoteOK": "https://remoteok.com/api",
}

def fetch_remoteok():
    print("Fetching jobs from RemoteOK...")
    try:
        response = requests.get(APIS["RemoteOK"])
        jobs = response.json()[1:]  # skip metadata object
        results = []
        for job in jobs:
            results.append({
                "source": "RemoteOK",
                "title": job.get("position"),
                "company": job.get("company"),
                "url": job.get("url"),
                "tags": ", ".join(job.get("tags", [])),
                "date_posted": job.get("date")
            })
        return results
    except Exception as e:
        print("Error fetching RemoteOK:", e)
        return []

def save_to_csv(jobs, filename="job_results.csv"):
    print(f"Saving {len(jobs)} jobs to {filename}...")
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["source", "title", "company", "url", "tags", "date_posted"])
        writer.writeheader()
        writer.writerows(jobs)

if __name__ == "__main__":
    all_jobs = fetch_remoteok() + fetch_remotive()
    save_to_csv(all_jobs)
    print("Job scraping complete.")
