
from .MaxnAgent import MaxnAgent


class HumanAgent:

    def __init__(self, upstream, downstream, depth):
        self.upstream = upstream
        self.downstream = downstream
        self.arrived_strategy_points = False
        self.depth = depth
        self.search_agent = MaxnAgent(self.depth)
        self.strategy_points = None

    def strategy_point_occupied(self, state, point):
        return point in state.pieces_player_dict

    def update_strategy_points(self, state):
        if state.is_player_knock_out(self.upstream):
            for point in STRATEGIC_POINTS[state.playing_player][:2]:
                if point in self.strategy_points:
                    self.strategy_points.remove(point)
        if state.is_player_knock_out(self.downstream):
            for point in STRATEGIC_POINTS[state.playing_player][2:]:
                if point in self.strategy_points:
                    self.strategy_points.remove(point)

    def get_next_action(self, state, player):
        # if state.turns == 1:
        #     return "MOVE", ((-3, 3), (-2, 3))
        action = input("Enter action: ").upper()
        from_q = int(input("Jump from(q): "))
        from_r = int(input("Jump from(r): "))
        to_q = int(input("Jump to(q): "))
        to_r = int(input("Jump to(r): "))
        return action, ((from_q, from_r), (to_q, to_r))
