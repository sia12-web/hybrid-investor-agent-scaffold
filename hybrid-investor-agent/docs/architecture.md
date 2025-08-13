
# Phase 0 Architecture (Concise)

- **TradingView (Pine)** -> Webhook (FastAPI) -> Risk Sizing -> Venue Router (OANDA/Gemini)
- LLM (GPT-5) used for pre-trade sanity & post-trade journaling (non-blocking in scaffold).

Artifacts here are placeholders to unblock setup and paper testing.
