from datetime import datetime, timezone

DEFAULT_CATEGORIES = [
    {"category": "Mobile Phones", "typical_min_price": 15000, "typical_max_price": 250000},
    {"category": "Electronics", "typical_min_price": 5000, "typical_max_price": 150000},
    {"category": "Vehicles", "typical_min_price": 300000, "typical_max_price": 5000000},
    {"category": "Furniture", "typical_min_price": 3000, "typical_max_price": 80000},
    {"category": "Fashion", "typical_min_price": 500, "typical_max_price": 20000},
    {"category": "Property/Rent", "typical_min_price": 15000, "typical_max_price": 500000},
    {"category": "Other", "typical_min_price": 1000, "typical_max_price": 50000},
]

def seed_categories():
    """Run once to populate category_price_references. Safe to re-run — clears and reinserts."""
    try:
        from db import db
        if db is not None:
            category_price_references = db["category_price_references"]
            category_price_references.delete_many({})
            for cat in DEFAULT_CATEGORIES:
                cat["updated_at"] = datetime.now(timezone.utc).isoformat()
            category_price_references.insert_many(DEFAULT_CATEGORIES)
            print(f"Seeded {len(DEFAULT_CATEGORIES)} categories")
    except Exception as e:
        print(f"Could not seed categories to DB: {e}")

def get_reference(category: str):
    try:
        from db import db
        if db is not None:
            ref = db["category_price_references"].find_one({"category": category})
            if ref:
                return ref
    except Exception:
        pass

    # Fallback to in-memory DEFAULT_CATEGORIES if DB is offline or category not in DB
    for cat in DEFAULT_CATEGORIES:
        if cat["category"] == category:
            return cat
    return None

if __name__ == "__main__":
    seed_categories()