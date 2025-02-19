import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from mlagents_envs.environment import UnityEnvironment
from mlagents_envs.base_env import ActionTuple

env = UnityEnvironment(file_name="IndustrialEnvironment")
env.reset()
behavior_name = list(env.behavior_specs.keys())[0]
spec = env.behavior_specs[behavior_name]

class WorkerAgent(nn.Module):
    def __init__(self):
        super(WorkerAgent, self).__init__()
        self.fc1 = nn.Linear(8, 64)
        self.fc2 = nn.Linear(64, 32)
        self.fc3 = nn.Linear(32, 2)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        return torch.tanh(self.fc3(x))

agent = WorkerAgent()
optimizer = optim.Adam(agent.parameters(), lr=0.001)
criterion = nn.MSELoss()

def select_action(state):
    with torch.no_grad():
        return agent(torch.tensor(state, dtype=torch.float32)).numpy()

for episode in range(500):
    env.reset()
    decision_steps, terminal_steps = env.get_steps(behavior_name)
    state = decision_steps.obs[0][0]

    for step in range(200):
        action = select_action(state)
        action_tuple = ActionTuple()
        action_tuple.add_continuous(np.array([action]))
        env.set_actions(behavior_name, action_tuple)
        env.step()

        decision_steps, terminal_steps = env.get_steps(behavior_name)
        if len(decision_steps) > 0:
            next_state = decision_steps.obs[0][0]
            reward = decision_steps.reward[0]
            done = len(terminal_steps) > 0

            predicted = agent(torch.tensor(state, dtype=torch.float32))
            target = torch.tensor(action, dtype=torch.float32)
            loss = criterion(predicted, target)

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            state = next_state

            if done:
                break

print("Training complete!")
env.close()
