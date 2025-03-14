import traci

# Dicionários para armazenar estatísticas
vehicle_wait_times = {}  # Tempo total de espera por veículo
vehicle_travel_times = {}  # Tempo total de viagem por veículo

while traci.simulation.getMinExpectedNumber() > 0:
    traci.simulationStep()
    step = traci.simulation.getTime()

    for veh_id in traci.vehicle.getIDList():
        # 📊 Coletar tempo de espera (parado no semáforo)
        wait_time = traci.vehicle.getWaitingTime(veh_id)
        vehicle_wait_times[veh_id] = vehicle_wait_times.get(veh_id, 0) + wait_time

        # 📊 Coletar tempo total de viagem
        if veh_id not in vehicle_travel_times:
            vehicle_travel_times[veh_id] = step  # Marca o tempo de entrada do veículo

    # Ao final, calcular tempo total de viagem dos veículos que saíram do sistema
    for veh_id in list(vehicle_travel_times.keys()):
        if veh_id not in traci.vehicle.getIDList():
            vehicle_travel_times[veh_id] = step - vehicle_travel_times[veh_id]

# Fechar conexão com SUMO
traci.close()

# 📈 Análise dos dados coletados
avg_wait_time = sum(vehicle_wait_times.values()) / len(vehicle_wait_times) if vehicle_wait_times else 0
avg_travel_time = sum(vehicle_travel_times.values()) / len(vehicle_travel_times) if vehicle_travel_times else 0

print(f"\n📊 RESULTADOS DA SIMULAÇÃO:")
print(f"⏳ Tempo médio de espera nos semáforos: {avg_wait_time:.2f} segundos")
print(f"🚗 Tempo médio de viagem dos veículos: {avg_travel_time:.2f} segundos")
