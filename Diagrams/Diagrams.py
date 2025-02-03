from diagrams import Cluster, Diagram
from diagrams.custom import Custom
from diagrams.aws.database import Dynamodb, DMS
from diagrams.aws.general import Client, User
from diagrams.aws.compute import Lambda, EC2

with Diagram("Sistema dinâmico de semáforos (Overall)", show=False, node_attr={"fontsize": "16", "fontname": "Arial"}):
    with Cluster("API", graph_attr={"bgcolor": "lightblue"}):
        tomtom = Custom("", r"./resources/TomTomSymbol.png")
        another_api = Custom("Another API", r"./resources/API.png")
        api = [tomtom, another_api]

    with Cluster("Cloud", graph_attr={"bgcolor": "#00CC99"}):
        lambda_function = EC2("Algorithm")
        db = Dynamodb("Database")

    with Cluster("Simulation", graph_attr={"bgcolor": "#FFCC66"}):
        sumo = Custom("", r"./resources/SUMO.png")
        traffic = Custom("Traffic Light", r"./resources/traffic-light.png")
        simul = [sumo, traffic]

    with Cluster("Interface", graph_attr={"bgcolor": "#FFFF99"}):
        monitor = Client("Monitor")
        user = User("User")

    api >> db >> lambda_function
    lambda_function >> simul
    lambda_function >> monitor >> user
    user >> monitor >> lambda_function