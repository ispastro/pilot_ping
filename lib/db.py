import os
from supabase import create_client

url = os.environ["SUPABASE_URL"]
key = os.environ["SUPABASE_KEY"]
supabase = create_client(url, key)

def add_subscriber(chat_id: int):
    supabase.table("subscribers").upsert({"chat_id": chat_id}).execute()

def remove_subscriber(chat_id: int):
    supabase.table("subscribers").delete().eq("chat_id", chat_id).execute()

def get_subscribers() -> list[int]:
    res = supabase.table("subscribers").select("chat_id").execute()
    return [row["chat_id"] for row in res.data]

def is_subscriber(chat_id: int) -> bool:
    res = supabase.table("subscribers").select("chat_id").eq("chat_id", chat_id).execute()
    return len(res.data) > 0

def is_new_job(text: str, link: str) -> bool:
    res = supabase.table("jobs").select("id").eq("text", text).eq("link", link).execute()
    if not res.data:
        supabase.table("jobs").insert({"text": text, "link": link}).execute()
        return True
    return False
