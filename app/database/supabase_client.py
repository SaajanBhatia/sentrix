import os
from supabase import create_client, Client
from dotenv import load_dotenv
from ..utils import CustomLogger

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")


class SupabaseClient:
    def __init__(self, logger: CustomLogger) -> None:
        self.supabase: Client = create_client(
            SUPABASE_URL, SUPABASE_KEY)
        self.logger = logger
