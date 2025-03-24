import os
import time
import socket
import platform
import threading
import ipaddress
from datetime import datetime
from colorama import Fore, Back, Style, init
from firewall import FirewallMonitor

# Инициализация colorama для поддержки цветного текста в консоли Windows
init(autoreset=True)

# Глобальные переменные
running = True
packet_stats = {"TCP": 0, "UDP": 0, "ICMP": 0, "OTHER": 0}
attack_level = 0
firewall = FirewallMonitor()

# Функция для отрисовки прогресс-бара
def draw_progress_bar(current, total, bar_length=50):
    percent = current / total
    arrow = '█' * int(round(percent * bar_length))
    spaces = ' ' * (bar_length - len(arrow))
    return f"[{arrow}{spaces}]"

# Симуляция выявления вредоносных пакетов с использованием FirewallMonitor
def simulate_packet_detection():
    global attack_level
    
    while running:
        # Используем FirewallMonitor для симуляции обнаружения атаки
        is_blocked, ip, protocol, port, size, attack_types = firewall.simulate_attack_detection()
        
        # Обновляем статистику пакетов
        packet_stats[protocol] += 1
        
        # Если был заблокирован IP, увеличиваем уровень атаки
        if is_blocked:
            attack_level = min(100, attack_level + random.randint(5, 15))
            
            # Получаем строковое представление типов атак
            attack_types_str = ", ".join(attack_types) if attack_types else "Неизвестный тип атаки"
            
            # Выводим информацию о заблокированной атаке
            timestamp = datetime.now().strftime("%H:%M:%S")
            threat_level = random.randint(5, 10)  # Для заблокированных IP уровень угрозы всегда высокий
            
            threat_color = Fore.YELLOW
            if threat_level > 7:
                threat_color = Fore.RED
            if threat_level > 9:
                threat_color = Fore.RED + Style.BRIGHT
                
            print(f"{Fore.CYAN}[{timestamp}] {Fore.RED}ЗАБЛОКИРОВАНА АТАКА! {threat_color}[Уровень угрозы: {threat_level}/10]")
            print(f"{Fore.YELLOW}  └─ IP: {Fore.WHITE}{ip} {Fore.YELLOW}Протокол: {Fore.WHITE}{protocol} {Fore.YELLOW}Порт: {Fore.WHITE}{port} {Fore.YELLOW}Размер: {Fore.WHITE}{size} байт")
            print(f"{Fore.YELLOW}  └─ Тип атаки: {Fore.WHITE}{attack_types_str}")
            print(f"{Fore.CYAN}  └─ Действие: {Fore.GREEN}IP адрес добавлен в черный список и пакеты отклонены")
        
        time.sleep(0.5)  # Частота симуляции пакетов

# Функция для отображения статистики топ-атак
def display_attack_types():
    attack_types = {
        "SYN_FLOOD": {"description": "Атака с помощью TCP SYN пакетов, приводящая к перегрузке сервера", "count": 0},
        "UDP_FLOOD": {"description": "Массовая отправка UDP пакетов на случайные порты", "count": 0},
        "HTTP_FLOOD": {"description": "Множество HTTP-запросов для перегрузки веб-сервера", "count": 0},
        "ICMP_FLOOD": {"description": "Перегрузка системы ICMP-пакетами (ping)", "count": 0},
        "TCP_AMP": {"description": "Атака с использованием TCP-усиления", "count": 0},
    }
    
    # Заполнение случайными значениями для демонстрации
    for attack in attack_types:
        attack_types[attack]["count"] = random.randint(10, 1000)
    
    # Сортировка по количеству атак
    sorted_attacks = sorted(attack_types.items(), key=lambda x: x[1]["count"], reverse=True)
    
    print(f"\n{Fore.CYAN}{Style.BRIGHT}ТОП ТИПОВ АТАК:")
    for i, (attack_name, attack_info) in enumerate(sorted_attacks[:3]):
        print(f"{Fore.YELLOW}{i+1}. {Fore.WHITE}{attack_name}: {attack_info['description']}")
        attack_bar = draw_progress_bar(attack_info["count"], 1000, 30)
        print(f"   {Fore.GREEN}{attack_bar} {Fore.WHITE}{attack_info['count']} блокировок")

# Отображение статистики и интерфейса
def display_interface():
    global attack_level
    
    while running:
        os.system('cls' if os.name == 'nt' else 'clear')
        
        # Текущее время
        current_time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        
        # Шапка программы
        print(f"{Fore.CYAN}{Style.BRIGHT}{'=' * 80}")
        print(f"{Fore.RED}{Style.BRIGHT}{'РАСШИРЕННАЯ АНТИ-DDOS ЗАЩИТА'.center(80)}")
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
        
        # Статус системы
        status_color = Fore.GREEN
        status_text = "НОРМАЛЬНЫЙ"
        if attack_level > 30:
            status_color = Fore.YELLOW
            status_text = "ПОВЫШЕННАЯ ГОТОВНОСТЬ"
        if attack_level > 60:
            status_color = Fore.RED
            status_text = "ПОД АТАКОЙ"
        if attack_level > 90:
            status_color = Fore.RED + Style.BRIGHT
            status_text = "КРИТИЧЕСКАЯ УГРОЗА"
            
        print(f"{Fore.CYAN}Статус системы: {status_color}{status_text}")
        
        # Постепенное снижение уровня атаки, если он ненулевой
        if attack_level > 0:
            attack_level = max(0, attack_level - 1)
        
        # Статистика блокировок
        stats = firewall.get_stats()
        print(f"\n{Fore.CYAN}{Style.BRIGHT}БЛОКИРОВКИ:")
        print(f"{Fore.GREEN}Всего заблокировано IP: {Fore.WHITE}{stats['blocked_count']}")
        print(f"{Fore.GREEN}Активные блокировки: {Fore.WHITE}{stats['active_blocks']}")
        print(f"{Fore.GREEN}Подозрительные IP: {Fore.WHITE}{stats['suspicious_count']}")
        
        # Вывод типов атак
        display_attack_types()
        
        # Список последних заблокированных IP
        if stats['blocked_ips']:
            print(f"\n{Fore.CYAN}{Style.BRIGHT}ПОСЛЕДНИЕ ЗАБЛОКИРОВАННЫЕ IP (максимум 5):")
            for i, ip in enumerate(stats['blocked_ips'][-5:]):
                print(f"{Fore.YELLOW}{i+1}. {Fore.WHITE}{ip}")
        
        # Инструкции
        print(f"\n{Fore.CYAN}{Style.BRIGHT}{'=' * 80}")
        print(f"{Fore.GREEN}Нажмите {Fore.WHITE}Ctrl+C {Fore.GREEN}для выхода")
        
        time.sleep(1)  # Обновление интерфейса каждую секунду

# Основная функция
def main():
    global running
    
    try:
        # Приветственное сообщение
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"{Fore.CYAN}{Style.BRIGHT}{'=' * 80}")
        print(f"{Fore.RED}{Style.BRIGHT}{'РАСШИРЕННАЯ АНТИ-DDOS ЗАЩИТА'.center(80)}")
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
    # Импортируем random здесь, чтобы избежать проблем с циклическими импортами
    import random
    main() 