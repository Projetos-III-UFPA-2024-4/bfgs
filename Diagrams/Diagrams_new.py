from diagrams import Cluster, Diagram
from diagrams.custom import Custom
from diagrams.aws.database import Dynamodb
from diagrams.aws.general import Client, User
from diagrams.aws.compute import EC2

with Diagram("Sistema Dinâmico de Semáforos (Fluxograma)", show=False, node_attr={"fontsize": "16", "fontname": "Arial"}):
    sumo = Custom("",r"./resources/SUMO.png")

    db_cong = Dynamodb("Congestion DB")
    db_semaf = Dynamodb("Traffic Light DB")

    congestion_detec = EC2("Congestion Detection")

    inteligent_optimization = EC2("Intelligent Optimization")

    traffic_light_control = EC2("Traffic Light Control")
    monitor = Client("Monitor")
    user = User("User")

    sumo >> db_cong
    db_cong >> congestion_detec
    congestion_detec >> inteligent_optimization
    db_cong >> inteligent_optimization

    inteligent_optimization >> db_semaf
    inteligent_optimization >> traffic_light_control
    db_semaf >> monitor >> user
    user >> monitor >> traffic_light_control >> sumo