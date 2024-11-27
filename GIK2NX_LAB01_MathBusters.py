# Students
# Nicklas Kjellbom h22nikje@du.se
# Filip Lindgren Dewari h22filil@du.se
# Thomas Stabforsmo Norell h22thsta@du.se
# Mona Tlili h22motli@du.se

import asyncio
import random
import operator
from spade.agent import Agent
from spade.behaviour import FSMBehaviour, State

# Define states that will be used by the agent (Finite State Machine Behaviour)
# https://spade-mas.readthedocs.io/en/latest/behaviours.html#finite-state-machine-behaviour
STATE_ONE = "START"
STATE_TWO = "GENERATE_QUESTION"
STATE_THREE = "PRESENT_QUESTION"
STATE_FOUR = "CHECK_ANSWER"
STATE_FIVE = "SCORE"
STATE_SIX = "END" 

# Define a custom FSMBehaviour for managing the game states
class MathBustersFSM(FSMBehaviour):
    async def on_start(self):
        print("Agent has successfully adapted the GameMaster persona")
        print("[GameMaster] Welcome to MathBusters!")

    async def on_end(self):
        print("[GameMaster] Thanks for playing MathBusters, don't forget to do maths in real life as well!")
        await self.agent.stop()

# StartState is the game start menu
# The player is given the option to decide how many questions the game will consist
class StartState(State):
    async def run(self):
        while True:
            try:
                max_questions = int(input("[GameMaster] How many questions would you like to answer? "))
                if max_questions <= 0:
                    raise ValueError("The number of questions must be positive.")
                break
            except ValueError as e:
                print(f"[GameMaster] Invalid input: {e}. Please enter a positive integer.")

        # Set the shared attributes in the agent
        self.agent.max_questions = max_questions
        self.agent.points = max_questions

        print(f"[GameMaster] Great! You'll answer {self.agent.max_questions} questions. Let's get started!")

        # Set the next state
        self.set_next_state(STATE_TWO) # Start -> Generate Question

# The state responsible for generating a new question
class GenerateQuestionState(State):
    """
        Generates a random math question and stores it in the agent.
        Initializes the number of attempts for the current question.
        Transitions to the state where the question is presented.
    """
    # Function to generate simple math question aimed at kids age 10-12
    # All maths utilize appropriate bounds.
    # Divison whole numbers are ensured by making numerator the result of denominator times another number.
    def generate_question(self):
        operators = {
            1: ('+', operator.add, (1, 1000)), 
            2: ('-', operator.sub, (1, 1000)),
            3: ('*', operator.mul, (1, 12)),
            4: ('/', operator.floordiv, (1, 12)),
        }

        symbol, operation, bounds = operators[random.randint(1, 4)]

        if symbol == '/':
            num2 = random.randint(bounds[0], bounds[1])
            num1 = num2 * random.randint(1, 12)
        elif symbol == '-':
            num1 = random.randint(bounds[0], bounds[1])
            num2 = random.randint(bounds[0], num1)
        else:
            num1 = random.randint(bounds[0], bounds[1])
            num2 = random.randint(bounds[0], bounds[1])

        return num1, symbol, num2, operation(num1, num2)

    async def run(self):
        self.agent.num1, self.agent.symbol, self.agent.num2, self.agent.correct_answer = self.generate_question()
        self.agent.attempts = 3
        self.set_next_state(STATE_THREE) # Generate Question -> Present Question

# The state where the question is presented to the user
class PresentQuestionState(State):
    async def run(self):
        print(f"[GameMaster] Question: What is {self.agent.num1} {self.agent.symbol} {self.agent.num2}?")
        self.set_next_state(STATE_FOUR) # Present Question -> Check Answer

