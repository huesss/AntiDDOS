# 🛡️ Анти-DDoS Защита для SCP:SL Серверов.

Мощная программа для защиты от DDoS-атак с красивым консольным интерфейсом. Отслеживает и блокирует подозрительные UDP и TCP пакеты, защищая ваш сервер от различных типов DDoS-атак.


## ✨ Возможности

- 🔍 Обнаружение и блокировка различных типов DDoS-атак (SYN-флуд, UDP-флуд, HTTP-флуд и др.)
- 📊 Красивый консольный интерфейс с цветовым оформлением
- 🚫 Автоматическая блокировка подозрительных IP-адресов
- 📈 Статистика пакетов и атак в реальном времени
- 🔔 Уведомления о блокировках и атаках
- 💻 Оптимизировано для использования с SCP:SL и Unity серверами

## 📋 Требования

- Python 3.6 или выше
- Windows, Linux или macOS
- Доступ к администраторским привилегиям (для блокировки IP-адресов)

## 🚀 Установка

### 1. Установите Python

#### Для Windows:

1. Скачайте установщик Python с [официального сайта](https://www.python.org/downloads/)
2. Запустите установщик
3. Убедитесь, что галочка "Add Python to PATH" отмечена
4. Нажмите "Install Now"
5. После установки откройте командную строку или PowerShell и проверьте, что Python установлен:
   ```
   python --version
   ```

#### Для Linux:

Ubuntu/Debian:
```bash
sudo apt-get update
sudo apt-get install python3 python3-pip
```

CentOS/RHEL:
```bash
sudo yum install python3 python3-pip
```

### 2. Скачайте программу

Скачайте или клонируйте этот репозиторий на ваш компьютер:

```bash
git clone https://github.com/huesss/anti-ddos.git
cd anti-ddos
```

или просто скачайте ZIP-архив и распакуйте его.

### 3. Установите зависимости

```bash
pip install colorama
```

## 🎮 Использование

### Запуск базовой версии:

```bash
python anti_ddos.py
```

### Запуск расширенной версии (рекомендуется):

```bash
python advanced_anti_ddos.py
```

## 🔧 Настройка

Программа работает "из коробки", но вы можете настроить параметры, отредактировав соответствующие переменные в файлах `firewall.py` и `advanced_anti_ddos.py`:

- `threshold` - количество подозрительных пакетов до блокировки IP
- `history_size` - размер истории пакетов для анализа
- `detection_patterns` - шаблоны для обнаружения различных типов атак

## 📚 Как это работает?

Программа отслеживает входящий сетевой трафик и анализирует его на наличие признаков DDoS-атак:

1. Отслеживание частоты пакетов с одного IP-адреса
2. Анализ содержимого пакетов
3. Проверка на соответствие известным шаблонам атак
4. Блокировка подозрительных IP-адресов

## ⚠️ Примечание

Текущая версия программы является демонстрационной и имитирует обнаружение и блокировку атак. Для реальной защиты вашего сервера от DDoS-атак вам потребуется настроить программу для вашей конкретной конфигурации сервера и сети.

## 📜 Лицензия

MIT License

## 📞 Поддержка

При возникновении вопросов или проблем создайте Issue в этом репозитории. 
