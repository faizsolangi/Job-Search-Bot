from datetime import datetime, timedelta
import requests

ZAPIER_WEBHOOK_URL = "https://hooks.zapier.com/hooks/catch/23715689/u2kede0/"  # Replace
KEYWORDS = ["agentic ai", "langchain", "python"]

def keyword_match(job):
    combined_text = (
        (job.get("position") or "") + " " +
        " ".join(job.get("tags") or []) + " " +
        (job.get("description") or "")
    ).lower()
    return any(keyword.lower() in combined_text for keyword in KEYWORDS)

def is_recent(job_date_str):
    try:
        job_time = datetime.fromisoformat(job_date_str.replace("Z", "+00:00"))
        return job_time >= datetime.utcnow() - timedelta(hours=2)
    except:
        return False

def fetch_remoteok_jobs():
    print("Fetching jobs from RemoteOK...")
    try:
        response = requests.get("https://remoteok.com/api")
        jobs = response.json()[1:]  # Skip metadata
        matched_jobs = []

        for job in jobs:
            if not is_recent(job.get("date", "")):
                continue
            if keyword_match(job):
                job_data = {
                    "job_title": job.get("position", ""),
                    "company_name": job.get("company", ""),
                    "job_url": job.get("url", ""),
                    "tags": ", ".join(job.get("tags", [])),
                    "location": job.get("location", ""),
                    "date_posted": job.get("date", "")
                }

                matched_jobs.append(job_data)
                requests.post(ZAPIER_WEBHOOK_URL, json=job_data)

        print(f"Filtered and sent {len(matched_jobs)} matching jobs to Zapier.")

    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    fetch_remoteok_jobs()

