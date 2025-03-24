import os
import time
import random
import socket
import platform
import threading
import ipaddress
from datetime import datetime
from colorama import Fore, Back, Style, init

# Инициализация colorama для поддержки цветного текста в консоли Windows
init(autoreset=True)

# Глобальные переменные
running = True
blocked_ips = set()
suspicious_ips = {}
packet_stats = {"TCP": 0, "UDP": 0, "ICMP": 0, "OTHER": 0}
total_blocked = 0
attack_level = 0

# Симуляция выявления вредоносных пакетов
def simulate_packet_detection():
    global attack_level, total_blocked
    
    while running:
        # Генерация случайного IP-адреса для демонстрации
        ip_parts = [str(random.randint(1, 255)) for _ in range(4)]
        ip = ".".join(ip_parts)
        
        # Выбор случайного протокола
        protocol = random.choice(["TCP", "UDP", "ICMP", "OTHER"])
        packet_stats[protocol] += 1
        
        # Симуляция размера пакета
        packet_size = random.randint(100, 9000)
        
        # Симуляция порта
        port = random.randint(1, 65535)
        
        # Вероятность обнаружения вредоносного пакета
        is_malicious = random.random() < 0.3
        
        if is_malicious:
            if ip not in blocked_ips:
                blocked_ips.add(ip)
                total_blocked += 1
                # Симуляция уровня угрозы
                attack_level = min(100, attack_level + random.randint(1, 5))
                log_attack(ip, protocol, port, packet_size)
            
        time.sleep(0.5)  # Частота симуляции пакетов

# Функция логирования атаки с цветовым выделением
def log_attack(ip, protocol, port, size):
    timestamp = datetime.now().strftime("%H:%M:%S")
    
    threat_level = random.randint(1, 10)
    threat_color = Fore.GREEN
    if threat_level > 3:
        threat_color = Fore.YELLOW
    if threat_level > 6:
        threat_color = Fore.RED
    if threat_level > 8:
        threat_color = Fore.RED + Style.BRIGHT
        
    print(f"{Fore.CYAN}[{timestamp}] {Fore.RED}ЗАБЛОКИРОВАНА АТАКА! {threat_color}[Уровень угрозы: {threat_level}/10]")
    print(f"{Fore.YELLOW}  └─ IP: {Fore.WHITE}{ip} {Fore.YELLOW}Протокол: {Fore.WHITE}{protocol} {Fore.YELLOW}Порт: {Fore.WHITE}{port} {Fore.YELLOW}Размер: {Fore.WHITE}{size} байт")
    print(f"{Fore.CYAN}  └─ Действие: {Fore.GREEN}IP адрес добавлен в черный список и пакеты отклонены")

