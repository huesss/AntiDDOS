import random
import time
from datetime import datetime, timedelta
from colorama import Fore, Style

class FirewallMonitor:
    def __init__(self):
        self.blocked_ips = set()
        self.suspicious_ips = {}  # IP: {count: int, first_seen: datetime}
        self.ip_packet_history = {}  # IP: [список последних пакетов]
        self.threshold = 50  # количество подозрительных пакетов до блокировки
        self.history_size = 100  # размер истории пакетов для анализа
        self.blocked_count = 0
        self.detection_patterns = self._load_detection_patterns()
        
    def _load_detection_patterns(self):
        """Загрузка шаблонов обнаружения DDoS атак"""
        return {
            "SYN_FLOOD": {"ports": [80, 443, 8080], "min_size": 40, "max_size": 60},
            "UDP_FLOOD": {"min_size": 500, "protocol": "UDP"},
            "HTTP_FLOOD": {"ports": [80, 443], "protocol": "TCP"},
            "ICMP_FLOOD": {"protocol": "ICMP", "rate": 50},
            "TCP_AMP": {"protocol": "TCP", "size_multiplier": 3.0},
        }
    
    def analyze_packet(self, ip, protocol, port, size):
        """Анализирует пакет и определяет, является ли он частью DDoS-атаки"""
        # Добавляем в историю
        if ip not in self.ip_packet_history:
            self.ip_packet_history[ip] = []
        
        # Запись информации о пакете
        packet_info = {
            "protocol": protocol,
            "port": port,
            "size": size,
            "timestamp": datetime.now()
        }
        
        self.ip_packet_history[ip].append(packet_info)
        
        # Ограничение размера истории
        if len(self.ip_packet_history[ip]) > self.history_size:
            self.ip_packet_history[ip].pop(0)
        
        # Анализ шаблонов атак
        attack_score = 0
        detected_attacks = []
        
        # Проверка частоты пакетов
        recent_packets = [p for p in self.ip_packet_history[ip] 
                         if p["timestamp"] > datetime.now() - timedelta(seconds=5)]
        
        # Проверка на SYN-флуд
        if (protocol == "TCP" and 
            port in self.detection_patterns["SYN_FLOOD"]["ports"] and
            self.detection_patterns["SYN_FLOOD"]["min_size"] <= size <= self.detection_patterns["SYN_FLOOD"]["max_size"] and
            len(recent_packets) > 30):
            attack_score += 30
            detected_attacks.append("SYN_FLOOD")
        
        # Проверка на UDP-флуд
        if protocol == "UDP" and len(recent_packets) > 40:
            attack_score += 25
            detected_attacks.append("UDP_FLOOD")
        
        # Проверка на HTTP-флуд
        if (protocol == "TCP" and 
            port in self.detection_patterns["HTTP_FLOOD"]["ports"] and
            len(recent_packets) > 35):
            attack_score += 20
            detected_attacks.append("HTTP_FLOOD")
        
        # Проверка на ICMP-флуд
        if protocol == "ICMP" and len(recent_packets) > 20:
            attack_score += 15
            detected_attacks.append("ICMP_FLOOD")
        
        # Считаем подозрительным, если attack_score больше порогового значения
        is_suspicious = attack_score >= 20
        
        # Обработка подозрительного IP
        if is_suspicious:
            if ip not in self.suspicious_ips:
                self.suspicious_ips[ip] = {
                    "count": 1,
                    "first_seen": datetime.now(),
                    "last_seen": datetime.now(),
                    "attack_types": detected_attacks
                }
            else:
                self.suspicious_ips[ip]["count"] += 1
                self.suspicious_ips[ip]["last_seen"] = datetime.now()
                self.suspicious_ips[ip]["attack_types"] = list(set(self.suspicious_ips[ip].get("attack_types", []) + detected_attacks))
            
            # Если превышен порог - блокируем IP
            if self.suspicious_ips[ip]["count"] >= self.threshold and ip not in self.blocked_ips:
                self.block_ip(ip)
                return True, self.suspicious_ips[ip]["attack_types"]
        
        return False, []
    
    def block_ip(self, ip):
        """Блокирует указанный IP-адрес"""
        if ip not in self.blocked_ips:
            self.blocked_ips.add(ip)
            self.blocked_count += 1
            print(f"{Fore.RED}{Style.BRIGHT}[БЛОКИРОВКА] {Fore.YELLOW}IP {Fore.WHITE}{ip} {Fore.YELLOW}добавлен в черный список!")
            
            # Здесь может быть реальная блокировка на уровне системы
            # Например, добавление правила в iptables/Windows Firewall
            
            # Для наглядности просто показываем информацию
            if ip in self.suspicious_ips:
                attack_types = ", ".join(self.suspicious_ips[ip].get("attack_types", ["Неизвестно"]))
                count = self.suspicious_ips[ip]["count"]
                first_seen = self.suspicious_ips[ip]["first_seen"].strftime("%H:%M:%S")
                print(f"{Fore.YELLOW}  └─ Тип атаки: {Fore.WHITE}{attack_types}")
                print(f"{Fore.YELLOW}  └─ Подозрительных пакетов: {Fore.WHITE}{count}")
                print(f"{Fore.YELLOW}  └─ Первое обнаружение: {Fore.WHITE}{first_seen}")
            
            return True
        return False
    
    def unblock_ip(self, ip):
        """Разблокирует указанный IP-адрес"""
        if ip in self.blocked_ips:
            self.blocked_ips.remove(ip)
            if ip in self.suspicious_ips:
                del self.suspicious_ips[ip]
            if ip in self.ip_packet_history:
                del self.ip_packet_history[ip]
            return True
        return False
    
    def get_stats(self):
        """Возвращает статистику блокировок"""
        return {
            "blocked_count": self.blocked_count,
            "active_blocks": len(self.blocked_ips),
            "suspicious_count": len(self.suspicious_ips),
            "blocked_ips": list(self.blocked_ips)[-10:],  # Последние 10 заблокированных IP
        }
    
    def simulate_attack_detection(self):
        """Симуляция обнаружения атаки для демонстрации"""
        ip_parts = [str(random.randint(1, 255)) for _ in range(4)]
        ip = ".".join(ip_parts)
        protocol = random.choice(["TCP", "UDP", "ICMP", "OTHER"])
        port = random.randint(1, 65535)
        size = random.randint(64, 8192)
        
        is_blocked, attack_types = self.analyze_packet(ip, protocol, port, size)
        
        return is_blocked, ip, protocol, port, size, attack_types 