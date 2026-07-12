from config import Config
from core.logger import setup_logger
from core.pipeline import TradingPipeline

logger = setup_logger("GoldBot")


class GoldBot:
    """
    GoldBot — main orchestrator.

    Wires the real TradingPipeline (Data -> Context -> Strategy ->
    Signal -> AI -> Decision -> Risk -> Telegram Format -> Telegram
    Delivery -> Persistence) as the v0.1 entry point. No business
    logic lives here; all of it belongs to core.pipeline.TradingPipeline
    and the layers it wires.
    """

    def __init__(self):
        self.pipeline = TradingPipeline(
            symbol="XAUUSD",
            interval="M15",
            outputsize=Config.TIMEFRAME_HISTORY["M15"],
            send_notifications=True,
            persist_signals=True,
        )

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
            result = self.pipeline.run()
            logger.info(
                f"GoldBot run cycle completed: "
                f"{len(result['signals'])} signal(s), "
                f"{len(result['decisions'])} decision(s), "
                f"{len(result['telegram_messages'])} telegram message(s)."
            )
            return result

        except Exception as e:
            logger.error(f"GoldBot run failed: {e}")
            raise


if __name__ == "__main__":
    bot = GoldBot()
    bot.run()