# Отображение статистики и интерфейса
def display_interface():
    global attack_level
    
    while running:
        os.system('cls' if os.name == 'nt' else 'clear')
        
        # Текущее время
        current_time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        
        # Шапка программы
        print(f"{Fore.CYAN}{Style.BRIGHT}{'=' * 80}")
        print(f"{Fore.RED}{Style.BRIGHT}{'АНТИ-DDOS ЗАЩИТА'.center(80)}")
        print(f"{Fore.YELLOW}{Style.BRIGHT}{'SCP:SL И UNITY СЕРВЕР'.center(80)}")
        print(f"{Fore.CYAN}{Style.BRIGHT}{'=' * 80}")
        
        # Системная информация
        print(f"{Fore.GREEN}Время: {Fore.WHITE}{current_time}")
        print(f"{Fore.GREEN}Система: {Fore.WHITE}{platform.system()} {platform.release()}")
        try:
            hostname = socket.gethostname()
            host_ip = socket.gethostbyname(hostname)
            print(f"{Fore.GREEN}Хост: {Fore.WHITE}{hostname} ({host_ip})")
        except:
            print(f"{Fore.GREEN}Хост: {Fore.WHITE}Не удалось определить")
        
        # Статистика пакетов
        print(f"\n{Fore.CYAN}{Style.BRIGHT}СТАТИСТИКА ПАКЕТОВ:")
        print(f"{Fore.GREEN}TCP: {Fore.WHITE}{packet_stats['TCP']} {Fore.GREEN}UDP: {Fore.WHITE}{packet_stats['UDP']} {Fore.GREEN}ICMP: {Fore.WHITE}{packet_stats['ICMP']} {Fore.GREEN}ДРУГИЕ: {Fore.WHITE}{packet_stats['OTHER']}")
        
        # Уровень атаки
        print(f"\n{Fore.CYAN}{Style.BRIGHT}ТЕКУЩИЙ УРОВЕНЬ УГРОЗЫ:")
        attack_bar = draw_progress_bar(attack_level, 100, 50)
        attack_color = Fore.GREEN
        if attack_level > 30:
            attack_color = Fore.YELLOW
        if attack_level > 60:
            attack_color = Fore.RED
        print(f"{attack_color}{attack_bar} {attack_level}%")
        
        # Постепенное снижение уровня атаки, если он ненулевой
        if attack_level > 0:
            attack_level = max(0, attack_level - 1)
        
        # Статистика блокировок
        print(f"\n{Fore.CYAN}{Style.BRIGHT}БЛОКИРОВКИ:")
        print(f"{Fore.GREEN}Всего заблокировано IP: {Fore.WHITE}{total_blocked}")
        print(f"{Fore.GREEN}Активные блокировки: {Fore.WHITE}{len(blocked_ips)}")
        
        # Список последних заблокированных IP
        if blocked_ips:
            print(f"\n{Fore.CYAN}{Style.BRIGHT}ПОСЛЕДНИЕ ЗАБЛОКИРОВАННЫЕ IP (максимум 10):")
            for i, ip in enumerate(list(blocked_ips)[-10:]):
                print(f"{Fore.YELLOW}{i+1}. {Fore.WHITE}{ip}")
        
        # Инструкции
        print(f"\n{Fore.CYAN}{Style.BRIGHT}{'=' * 80}")
        print(f"{Fore.GREEN}Нажмите {Fore.WHITE}Ctrl+C {Fore.GREEN}для выхода")
        
        time.sleep(1)  # Обновление интерфейса каждую секунду

# Функция для отрисовки прогресс-бара
def draw_progress_bar(current, total, bar_length=50):
    percent = current / total
    arrow = '█' * int(round(percent * bar_length))
    spaces = ' ' * (bar_length - len(arrow))
    return f"[{arrow}{spaces}]"

# Основная функция
def main():
    global running
    
    try:
        # Приветственное сообщение
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"{Fore.CYAN}{Style.BRIGHT}{'=' * 80}")
        print(f"{Fore.RED}{Style.BRIGHT}{'АНТИ-DDOS ЗАЩИТА'.center(80)}")
        print(f"{Fore.YELLOW}{Style.BRIGHT}{'ЗАПУСК СИСТЕМЫ...'.center(80)}")
        print(f"{Fore.CYAN}{Style.BRIGHT}{'=' * 80}")
        
        # Симуляция инициализации
        for i in range(101):
            progress_bar = draw_progress_bar(i, 100, 50)
            print(f"\r{Fore.GREEN}Инициализация... {Fore.WHITE}{progress_bar} {i}%", end='')
            time.sleep(0.02)
        
        print(f"\n\n{Fore.GREEN}Система защиты активирована!")
        time.sleep(1)
        
        # Запуск потоков для симуляции и отображения
        detector_thread = threading.Thread(target=simulate_packet_detection)
        interface_thread = threading.Thread(target=display_interface)
        
        detector_thread.daemon = True
        interface_thread.daemon = True
        
        detector_thread.start()
        interface_thread.start()
        
        # Ожидание сигнала выхода
        while True:
            time.sleep(0.1)
            
    except KeyboardInterrupt:
        running = False
        print(f"\n{Fore.YELLOW}Выключение системы защиты...")
        time.sleep(1)
        print(f"{Fore.GREEN}Система защиты выключена. До свидания!")

if __name__ == "__main__":
    main() 