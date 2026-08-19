import requests
import re
import random
import sys
import time

print("🚀 ISYZAN VPN V2 START", flush=True)

# Прямые ссылки на готовые OpenVPN-конфиги (бесплатные серверы)
CONFIG_SOURCES = [
    'https://www.vpngate.net/api/iphone/',
    'https://raw.githubusercontent.com/NeverWonderLand/openvpn-servers/master/servers.txt',
    'https://raw.githubusercontent.com/hwdsl2/openvpn-servers/master/servers.txt'
]

all_configs = []

print("📡 Загружаю готовые конфиги...", flush=True)

for url in CONFIG_SOURCES:
    try:
        response = requests.get(url, timeout=15)
        if response.status_code == 200:
            # Ищем блоки OpenVPN-конфигов (начинаются с "client")
            configs = re.findall(r'client.*?(?=client|$)', response.text, re.DOTALL)
            if configs:
                all_configs.extend(configs)
                print(f"✅ Найдено {len(configs)} конфигов из {url[:30]}...", flush=True)
            else:
                # Если не нашли — ищем IP:PORT для ручной сборки
                ips = re.findall(r'\d+\.\d+\.\d+\.\d+:\d+', response.text)
                if ips:
                    print(f"✅ Найдено {len(ips)} серверов из {url[:30]}...", flush=True)
                    # Собираем конфиг вручную
                    for ip in ips[:10]:
                        cfg = f"""client
dev tun
proto tcp
remote {ip}
resolv-retry infinite
nobind
persist-key
persist-tun
remote-cert-tls server
cipher AES-256-CBC
verb 3
<auth-user-pass>
vpn
vpn
</auth-user-pass>
"""
                        all_configs.append(cfg)
    except Exception as e:
        print(f"⚠️ Ошибка: {str(e)[:30]}", flush=True)

print(f"✅ ВСЕГО НАЙДЕНО: {len(all_configs)} конфигов", flush=True)

if not all_configs:
    print("❌ Нет конфигов, выход", flush=True)
    with open('isyzan_config.ovpn', 'w') as f:
        f.write("# ISYZAN VPN - Нет конфигов, попробуй позже")
    sys.exit(0)

# Берём случайный конфиг
random.shuffle(all_configs)
selected = all_configs[0]

# Добавляем метку времени
selected = f"# ISYZAN VPN CONFIG\n# Обновлено: {time.strftime('%Y-%m-%d %H:%M:%S')}\n{selected}"

# Сохраняем
with open('isyzan_config.ovpn', 'w') as f:
    f.write(selected)

print("🎉 КОНФИГ СОЗДАН!", flush=True)
print("📁 Сохранён как isyzan_config.ovpn", flush=True)

# Дополнительно сохраняем в Artifacts (для скачивания)
with open('isyzan_config_backup.ovpn', 'w') as f:
    f.write(selected)

print("✅ ISYZAN VPN V2 ЗАВЕРШЁН", flush=True)
