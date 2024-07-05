import random
import json
import os
import torch
import sys

from model import NeuralNet
from nltk_utils import bag_of_words, tokenize

if len(sys.argv) < 2:
    print("Erro de uso")
    sys.exit(1)

# Pega todos os argumentos a partir do índice 1 e une em uma única string
sentence = " ".join(sys.argv[1:])
if sentence == "quit":
    print("You're out!")
    sys.exit(0)

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Obtenha o caminho absoluto do diretório atual
current_dir = os.path.dirname(os.path.abspath(__file__))
# Combine o caminho absoluto com o nome do arquivo
file_path = os.path.join(current_dir, 'intents.json')

if os.path.exists(file_path):
    with open(file_path, 'r') as f:
        intents = json.load(f)

FILE = "data.pth"
data = torch.load(FILE)

input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data['all_words']
tags = data['tags']
model_state = data["model_state"]

model = NeuralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()

bot_name = "Jarvis"

sentence = tokenize(sentence)
X = bag_of_words(sentence, all_words)
X = X.reshape(1, X.shape[0])
X = torch.from_numpy(X).to(device)

output = model(X)
_, predicted = torch.max(output, dim=1)

tag = tags[predicted.item()]

probs = torch.softmax(output, dim=1)
prob = probs[0][predicted.item()]
if prob.item() > 0.75:
    for intent in intents['intents']:
        if tag == intent["tag"]:
            print(f"{bot_name}: {random.choice(intent['responses'])}")
else:
    print(f"{bot_name}: Desculpe, acho que não entendi o que você quis dizer ou não possuo esse conhecimento no momento. Poderia reformular ou fazer outra pergunta, por favor?")