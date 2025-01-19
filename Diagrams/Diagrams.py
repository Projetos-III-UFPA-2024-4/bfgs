from diagrams import Cluster, Diagram
from diagrams.custom import Custom
from diagrams.aws.database import DatabaseMigrationService, DMS
from diagrams.aws.general import Client, User

with Diagram("Sistema dinamico de Semaforos", show=False):
    api = Custom("TomTom or ...", r".\resources\API_2.png")
    db = DMS("Database")

    with Cluster("Cloud"):
        aws = Custom("AWS services", r".\resources\AWS.png")

    with Cluster("Simulation"):
       sumo = Custom("Sumo", r".\resources\SUMO.png")
       traffic = Custom("Traffic Light", r".\resources\traffic-light.png")
       simul = [sumo, traffic]

    with Cluster("Interface"):
        monitor = Client("Monitor")
        user = User("User")
        monitor >> user

    api >> db
    db >> aws
    aws >> simul
    aws >> monitor