from diagrams import Cluster, Diagram
from diagrams.custom import Custom
from diagrams.aws.database import DatabaseMigrationService, DMS
from diagrams.aws.general import Client, User
from diagrams.aws.compute import Lambda, EC2

with Diagram("Sistema dinamico de Semaforos (Fluxograma)", show=False, node_attr={"fontsize": "16", "fontname": "Arial"}):
    sumo = Custom("",r"C:\Users\machi\bfgs\Diagrams\resources\SUMO.png")

    db_cong = DMS("Congestion DB")
    db_semaf = DMS("Traffic Light DB")

    congestion_detec = Lambda("Congestion Detection")

    inteligent_optimization = Lambda("Intelligent Optimization")

    traffic_light_control = Lambda("Traffic Light Control")
    monitor = Client("Monitor")
    user = User("User")

    sumo >> congestion_detec
    db_cong >> congestion_detec
    congestion_detec >> inteligent_optimization
    db_cong >> inteligent_optimization

    inteligent_optimization >> db_semaf
    inteligent_optimization >> traffic_light_control
    db_semaf >> monitor >> user
    user >> monitor >> traffic_light_control >> sumo