# The state where the user's answer is checked
class CheckAnswerState(State):
    async def run(self):
        """
        Accepts the user's answer and verifies its correctness.
        - If correct: Transitions to the scoring state.
        - If incorrect: Reduces attempts and either retries the same question or transitions to scoring.
        """
        try:
            user_answer = int(input("Your answer: "))
            if user_answer == self.agent.correct_answer:
                print("[GameMaster] Correct!")
                self.set_next_state(STATE_FIVE)  # Check Answer -> Score
            else:
                self.agent.attempts -= 1
                print(f"[GameMaster] Wrong! You have {self.agent.attempts} attempts left.")
                if self.agent.attempts > 0:
                    self.agent.points -= 0.25
                    self.set_next_state(STATE_THREE) # Retry on wrong answer
                else:
                    print(f"[GameMaster] The correct answer was {self.agent.correct_answer}.")
                    self.agent.points -= 0.5
                    self.set_next_state(STATE_FIVE)  # Check Answer -> Score
        except ValueError:
            print("[GameMaster] Invalid input. Please enter a number.")
            self.set_next_state(STATE_THREE)  # Retry the same question (No loses of attempts)

# The state of the game
class ScoreState(State):
    async def run(self):
        if self.agent.current_question < self.agent.max_questions:
            self.agent.current_question += 1
            self.set_next_state(STATE_TWO) # Score -> Generate Question (Next question)
        else:
            self.set_next_state(STATE_SIX) # Score -> End

class EndState(State):
    async def run(self):
        """Displays the final score and ends the game."""
        print(f"[GameMaster] Final score: {self.agent.points}. Do you want to play again? (y/n)")

        user_answer = input("Your answer: ").strip().lower()

        if user_answer == "y":
            user_answer = None
            self.agent.current_question = 1
            self.set_next_state(STATE_ONE)
        elif user_answer == "n":
            print("[GameMaster] Thank you for playing! Goodbye!")
            await self.agent.stop() # Terminates the game
        else:
            print("[GameMaster] Invalid input. Please answer with 'y' or 'n'.")
            await self.run()  # Prompt again if the input is invalid

class MathBustersAgent(Agent):
    """
        Sets up the agent with initial parameters and attaches the FSM behaviour.
        - Initializes game parameters such as max questions, current question, points, and attempts.
        - Configures and starts the FSMBehaviour with defined states and transitions.
    """
    async def setup(self):
        self.max_questions = 0  # Value is chosen by the player
        self.points = 0  # Value is chosen by the player
        self.current_question = 1
        self.attempts = 3

        fsm = MathBustersFSM()
        fsm.add_state(name=STATE_ONE, state=StartState(), initial=True)
        fsm.add_state(name=STATE_TWO, state=GenerateQuestionState())
        fsm.add_state(name=STATE_THREE, state=PresentQuestionState())
        fsm.add_state(name=STATE_FOUR, state=CheckAnswerState())
        fsm.add_state(name=STATE_FIVE, state=ScoreState())
        fsm.add_state(name=STATE_SIX, state=EndState())

        fsm.add_transition(source=STATE_ONE, dest=STATE_TWO)  # Start -> Generate Question
        fsm.add_transition(source=STATE_TWO, dest=STATE_THREE)  # Generate Question -> Present Question
        fsm.add_transition(source=STATE_THREE, dest=STATE_FOUR)  # Present Question -> Check Answer
        fsm.add_transition(source=STATE_FOUR, dest=STATE_FIVE)  # Check Answer -> Score
        fsm.add_transition(source=STATE_FOUR, dest=STATE_THREE)  # Retry on wrong answer
        fsm.add_transition(source=STATE_FIVE, dest=STATE_TWO)  # Score -> Generate Question (Next question)
        fsm.add_transition(source=STATE_FIVE, dest=STATE_SIX)  # Score -> End
        fsm.add_transition(source=STATE_SIX, dest=STATE_ONE)  # Score -> End


        self.add_behaviour(fsm) # Attach the FSM behaviour to the agent

async def main():
    agent = MathBustersAgent("kaffesumpet@magicbroccoli.de", "enkopptack")
    await agent.start()

    while agent.is_alive():
        await asyncio.sleep(1) # Keep the script running while the agent is alive

if __name__ == "__main__":
    asyncio.run(main())
