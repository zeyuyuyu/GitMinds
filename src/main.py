# src/main.py

import asyncio
import random

class SwarmAgent:
    def __init__(self, id):
        self.id = id
        self.neighbors = []
        self.state = 'idle'
        self.consensus_value = None

    async def run(self):
        while True:
            if self.state == 'idle':
                await self.discover_neighbors()
                await self.join_consensus()
            elif self.state == 'consensus':
                await self.reach_consensus()
            await asyncio.sleep(random.uniform(0.1, 1))

    async def discover_neighbors(self):
        # Discover neighboring agents in the swarm
        self.neighbors = [SwarmAgent(i) for i in range(random.randint(3, 10))]
        self.state = 'consensus'

    async def join_consensus(self):
        # Join the decentralized consensus protocol
        self.consensus_value = random.randint(0, 100)
        await self.broadcast_value()

    async def reach_consensus(self):
        # Reach consensus with neighboring agents
        await self.aggregate_values()
        if self.is_consensus_reached():
            self.state = 'idle'
        else:
            await self.broadcast_value()

    async def broadcast_value(self):
        # Broadcast the current consensus value to neighbors
        await asyncio.gather(*[neighbor.receive_value(self.consensus_value) for neighbor in self.neighbors])

    async def receive_value(self, value):
        # Receive a consensus value from a neighboring agent
        self.consensus_value = value

    async def aggregate_values(self):
        # Aggregate the consensus values from neighboring agents
        self.consensus_value = sum([agent.consensus_value for agent in self.neighbors]) / len(self.neighbors)

    def is_consensus_reached(self):
        # Check if the swarm has reached a consensus
        return all(abs(agent.consensus_value - self.consensus_value) < 1 for agent in self.neighbors)

async def main():
    agents = [SwarmAgent(i) for i in range(10)]
    await asyncio.gather(*[agent.run() for agent in agents])

if __name__ == '__main__':
    asyncio.run(main())
