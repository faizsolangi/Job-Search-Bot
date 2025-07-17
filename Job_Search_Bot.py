import requests

ZAPIER_WEBHOOK_URL = "https://hooks.zapier.com/hooks/catch/23715689/u2kede0/"  # Replace with your Zapier URL

# Define your keywords here
KEYWORDS = ["agentic ai", "langchain", "python"]

def keyword_match(job):
    """Returns True if any keyword is found in job title, tags or description."""
    combined_text = (
        (job.get("position") or "") + " " +
        " ".join(job.get("tags") or []) + " " +
        (job.get("description") or "")
    ).lower()
    
    return any(keyword.lower() in combined_text for keyword in KEYWORDS)

def fetch_remoteok_jobs():
    print("Fetching jobs from RemoteOK...")
    try:
        response = requests.get("https://remoteok.com/api")
        jobs = response.json()[1:]  # Skip metadata
        matched_jobs = []

        for job in jobs:
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
                # 🔥 Send to Zapier
                requests.post(ZAPIER_WEBHOOK_URL, json=job_data)

        print(f"Filtered and sent {len(matched_jobs)} matching jobs to Zapier.")

    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    fetch_remoteok_jobs()
