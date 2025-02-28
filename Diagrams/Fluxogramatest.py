from graphviz import Digraph

dot = Digraph("Fluxograma")

dot.node("A", "Início")
dot.node("B", "Coletar dados do SUMO\n (Dados de trafego)")
dot.node("C", "Banco de dados do congestionamento")
dot.node("D", "Calcula o tempo de ciclo otimizado (Formula de Webster)")
dot.node("if", "Mudança no tempo de ciclo é significante?")
dot.node("E", "Define o tempo de verde para cada via")
dot.node("F", "Banco de dados dos semáforos")
dot.node("G", "Controlador dos semáforos")
dot.node("H", "Sumo")
dot.node("Wait", "Espera")

dot.edge("A", "B")
dot.edge("B", "C")
dot.edge("C", "D")
dot.edge("D", "if")
dot.edge("if", "Wait", label= "Não é significante")
dot.edge("if", "E", label= "É significante")
dot.edge("Wait","B", label= "Apos T segundos")
dot.edge("E", "F")
dot.edge("F", "G")
dot.edge("G", "H")
dot.edge("H","B", label="Apos T tempo")

dot.render("fluxograma", format="png", view=True)  # Gera e exibe o fluxograma