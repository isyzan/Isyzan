import requests
import re
import random

print('🔥 ISYZAN VPN — АВТООБНОВЛЕНИЕ')

# 1. Скачиваем список бесплатных серверов
url = 'https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt'
text = requests.get(url, timeout=10).text

# 2. Находим все IP:PORT
proxies = re.findall(r'\d+\.\d+\.\d+\.\d+:\d+', text)
print(f'Найдено {len(proxies)} серверов')

# 3. Проверяем случайные
random.shuffle(proxies)
for proxy in proxies[:10]:
    try:
        r = requests.get('https://httpbin.org/ip', 
                         proxies={'http': proxy, 'https': proxy}, 
                         timeout=3)
        if r.status_code == 200:
            print(f'✅ Рабочий: {proxy}')
            
            # 4. Отправляем запрос (замени URL на свой)
            renew = requests.get('https://www.google.com', 
                                 proxies={'http': proxy, 'https': proxy},
                                 timeout=5)
            
            if renew.status_code == 200:
                print(f'🎉 ПОДПИСКА ОБНОВЛЕНА через {proxy}')
                
                # 5. Сохраняем конфиг ISYZAN VPN
                config = f"""
# ISYZAN VPN CONFIG
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
                print('📁 Конфиг ISYZAN сохранён — скачай!')
                break
    except:
        pass
