import random
from vocabulary import vocab


# Function to start the game
def start_game():
    print("Welcome to the Swedish Learning Game!")
    print("Choose a category to start learning:\n")

    categories = list(vocab.keys())
    
    while True:
        for i, category in enumerate(categories, 1):
            print(f"{i}. {category.capitalize()}")
        
        try:
            category_choice = int(input("\nEnter the number of your chosen category: ")) - 1
            if category_choice < 0 or category_choice >= len(categories):
                print(f"Invalid choice, please select a number between 1 and {len(categories)}.\n")
                continue
            chosen_category = categories[category_choice]
            break
        except ValueError:
            print(f"Invalid input. Please enter a number between 1 and {len(categories)}.\n")

    words = vocab[chosen_category]
    score = 0

    print(f"\nStarting quiz on {chosen_category.capitalize()}! Type 'exit' anytime to stop.\n")

    word_items = list(words.items())
    random.shuffle(word_items)

    for english_word, swedish_word in word_items:
        answer = input(f"What is the Swedish word for '{english_word}'? ").strip().lower()
        
        if answer == "exit":
            break
        elif answer == swedish_word:
            print("Correct!\n")
            score += 1
        else:
            print(f"Incorrect. The correct answer is '{swedish_word}'.\n")
    
    print(f"Game over! Your score: {score}/{len(words)}")
    print("Thanks for playing and learning some Swedish!")

# Start the game
start_game()
