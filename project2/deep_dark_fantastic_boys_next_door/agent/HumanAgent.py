
class HumanAgent:

    def __init__(self):
        pass

    def get_next_action(self, state, player):
        actions = state.all_next_action()

        for i, action in enumerate(actions):
            print(i, ":", action)

        choose = int(input("your choice: "))

        return actions[choose]
