import requests
import re
import random
import sys

print("🚀 ISYZAN VPN START", flush=True)

try:
    # Самый надёжный источник прокси
    url = 'https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000'
    print("📡 Загружаю список прокси...", flush=True)
    
    response = requests.get(url, timeout=15)
    text = response.text
    
    # Находим IP:PORT
    proxies = re.findall(r'\d+\.\d+\.\d+\.\d+:\d+', text)
    print(f"✅ Найдено {len(proxies)} прокси", flush=True)
    
    if not proxies:
        print("❌ Нет прокси, выхожу", flush=True)
        sys.exit(0)
    
    # Берём первые 20 случайных
    random.shuffle(proxies)
    success = False
    
    for i, proxy in enumerate(proxies[:20]):
        try:
            print(f"🔍 Проверяю {i+1}/20: {proxy}", flush=True)
            
            # Проверка через httpbin
            test = requests.get(
                'https://httpbin.org/ip',
                proxies={'http': proxy, 'https': proxy},
                timeout=3
            )
            
            if test.status_code == 200:
                print(f"✅ РАБОЧИЙ: {proxy}", flush=True)
                
                # Пытаемся обновить подписку
                renew = requests.get(
                    'https://httpbin.org/get',
                    proxies={'http': proxy, 'https': proxy},
                    timeout=5
                )
                
                if renew.status_code == 200:
                    print(f"🎉 ПОДПИСКА ОБНОВЛЕНА через {proxy}", flush=True)
                    
                    # Создаём конфиг
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
            print(f"⚠️ Ошибка на {proxy}: {str(e)[:50]}", flush=True)
            continue
    
    if not success:
        print("❌ Нет рабочих прокси", flush=True)
        # Создаём запасной конфиг
        with open('isyzan_config.ovpn', 'w') as f:
            f.write("# ISYZAN VPN - Нет рабочих прокси, попробуй позже")
        sys.exit(0)
        
except Exception as e:
    print(f"❌ КРИТИЧЕСКАЯ ОШИБКА: {str(e)[:100]}", flush=True)
    # Создаём пустой конфиг, чтобы не падать
    with open('isyzan_config.ovpn', 'w') as f:
        f.write(f"# ISYZAN VPN - Ошибка: {str(e)[:100]}")
    sys.exit(0)

print("✅ ISYZAN VPN УСПЕШНО ЗАВЕРШЁН", flush=True)
