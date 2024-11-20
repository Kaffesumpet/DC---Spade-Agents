# Authored by:
# Mona Tlili
# Nicklas Kjellbom
# Filip Lindgren Dewari
# Thomas Stabforsmo Norell

import spade

# class DummyAgent(spade.agent.Agent):
#     async def setup(self):
#         print("Hello World! I'm agent {}".format(str(self.jid)))

# async def main():
#     dummy = DummyAgent("monatlilijabber.cz@", "jagskainteglommamittlosenord")
#     await dummy.start()

# if __name__ == "__main__":
#     spade.run(main())

class DummyAgent(spade.agent.Agent):
    async def setup(self):
        print("Hello! I'm agent {}".format(str(self.jid)), "pew pew")

async def main():
    dummy = DummyAgent("thompe@jabbers.one", "Jagkommerglommamitt")
    await dummy.start()

if __name__ == "__main__":
    spade.run(main())


# Creating an agent with behaviours
# import asyncio
# import spade
# from spade import wait_until_finished
# from spade.agent import Agent
# from spade.behaviour import CyclicBehaviour

# class DummyAgent(Agent):
#     class MyBehav(CyclicBehaviour):
#         async def on_start(self):
#             print("Starting behaviour . . .")
#             self.counter = 0

#         async def run(self):
#             print("Counter: {}".format(self.counter))
#             self.counter += 1
#             await asyncio.sleep(1)

#     async def setup(self):
#         print("Agent starting . . .")
#         b = self.MyBehav()
#         self.add_behaviour(b)

# async def main():
#     dummy = DummyAgent("your_jid@your_xmpp_server", "your_password")
#     await dummy.start()
#     print("DummyAgent started. Check its console to see the output.")

#     print("Wait until user interrupts with ctrl+C")
#     await wait_until_finished(dummy)

# if __name__ == "__main__":
#     spade.run(main())


# Creating an agent from within another agent
# import spade
# from spade.agent import Agent
# from spade.behaviour import OneShotBehaviour

# class AgentExample(Agent):
#     async def setup(self):
#         print(f"{self.jid} created.")

# class CreateBehav(OneShotBehaviour):
#     async def run(self):
#         agent2 = AgentExample("filledill@jabbers.one", "Jagharredanglomtmitt")
#         await agent2.start(auto_register=True)

# async def main():
#     agent1 = AgentExample("thompe@jabbers.one", "Jagkommerglommamitt")
#     behav = CreateBehav()
#     agent1.add_behaviour(behav)
#     await agent1.start(auto_register=True)

#     # wait until the behaviour is finished to quit spade.
#     await behav.join()

# if __name__ == "__main__":
#     spade.run(main())


#Sending and receiving messages between agents
# import spade
# from spade.agent import Agent
# from spade.behaviour import OneShotBehaviour
# from spade.message import Message
# from spade.template import Template

# class SenderAgent(Agent):
#     class InformBehav(OneShotBehaviour):
#         async def run(self):
#             print("InformBehav running")
#             msg = Message(to="filledill@jabbers.one")     # Instantiate the message
#             msg.set_metadata("performative", "inform")  # Set the "inform" FIPA performative
#             msg.body = "Tjeeeeena Filleeeeeeh!"                    # Set the message content

#             await self.send(msg)
#             print("Message sent!")

#             # stop agent from behaviour
#             await self.agent.stop()

#     async def setup(self):
#         print("SenderAgent started")
#         b = self.InformBehav()
#         self.add_behaviour(b)

# class ReceiverAgent(Agent):
#     class RecvBehav(OneShotBehaviour):
#         async def run(self):
#             print("RecvBehav running")

#             msg = await self.receive(timeout=10) # wait for a message for 10 seconds
#             if msg:
#                 print("Message received with content: {}".format(msg.body))
#             else:
#                 print("Did not received any message after 10 seconds")

#             # stop agent from behaviour
#             await self.agent.stop()

#     async def setup(self):
#         print("ReceiverAgent started")
#         b = self.RecvBehav()
#         template = Template()
#         template.set_metadata("performative", "inform")
#         self.add_behaviour(b, template)

# async def main():
#     receiveragent = ReceiverAgent("filledill@jabbers.one", "Jagharredanglomtmitt")
#     await receiveragent.start(auto_register=True)
#     print("Receiver started")

#     senderagent = SenderAgent("thompe@jabbers.one", "Jagkommerglommamitt")
#     await senderagent.start(auto_register=True)
#     print("Sender started")

#     await spade.wait_until_finished(receiveragent)
#     print("Agents finished")

# if __name__ == "__main__":
#     spade.run(main())