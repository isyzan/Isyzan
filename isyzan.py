import requests
import re
import random
import sys

print("🚀 ISYZAN VPN START", flush=True)

try:
    url = 'https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000'
    print("📡 Загружаю список прокси...", flush=True)
    
    response = requests.get(url, timeout=15)
    text = response.text
    
    proxies = re.findall(r'\d+\.\d+\.\d+\.\d+:\d+', text)
    print(f"✅ Найдено {len(proxies)} прокси", flush=True)
    
    if not proxies:
        print("❌ Нет прокси", flush=True)
        with open('isyzan_config.ovpn', 'w') as f:
            f.write("# ISYZAN VPN - Нет рабочих прокси")
        sys.exit(0)
    
    random.shuffle(proxies)
    success = False
    
    for proxy in proxies[:20]:
        try:
            print(f"🔍 Проверяю: {proxy}", flush=True)
            
            test = requests.get(
                'https://httpbin.org/ip',
                proxies={'http': proxy, 'https': proxy},
                timeout=3
            )
            
            if test.status_code == 200:
                print(f"✅ РАБОЧИЙ: {proxy}", flush=True)
                
                config = f"""# ISYZAN VPN CONFIG
# Сервер: {proxy}
client
dev tun
proto tcp
remote {proxy}
resolv-retry infinite
nobind
persist-key
persist-tun
remote-cert-tls server
cipher AES-256-CBC
verb 3
<auth-user-pass>
isyzan
isyzan
</auth-user-pass>
"""
                with open('isyzan_config.ovpn', 'w') as f:
                    f.write(config)
                
                print("✅ КОНФИГ СОЗДАН", flush=True)
                success = True
                break
                
        except Exception as e:
            print(f"⚠️ Ошибка: {str(e)[:40]}", flush=True)
            continue
    
    if not success:
        print("❌ Нет рабочих прокси", flush=True)
        with open('isyzan_config.ovpn', 'w') as f:
            f.write("# ISYZAN VPN - Попробуй позже")
        
except Exception as e:
    print(f"❌ ОШИБКА: {str(e)[:100]}", flush=True)
    with open('isyzan_config.ovpn', 'w') as f:
        f.write(f"# ISYZAN VPN - Ошибка: {str(e)[:100]}")

print("✅ ISYZAN VPN ЗАВЕРШЁН", flush=True)
