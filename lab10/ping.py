import time
from scapy.all import *
import ipaddress
import argparse

class Response:
    def __init__(self, ip : str, bytes_count : int, ttl : int, rtt_ms : int):
        self.ip = ip
        self.bytes_count = bytes_count
        self.ttl = ttl
        self.rtt_ms = rtt_ms

    def __str__(self):
        if self.rtt_ms:
            return f"Ответ от {self.ip}: число байт={self.bytes_count} время={self.rtt_ms}мс TTL={self.ttl}"
        else:
            return "Превышен интервал ожидания для запроса."

class ResponseStatistics:
    def __init__(self, ip):
        self.ip = ip
        self.send = 0
        self.got = 0
        self.min_rtt = None
        self.max_rtt = None
        self.sum_rtt = 0

    def add_responce(self, response : Response):
        if response.ip != self.ip:
            raise ValueError(f"Responce ip ({response.ip}) is not equal to statistics ip ({self.ip})!")
        self.send += 1
        if response.rtt_ms is None:
            return

        self.got += 1

        self.sum_rtt += response.rtt_ms
        if self.min_rtt is None or self.min_rtt > response.rtt_ms:
            self.min_rtt = response.rtt_ms

        if self.max_rtt is None or self.max_rtt < response.rtt_ms:
            self.max_rtt = response.rtt_ms

    def __str__(self):
        lost = self.send - self.got
        lost_percent = round(lost / self.got * 100, 1) if self.got != 0 else 0.0
        avg_rtt = round(self.sum_rtt / self.got) if self.got != 0 else 0.0
        result = [
            f"Статистика Ping для {self.ip}:",
            f"    Пакетов: отправлено = {self.send}, получено = {self.got}, потеряно = {lost}",
            f"    ({lost_percent}% потерь)",
            f"Приблизительное время приема-передачи в мс:",
            f"    Минимальное = {self.min_rtt}мсек, Максимальное = {self.max_rtt} мсек, Среднее = {avg_rtt} мсек"
        ]
        return "\n".join(result)

def send_icmp_request(ip, timeout_ms):
    icmp_request = IP(dst=ip)/ICMP()

    response = sr1(icmp_request, timeout=timeout_ms / 1000, verbose=0)
    if response:
        if response.haslayer(ICMP):
            icmp_layer = response.getlayer(ICMP)
            icmp_type = icmp_layer.type
            icmp_code = icmp_layer.code
        rtt_s = response.time - icmp_request.sent_time
        rtt_ms = round(rtt_s * 1000)
        return Response(ip, len(response), response.ttl, rtt_ms)
    else:
        return Response(ip, None, None, None)

def check_ip(ip : str):
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Ping a specified IP address with an optional timeout.")

    default_timeout = 1000
    default_requests_count = 5

    parser.add_argument('ip', type=str, help='The IP address to ping.')
    parser.add_argument('--timeout', type=int, default=default_timeout, help=f'Timeout in miliseconds (default: {default_timeout}).')
    parser.add_argument('--requests_count', type=int, default=default_requests_count, help=f'Requests count (defalt : {default_requests_count}).')

    args = parser.parse_args()

    ip = args.ip
    timeout = args.timeout
    request_count = args.requests_count

    statistics = ResponseStatistics(ip)
    for i in range(request_count):
        response = send_icmp_request(ip, timeout)
        print(response)
        statistics.add_responce(response)
        time.sleep(1)
    print()

    print(statistics)
