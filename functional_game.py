import asyncio
import random
import operator
from spade.agent import Agent
from spade.behaviour import FSMBehaviour, State

# Define states
STATE_ONE = "START"
STATE_TWO = "GENERATE_QUESTION"
STATE_THREE = "PRESENT_QUESTION"
STATE_FOUR = "CHECK_ANSWER"
STATE_FIVE = "SCORE"
STATE_SIX = "END"

# Function to generate simple math question aimed at kids age 10-12
def generate_question():
    operators = {
        1: ('+', operator.add, (1, 1000)),
        2: ('-', operator.sub, (1, 1000)),
        3: ('*', operator.mul, (1, 12)),
        4: ('/', operator.floordiv, (1, 12)),
    }
    dice_roll = random.randint(1, 4)
    symbol, operation, bounds = operators[dice_roll]

    # Only divisions that results in whole numbers is allowed.
    if symbol == '/':
        while True:
            num1 = random.randint(1, bounds[1])
            num2 = random.randint(1, bounds[1])
            if num2 != 0 and num1 % num2 == 0:
                break
    # Ensure non-negative results for subtraction by limiting making the upper limit of num2 = num 1
    elif symbol == '-':
        num1 = random.randint(bounds[0], bounds[1])
        num2 = random.randint(bounds[0], num1)
    else:
        # For addition and multiplication, pick random numbers within bounds
        num1 = random.randint(bounds[0], bounds[1])
        num2 = random.randint(bounds[0], bounds[1])

    return num1, symbol, num2, operation(num1, num2)

# Define a custom FSMBehaviour for managing the game states
class MathBustersFSM(FSMBehaviour):
    async def on_start(self):
        print("Agent has successfully adapted the GameMaster persona")

    async def on_end(self):
        print("[GameMaster] Thanks for playing MathBusters, don't forget to do maths irl too!")
        await self.agent.stop()

# The starting state of the game
class StartState(State):
    async def run(self):
        print("[GameMaster] Welcome to MathBusters!")
        self.set_next_state(STATE_TWO)

# The state responsible for generating a new question
class GenerateQuestionState(State):
    """
        Generates a random math question and stores it in the agent.
        Initializes the number of attempts for the current question.
        Transitions to the state where the question is presented.
    """
    async def run(self):
        self.agent.num1, self.agent.symbol, self.agent.num2, self.agent.correct_answer = generate_question()
        self.agent.attempts = 3 
        self.set_next_state(STATE_THREE)

# The state where the question is presented to the user
class PresentQuestionState(State):
    async def run(self):
        print(f"[GameMaster] Question: What is {self.agent.num1} {self.agent.symbol} {self.agent.num2}?")
        self.set_next_state(STATE_FOUR)

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
                self.set_next_state(STATE_FIVE)  # Proceed to scoring
            else:
                self.agent.attempts -= 1
                print(f"[GameMaster] Wrong! You have {self.agent.attempts} attempts left.")
                if self.agent.attempts > 0:
                    self.agent.points -= 0.25
                    self.set_next_state(STATE_THREE)  # Retry the same question
                else:
                    print(f"[GameMaster] The correct answer was {self.agent.correct_answer}.")
                    self.agent.points -= 0.5
                    self.set_next_state(STATE_FIVE)  # Move to scoring
        except ValueError:
            print("[GameMaster] Invalid input. Please enter a number.")
            self.set_next_state(STATE_THREE)  # Retry the same question

# The final state of the game
class ScoreState(State):
    async def run(self):
        """Displays the final score and ends the game."""
        print(f"[GameMaster] Your score: {self.agent.points}")
        if self.agent.current_question < self.agent.max_questions:
            self.agent.current_question += 1
            self.set_next_state(STATE_TWO)
        else:
            self.set_next_state(STATE_SIX)

class EndState(State):
    async def run(self):
        print(f"[GameMaster] Game over! Final score: {self.agent.points}")
        self.kill()

class MathBustersAgent(Agent):
    """
        Sets up the agent with initial parameters and attaches the FSM behaviour.
        - Initializes game parameters such as max questions, current question, points, and attempts.
        - Configures and starts the FSMBehaviour with defined states and transitions.
    """
    async def setup(self):
        self.max_questions = 2
        self.current_question = 1
        self.points = 5
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

        self.add_behaviour(fsm) # Attach the FSM behaviour to the agent

async def main():
    agent = MathBustersAgent("kaffesumpet@magicbroccoli.de", "enkopptack")
    await agent.start()

    while agent.is_alive():
        await asyncio.sleep(1) # Keep the script running while the agent is alive

if __name__ == "__main__":
    asyncio.run(main())