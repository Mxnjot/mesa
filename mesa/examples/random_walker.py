import sys
import mesa
print("Mesa location:", mesa.__file__)
print("Python paths:", sys.path)

from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer

class RandomWalker(Agent):
    """An agent that moves randomly on a grid."""
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        # Move to a random adjacent cell
        possible_steps = self.model.grid.get_neighborhood(
            self.pos, moore=True, include_center=False
        )
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)

class RandomWalkModel(Model):
    """A simple model with random walkers."""
    def __init__(self, num_agents, width, height):
        self.num_agents = num_agents
        self.grid = MultiGrid(width, height, torus=True)
        self.schedule = RandomActivation(self)
        self.running = True

        # Create agents
        for i in range(self.num_agents):
            a = RandomWalker(i, self)
            self.schedule.add(a)
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(a, (x, y))

        self.datacollector = DataCollector(
            {"Agent Count": lambda m: m.schedule.get_agent_count()}
        )

    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()

# Visualization
def agent_portrayal(agent):
    return {"Shape": "circle", "Color": "blue", "Filled": True, "r": 0.5}

grid = CanvasGrid(agent_portrayal, 10, 10, 500, 500)

server = ModularServer(
    RandomWalkModel,
    [grid],
    "Random Walkers",
    {"num_agents": 10, "width": 10, "height": 10}
)

if __name__ == "__main__":
    server.launch()
