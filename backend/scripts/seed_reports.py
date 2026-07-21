"""
Script to seed the Supabase database with mock reports for the dashboard demo.
"""
import asyncio
import random
from datetime import datetime, timedelta
from app.services.supabase_service import supabase_service
from app.core.constants import SCAM_SCRIPT_LABELS, RISK_THRESHOLDS

CITIES = [
    {"name": "Delhi", "lat": 28.6139, "lng": 77.209},
    {"name": "Mumbai", "lat": 19.076, "lng": 72.8777},
    {"name": "Bengaluru", "lat": 12.9716, "lng": 77.5946},
    {"name": "Hyderabad", "lat": 17.385, "lng": 78.4867},
    {"name": "Chennai", "lat": 13.0827, "lng": 80.2707},
]

async def seed_reports(count=50):
    supabase_service.connect()
    
    if supabase_service.use_fallback:
        print("Supabase is not configured or available. Cannot seed.")
        return

    print(f"Seeding {count} reports...")
    now = datetime.utcnow()
    
    for i in range(count):
        risk = random.choice(["CRITICAL", "HIGH", "MEDIUM", "LOW"])
        score_ranges = {
            "CRITICAL": (85, 99),
            "HIGH": (65, 84),
            "MEDIUM": (40, 64),
            "LOW": (5, 39)
        }
        score = random.randint(*score_ranges[risk])
        city = random.choice(CITIES)
        created_at = now - timedelta(minutes=random.randint(1, 10000))
        
        report = {
            "id": f"SA-{10000 + i}",
            "created_at": created_at.isoformat() + "Z",
            "scam_type": random.choice(SCAM_SCRIPT_LABELS),
            "risk_level": risk,
            "risk_score": score,
            "language": "English",
            "source": random.choice(["WhatsApp", "IVR", "Dashboard"]),
            "city": city["name"],
            "lat": city["lat"] + (random.random() - 0.5) * 0.1,
            "lng": city["lng"] + (random.random() - 0.5) * 0.1,
            "amount_involved": random.choice([0, 25000, 50000, 120000, 300000]),
            "status": random.choice(["New", "Under Review", "Escalated", "Resolved"])
        }
        
        result = await supabase_service.log_fraud_report(report)
        if result["status"] == "success":
            print(f"Logged {report['id']}")
        else:
            print(f"Failed to log {report['id']}: {result}")
            
    print("Done seeding reports.")

if __name__ == "__main__":
    asyncio.run(seed_reports())
