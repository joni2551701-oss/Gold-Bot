from config import Config
from core.logger import setup_logger
from goldbot.core_layer.pipeline import TradingPipeline
from monitoring.resource_monitor import record_process_start

logger = setup_logger("GoldBot")

logger.info("GoldBot starting...")
logger.info("Configuration loaded.")


class GoldBot:
    """
    GoldBot — main orchestrator.

    Wires the real TradingPipeline (Data -> Context -> Strategy ->
    Signal -> AI -> Decision -> Risk -> Telegram Format -> Telegram
    Delivery -> Persistence) as the v0.1 entry point. No business
    logic lives here; all of it belongs to goldbot.core_layer.pipeline.TradingPipeline
    and the layers it wires.
    """

    def __init__(self):
        record_process_start()
        self.pipeline = TradingPipeline(
            symbol="XAUUSD",
            interval="M15",
            outputsize=Config.TIMEFRAME_HISTORY["M15"],
            send_notifications=True,
            persist_signals=True,
        )
        logger.info("Trading Pipeline initialized.")

    def run(self):
        """
        Runs one full pipeline cycle. TradingPipeline.run() is
        synchronous (it bridges to Telegram's async delivery
        internally via Notifier), so this stays synchronous too --
        wrapping it in asyncio.run() would raise "asyncio.run()
        cannot be called from a running event loop" as soon as
        Notifier.send_message() makes its own asyncio.run() call.
        """
        logger.info("GoldBot started")

        try:
            logger.info("Starting pipeline...")
            result = self.pipeline.run()
            logger.info("Pipeline finished.")
            logger.info(
                f"GoldBot run cycle completed: "
                f"{len(result['signals'])} signal(s), "
                f"{len(result['decisions'])} decision(s), "
                f"{len(result['telegram_messages'])} telegram message(s)."
            )
            return result

        except Exception as e:
            # Fatal for this run (re-raised below): logger.exception()
            # attaches the stack trace to the same log record, same
            # message text and control flow as before.
            logger.exception(f"GoldBot run failed: {e}")
            raise
        finally:
            logger.info("GoldBot finished.")


if __name__ == "__main__":
    bot = GoldBot()
    bot.run()
