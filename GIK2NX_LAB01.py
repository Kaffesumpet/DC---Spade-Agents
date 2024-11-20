# Authored by:
# Mona Tlili
# Nicklas Kjellbom
# Filip Lindgren Dewari
# Thomas Stabforsmo Norell

import spade
from spade.agent import Agent
from spade.behaviour import FSMBehaviour, State
from spade.message import Message
import random
import operator

STATE_ONE = "START"
STATE_TWO = "GENERATE_QUESTION"
STATE_THREE = "PRESENT_QUESTION"
STATE_FOUR = "CHECK_ANSWER"
STATE_FIVE = "SCORE"
STATE_SIX = "END"

def generate_question():
    operators = {
        1: ('+', operator.add, (1, 1000)), 
        2: ('-', operator.sub, (1, 1000)), 
        3: ('*', operator.mul, (1, 12)), 
        4: ('/', operator.floordiv, (1, 12))
    }
    
    dice_roll = random.randint(1, 4) 
    symbol, operation, bounds = operators[dice_roll]
    
    if symbol == '/':  
        while True: 
            num1 = random.randint(1, bounds[1])
            num2 = random.randint(1, bounds[1])
            if num2 != 0 and num1 % num2 == 0:
                break
    elif symbol == '-':
        num1 = random.randint(bounds[0], bounds[1])
        num2 = random.randint(bounds[0], num1)    
    else:
        num1 = random.randint(bounds[0], bounds[1]) 
        num2 = random.randint(bounds[0], bounds[1])
    
    return num1, symbol, num2, operation(num1, num2)

class MathBustersFSM(FSMBehaviour):
    async def on_start(self): 
        print(f"Agent starting FSM game in {self.current_state}")

    async def on_end(self):
        print(f"FSM finished at state {self.current_state}")
        await self.agent.stop() 

class StartState(State):
    async def run(self):
        print("Welcome to MathBusters!")
        print("An interactive math game where you can earn points by answering questions correctly.")
        self.set_next_state(STATE_TWO)

class GenerateQuestionState(State):
    async def run(self):
        for i in range(1, total_questions + 1): 
            num1, symbol, num2, correct_answer = generate_question()
            attempts = 0
        self.set_next_state(STATE_THREE)

class PresentQuestionState(State):
    async def run(self):
       
        # no final state is setted, since this is a final state'
        self.set_next_state(STATE_FOUR)

class CheckAnswerState(State):
    async def run(self):
        print("I'm at state three (final state)")
        msg = await self.receive(timeout=5)
        print(f"State Three received message {msg.body}")
        self.set_next_state(STATE_FIVE)

class ScoreState(State): 
    async def run(self):
        print("I'm at state three (final state)")
        msg = await self.receive(timeout=5)
        print(f"State Three received message {msg.body}")
        self.set_next_state(STATE_SIX)

class EndState(State):
    async def run(self):
        print("I'm at state three (final state)")
        msg = await self.receive(timeout=5)
        print(f"State Three received message {msg.body}")
        self.set_next_state("??")

class FSMAgent(Agent):
    async def setup(self):
        fsm = MathBustersFSM()
        fsm.add_state(name=STATE_ONE, state=StartState(), initial=True)
        fsm.add_state(name=STATE_TWO, state=GenerateQuestionState())
        fsm.add_state(name=STATE_THREE, state=PresentQuestionState())
        fsm.add_state(name=STATE_FOUR, state=CheckAnswerState())
        fsm.add_state(name=STATE_FIVE, state=ScoreState())
        fsm.add_state(name=STATE_SIX, state=EndState())
        
        fsm.add_transition(source=STATE_ONE, dest=STATE_TWO)
        fsm.add_transition(source=STATE_TWO, dest=STATE_THREE)
        fsm.add_transition(source=STATE_THREE, dest=STATE_FOUR)
        fsm.add_transition(source=STATE_FOUR, dest=STATE_FIVE)
        fsm.add_transition(source=STATE_FIVE, dest=STATE_SIX)
        self.add_behaviour(fsm)


async def main():
    fsmagent = FSMAgent("filledill@jabbers.one", "Jagharredanglomtmitt")
    await fsmagent.start()

    await spade.wait_until_finished(fsmagent)
    await fsmagent.stop()
    print("Agent finished")

if __name__ == "__main__":
    spade.run(main())


# class DummyAgent(spade.agent.Agent):
#     async def setup(self):
#         print("Hello! I'm agent {}".format(str(self.jid)), "pew pew")

# async def main(): 
#     dummy = DummyAgent("thompe@jabbers.one", "Jagkommerglommamitt")
#     await dummy.start()

# if __name__ == "__main__": 
#     spade.run(main()) 


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
#     dummy = DummyAgent("thompe@jabbers.one", "Jagkommerglommamitt")
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