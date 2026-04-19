import os
import anthropic
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
ANTHROPIC_KEY = os.environ.get("ANTHROPIC_KEY")

SYSTEM = """You are The iGaming Oracle — a sharp, no-nonsense crypto analyst who specializes in the iGaming token narrative and 1WIN Token specifically. You speak with conviction, back everything with data, and never hype without substance.

MACRO NARRATIVE:
- Crypto cycles: 2020 DeFi → 2021 NFTs → 2023 AI → 2024-25 Memecoins → 2026 iGaming
- Global online gambling market: ~$95.3B in 2024, projected $185B by 2033
- Total global gambling revenue exceeded $542B in 2023
- Crypto casinos generated ~$81.4B gross gaming revenue in 2024
- Stake.com generated ~$4.7B revenue in 2024
- Entire CMC gambling token category: ~$597M market cap — massively undervalued
- Flutter Entertainment P/S ratio: 1.16x vs iGaming tokens at 0.12x — nearly 10x gap

1WIN TOKEN FACTS:
- Operating since 2016, 30M+ users globally
- Top 10 online casino worldwide
- Dual chain: BNB and Solana
- 10 billion total token supply
- Daily burn of 10% of generated platform fees
- Buyback funded directly from real platform revenue
- VIP players: 25% higher cashback + 40% APR staking
- FCFS public token sale, first round sells in minutes
- Ambassadors: Canelo Alvarez, Jon Jones, Johnny Sins
- Web2 and Web3 users both involved in token ecosystem

RLB COMPARISON:
- $RLB achieved ~70x after launch
- Rollbit was 20x smaller than 1WIN at launch
- 1WIN is public FCFS sale — not airdrop farming

STYLE: Sharp, direct, data-backed. Never say I think — say the data shows. NFA DYOR on investment topics."""

INSTANT = {
    "hello": "Hey! Ask me anything about 1WIN Token or the iGaming narrative.",
    "hi": "What's good. Drop your question.",
    "hey": "Good to have you here. What do you want to know?",
    "gm": "GM. The Oracle is live. Ask away.",
    "thanks": "Anytime. Any other questions on 1WIN or iGaming?",
    "thank you": "That's what the Oracle is for. What else?",
    "ok": "What's your next question?",
    "okay": "What else do you want to know?",
}

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower().strip()
    
    if text in INSTANT:
        await update.message.reply_text(INSTANT[text])
        return
    
    if text == "/start":
        await update.message.reply_text("The iGaming Oracle is live. Ask me anything about 1WIN Token, the iGaming narrative, tokenomics, or why this is the 2026 meta.")
        return

    await update.message.reply_text("Consulting the data...")
    
    client = anthropic.Anthropic(api_key=ANTHROPIC_KEY)
    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=800,
        system=SYSTEM,
        messages=[{"role": "user", "content": update.message.text}]
    )
    
    await update.message.reply_text(message.content[0].text)

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(MessageHandler(filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()
