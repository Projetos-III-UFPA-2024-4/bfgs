import traci  # Importa a biblioteca TraCI para interagir com o SUMO
import traffic_utils
import Controller
import requests

class TrafficCollector:
    def __init__(self, myTl):
        self.myTl = myTl
        self.last_phase = 0
        self.cycle_number = 0
        self.current_phase_index = 0
        self.phase_start_time = traci.simulation.getTime()
        self.detectors = traci.inductionloop.getIDList()
        self.phases = traci.trafficlight.getAllProgramLogics(myTl)[0].phases
        self.green_phases = [i for i, phase in enumerate(self.phases) if "G" in phase.state]
        self.numPhases = traffic_utils.get_green_phases(myTl)
        self.observed_flow = 0
        self.phase_data = []

    def collect(self, cur, cnx, db_config, step):

        database = db_config["database"]
        table_congestion_data = db_config["table_congestion_data"]
        table_notifications = db_config["table_notification"]
        table_states = db_config["table_states"]

        query_congestionData_replace = f"""
            REPLACE INTO {database}.{table_congestion_data}
            (ID, Cycle_Number, Num_Phases, Phase_Index, Observed_Flow, Critical_Flow, Critical_Flow_TOTAL)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """

        query_notification_replace = f"""
            REPLACE INTO {database}.{table_notifications}
            (ID, Message)
            VALUES (%s, %s)
        """

        query_states_replace = f"""
            REPLACE INTO {database}.{table_states}
            (ID, States)
            VALUES (%s, %s)
        """

        current_phase = traci.trafficlight.getPhase(self.myTl)
        '''
        if current_phase != self.last_phase:
                    
            previous_state = traffic_utils.get_tls_states(self.myTl)
            cur.execute(query_states_replace, (1, previous_state))
            cnx.commit()              

            self.last_phase = current_phase
            print("[Collector] Estados inseridos")
        '''
        # Se a fase atual for uma fase verde
        if current_phase in self.green_phases:
            phase_duration = self.phases[current_phase].duration  # Obtém a duração da fase atual

            # Atualiza os detectores com base na fase atual
            self.observed_flow = traffic_utils.update_detector_counts(self.detectors, self.observed_flow)

            # Se a duração da fase verde terminou
            if step >= self.phase_start_time + phase_duration:                 

                # Calcula os fluxos críticos baseados na contagem de veículos
                flow = traffic_utils.calculate_critical_flow(self.observed_flow)
                print(f"[Collector] Fim da fase {current_phase}, fluxo = {flow:.4f}")

                self.phase_data.append({
                    "cycle": self.cycle_number,
                    "phase": current_phase,
                    "observed_flow": self.observed_flow,
                    "critical_flow": flow
                })

                # Avançar para a próxima fase de verde
                self.current_phase_index = (self.current_phase_index + 1) % self.numPhases
                self.phase_start_time = step  # Atualiza o tempo de início da nova fase verde
                self.observed_flow = 0

                if self.current_phase_index == 0:
                    critical_flow_total = sum(p["critical_flow"] for p in self.phase_data)
                    print(f"Fluxo crítico total = {critical_flow_total:.4f} \nFim do Ciclo {self.cycle_number}\n")
                    massage = (traffic_utils.notification_agent(critical_flow_total),)
                        

                    # Substitui os dados no banco de dados
                    i = 0
                    for i, data in enumerate(self.phase_data):
                        cur.execute(query_congestionData_replace, (
                            i + 1,
                            data["cycle"],
                            self.numPhases,
                            data["phase"],
                            data["observed_flow"],
                            data["critical_flow"],
                            critical_flow_total
                        ))

                    cur.execute(query_notification_replace, (1, massage[0]))                           
                    cnx.commit()  # Confirma a transação no banco de dados
                    try:
                        requests.post("http://ec2-54-162-236-6.compute-1.amazonaws.com/optimize")
                        print("[Collector] Otimização acionada na nuvem.")
                    except Exception as e:
                        print("[Collector] Erro ao acionar otimização:", e)
                    print("[Collector] DADOS INSERIDOS")
                    self.phase_data = []
                    self.cycle_number += 1
                    Controller.controller_flow(cur, db_config)