import requests
import re
import random
import sys
import time

print("🚀 ISYZAN VPN START", flush=True)

# МНОГО источников для надёжности
SOURCES = [
    'https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000',
    'https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt',
    'https://raw.githubusercontent.com/roosterkid/openproxylist/main/HTTPS_RAW.txt',
    'https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt'
]

all_proxies = []

print("📡 Загружаю списки прокси...", flush=True)

for url in SOURCES:
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            found = re.findall(r'\d+\.\d+\.\d+\.\d+:\d+', response.text)
            all_proxies.extend(found)
            print(f"✅ {url.split('/')[-1][:20]}... -> {len(found)} прокси", flush=True)
    except Exception as e:
        print(f"⚠️ Ошибка загрузки: {str(e)[:30]}", flush=True)

# Удаляем дубликаты
all_proxies = list(set(all_proxies))
print(f"✅ ВСЕГО НАЙДЕНО: {len(all_proxies)} прокси", flush=True)

if not all_proxies:
    print("❌ Нет прокси, выход", flush=True)
    with open('isyzan_config.ovpn', 'w') as f:
        f.write("# ISYZAN VPN - Нет прокси, попробуй позже")
    sys.exit(0)

# Проверяем прокси
random.shuffle(all_proxies)
success = False

print("🔍 Проверяю прокси (это может занять 10-20 секунд)...", flush=True)

for i, proxy in enumerate(all_proxies[:30]):
    try:
        print(f"   {i+1}/30: {proxy}...", flush=True, end='')
        test = requests.get(
            'https://httpbin.org/ip',
            proxies={'http': proxy, 'https': proxy},
            timeout=3
        )
        if test.status_code == 200:
            print(" ✅ РАБОТАЕТ!", flush=True)
            
            # Создаём конфиг
            config = f"""# ISYZAN VPN CONFIG
# Активный сервер: {proxy}
# Обновлено: {time.strftime('%Y-%m-%d %H:%M:%S')}

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
            
            print("🎉 КОНФИГ СОЗДАН!", flush=True)
            success = True
            break
        else:
            print(" ❌ не ответил", flush=True)
    except Exception as e:
        print(f" ⚠️ ошибка", flush=True)
        continue

if not success:
    print("❌ НЕ НАЙДЕНО РАБОЧИХ ПРОКСИ", flush=True)
    with open('isyzan_config.ovpn', 'w') as f:
        f.write("""# ISYZAN VPN - ВРЕМЕННО НЕТ РАБОЧИХ ПРОКСИ
# Попробуй запустить Actions снова через 5-10 минут
# Или скачай конфиг с другого источника""")

print("✅ ISYZAN VPN ЗАВЕРШЁН", flush=True)
