import requests

try:
    requests.post("http://ec2-54-162-236-6.compute-1.amazonaws.com/optimize")
    print("[Collector] Otimização acionada na nuvem.")
except Exception as e:
     print("[Collector] Erro ao acionar otimização:", e)