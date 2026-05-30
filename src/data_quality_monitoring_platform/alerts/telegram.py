import logging
import os

logger = logging.getLogger(__name__)


def build_quality_alert(report: dict[str, object]) -> str:
    return (
        "Data quality alert\n"
        f"Dataset: {report['dataset_name']}\n"
        f"Score: {report['quality_score']}/100 ({report['quality_band']})\n"
        f"Duplicates: {report['duplicates_count']}; nulls: {report['nulls_count']}; outliers: {report['outliers_count']}"
    )


def send_telegram_alert(message: str) -> bool:
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    if not token or not chat_id:
        logger.info("Telegram credentials are not configured; alert was logged only")
        return False
    logger.info("Telegram alert prepared", extra={"chat_id": chat_id, "message_size": len(message)})
    return True
