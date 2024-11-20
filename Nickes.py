import random
import operator
from spade.agent import Agent
from spade.behaviour import FSMBehaviour, State

# function for generate_question_state 
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

# Start of game state
def main():
    score = 10
    total_questions = 10
    
    print("Welcome to the math game!")
    print("Answer the questions correctly to earn points.\n")
    # Generate question state
    for i in range(1, total_questions + 1): 
        num1, symbol, num2, correct_answer = generate_question()
        attempts = 0
        
        while attempts < 3:
            try:
                user_answer = float(input(f"Question {i}: What is {num1} {symbol} {num2}? "))
                if user_answer == correct_answer:
                    print("Correct! Well done!")
                    break
                else:
                    print("Incorrect. Try again.")
                    score -= 0.25
                    attempts += 1
            except ValueError: 
                print("Please enter a valid number.")
                attempts += 1 
        
        if attempts == 3:
            print(f"Sorry! The correct answer was {correct_answer}.")
            score -= 0.25

    # End state
    print("\nGame Over!")
    print(f"Your final score is: {score:.2f} / {total_questions}")
    
    if score >= 8:
        print("Congratulations! You won the game!")
    else:
        print("Better luck next time, sucker!")

if __name__ == "__main__":
    main()


class start_of_game(State):
    score = 10
    total_questions = 10
    
    print("Welcome to the math game!")
    print("Answer the questions correctly to earn points.\n")
    

class question_generation_state(State):
    num1, symbol, num2, correct_answer = generate_question()
    user_answer = float(input(f"Question {i}: What is {num1} {symbol} {num2}? "))