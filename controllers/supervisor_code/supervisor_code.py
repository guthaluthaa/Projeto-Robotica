from controller import Supervisor
import os

#supervisor
supervisor = Supervisor()

# Tempo de atualização
TIME_STEP = 64

# Lista com os nomes das caixas que definimos no .wbt)
box_names = ['BOX1', 'BOX2', 'BOX3', 'BOX4', 'BOX5', 'BOX6', 'BOX7', 'BOX8', 'BOX9','BOX10']

# Dicionário para armazenar as posições iniciais
initial_positions = {}

# Função para obter a posição de todas as caixas
def get_boxes_positions():
    positions = {}
    for name in box_names:
        box = supervisor.getFromDef(name)
        if box is not None:
            positions[name] = box.getPosition()
        else:
            print(f"Erro: Não foi possível encontrar a caixa {name}")
    return positions


for _ in range(10):
    supervisor.step(TIME_STEP)

initial_positions = get_boxes_positions()

def has_box_moved(initial_pos, current_pos, threshold=0.001):
    for i in range(3):
        if abs(initial_pos[i] - current_pos[i]) > threshold:
            return True
    return False

def is_box_moved():
    current_positions = get_boxes_positions()
    for name in box_names:
        if has_box_moved(initial_positions[name], current_positions[name]):
            return True
    return False

file_path = "C:/tmp/caixa_movida.txt"
if os.path.exists(file_path):
    os.remove(file_path)

while supervisor.step(TIME_STEP) != -1:
    if is_box_moved():
        print("Caixa leve foi encontrada e movida!")
        with open(file_path, "w") as f:
            f.write("Caixa leve encontrada")
        break