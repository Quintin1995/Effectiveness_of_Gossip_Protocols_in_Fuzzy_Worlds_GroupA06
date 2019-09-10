from enum import Enum
import math
import random
import protocols
from protocols import Protocols
from phonebook import PhonebookType
from model import Model

class LiarType (Enum):
    BLUFFER     = 1
    SABOTEUR    = 2

AMOUNT_AGENTS   = 22
MAX_SECRET      = 22
TRANSFER_CHANCE = 100
PROTOCOL        = Protocols.ANY
ITERATIONS      = 60
PHONEBOOKTYPE   = PhonebookType.ALL

gossip_model = Model(AMOUNT_AGENTS, MAX_SECRET, TRANSFER_CHANCE, PROTOCOL, PHONEBOOKTYPE)

# Main loop
for iteration in range(ITERATIONS):
    gossip_model.next_call()

for target_idx in range (AMOUNT_AGENTS):
    for agent_idx in range (AMOUNT_AGENTS):
        print ("Agent {} thinks agent {} has secret #{}".format(agent_idx, target_idx, gossip_model.get_secret_value(agent_idx, target_idx)))

    agent_secret = gossip_model.get_agent_secret(target_idx)
    print ("Agent {} has secret #{}".format(target_idx, agent_secret))
    print ()