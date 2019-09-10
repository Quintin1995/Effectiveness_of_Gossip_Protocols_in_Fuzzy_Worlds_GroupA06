class PhonebookType:
    ALL     = 1     # Everyone is in the phonebook

def generate_phonebook (phonebook_type, amount_agents):
    phonebook = list()

    if phonebook_type == PhonebookType.ALL:
        for agent_idx in range (amount_agents):
            phonebook.append(list())
            phonebook.append(list(range(amount_agents)))
        
            # Remove ourselves from the list
            if agent_idx in phonebook:
                phonebook.remove(agent_idx)
    return phonebook