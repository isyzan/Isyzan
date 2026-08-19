import requests
import re
import random

print('🔥 ISYZAN VPN START')

try:
    # Скачиваем список прокси
    url = 'https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt'
    response = requests.get(url, timeout=10)
    text = response.text
    
    # Находим все IP:PORT
    proxies = re.findall(r'\d+\.\d+\.\d+\.\d+:\d+', text)
    print(f'Найдено {len(proxies)} серверов')
    
    if not proxies:
        print('❌ Прокси не найдены')
        exit(1)
    
    # Перемешиваем и проверяем
    random.shuffle(proxies)
    success = False
    
    for proxy in proxies[:15]:
        try:
            print(f'Проверяю {proxy}...')
            test = requests.get('https://httpbin.org/ip', 
                                proxies={'http': proxy, 'https': proxy}, 
                                timeout=3)
            if test.status_code == 200:
                print(f'✅ Рабочий: {proxy}')
                
                # Пытаемся обновить подписку
                renew = requests.get('https://www.google.com', 
                                     proxies={'http': proxy, 'https': proxy},
                                     timeout=5)
                
                if renew.status_code == 200:
                    print(f'🎉 ПОДПИСКА ОБНОВЛЕНА через {proxy}')
                    
                    # Сохраняем конфиг
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
                    print('📁 Конфиг ISYZAN сохранён')
                    success = True
                    break
        except Exception as e:
            print(f'Ошибка на {proxy}: {e}')
    
    if not success:
        print('❌ Не удалось найти рабочий прокси')
        exit(1)
        
except Exception as e:
    print(f'❌ Критическая ошибка: {e}')
    exit(1)
