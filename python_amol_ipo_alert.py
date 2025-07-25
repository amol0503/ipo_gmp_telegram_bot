import requests
from bs4 import BeautifulSoup
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import re

# === CONFIGURATION ===
YOUR_TELEGRAM_BOT_TOKEN = '8376259524:AAE1kubs1Rx5muun_QBUYYxvvb5AOWZybLo'
YOUR_CHAT_ID = '1067971086'  # Not used in this version, we reply directly to user

# === Function to get IPO Data ===
def get_ipo_data():
    url = "https://ipowatch.in/ipo-grey-market-premium-latest-ipo-gmp/"
    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    rows = soup.find_all("tr")
    good_ipos = []

    for row in rows:
        cols = row.find_all("td")
        if len(cols) >= 4:
            ipo_name = cols[0].get_text(strip=True)
            gmp_value = cols[3].get_text(strip=True)

            # Extract percentage from GMP string
            match = re.search(r'(\d+)%', gmp_value)
            if match:
                percent = int(match.group(1))
                if percent > 30:
                    good_ipos.append(f"{ipo_name} - GMP {percent}%")

    return good_ipos

# === Telegram Command Handler ===
async def gmp_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ipo_list = get_ipo_data()

    if ipo_list:
        message = "🚀 IPOs with GMP > 30%:\n\n" + "\n".join(ipo_list)
    else:
        message = "ℹ️ No IPOs today with GMP > 30%"

    await update.message.reply_text(message)

# === Main Bot Runner ===
def main():
    app = ApplicationBuilder().token(YOUR_TELEGRAM_BOT_TOKEN).build()

    # Register command
    app.add_handler(CommandHandler("gmp", gmp_handler))

    # Run bot until manually stopped
    print("Bot is running... Type /gmp in your Telegram to test.")
    app.run_polling()

# === Run it ===
if __name__ == "__main__":
    main()