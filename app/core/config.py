from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    APP_NAME: str = "knowledge-updater"
    ENV: str = "development" # development / staging / production

    # ===== 向量库配置 =====
    CHROMA_PERSIST_DIR: str = "./chroma_db"
    CHROMA_COLLECTION: str = "faq"

    # ===== 数据源配置 =====
    FAQ_EXCEL_PATH: str = "./data/faq.xlsx"
    UPDATE_CHECK_INTERVAL: int = 300  # 5 分钟

    # ===== 通知配置 =====
    SLACK_WEBHOOK_URL: Optional[str] = None  # 生产环境才有

    # ===== LLM 配置 =====
    OPENAI_API_KEY: Optional[str] = None

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"  # 忽略 .env 里未定义的字段

settings = Settings()