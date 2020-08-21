import torch.nn as nn
import torch.nn.functional as F
import torch


class Critic(nn.Module):
    def __init__(self, state_dim, action_dim):
        super(Critic, self).__init__()

        # Q1 architecture
        self.l1 = nn.Linear(state_dim + action_dim, 500)
        self.l2 = nn.Linear(500, 256)
        self.l3 = nn.Linear(256, 256)
        self.l4 = nn.Linear(256, 64)
        self.l5 = nn.Linear(64, 1)

        # Q2 architecture
        self.l6 = nn.Linear(state_dim + action_dim, 500)
        self.l7 = nn.Linear(500, 256)
        self.l8 = nn.Linear(256, 256)
        self.l9 = nn.Linear(256, 64)
        self.l10 = nn.Linear(64, 1)

    def forward(self, state, action):
        sa = torch.cat([state, action], 1)

        q1 = F.relu(self.l1(sa))
        q1 = F.relu(self.l2(q1))
        q1 = F.relu(self.l3(q1))
        q1 = F.relu(self.l4(q1))

        q1 = self.l5(q1)

        q2 = F.relu(self.l6(sa))
        q2 = F.relu(self.l7(q2))
        q2 = F.relu(self.l8(q2))
        q2 = F.relu(self.l9(q2))

        q2 = self.l10(q2)
        return q1, q2

    def Q1(self, state, action):
        sa = torch.cat([state, action], 1)

        q1 = F.relu(self.l1(sa))
        q1 = F.relu(self.l2(q1))
        q1 = F.relu(self.l3(q1))
        q1 = F.relu(self.l4(q1))

        q1 = self.l5(q1)
        return q1
