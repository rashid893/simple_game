from django.shortcuts import render

from django.shortcuts import render
import random

def hangman(request):
    if request.method == 'POST':
        guess = request.POST.get('guess', '').lower()
        if guess:
            if 'word' not in request.session:
                # Define the word list.
                words = ["python"]

                # Choose a random word.
                word = random.choice(words)

                # Initialize the game state.
                request.session['word'] = word
                request.session['guesses'] = []
                request.session['wrong_guesses'] = 0

            word = request.session['word']
            guesses = request.session['guesses']
            wrong_guesses = request.session['wrong_guesses']

            # Check if the guess has already been made.
            if guess not in guesses:
                # Check if the guess is correct.
                if guess in word:
                    guesses.append(guess)
                else:
                    wrong_guesses += 1

            # Print the current state of the game.
            guess_word = "".join([c if c in guesses else "-" for c in word])

            # Update the session data
            request.session['guesses'] = guesses
            request.session['wrong_guesses'] = wrong_guesses

            if guess_word == word:
                game_result = "You won!"
            elif wrong_guesses == 6:
                game_result = "You lost!"
            else:
                game_result = None

            return render(request, 'hangman.html', {'guess_word': guess_word, 'game_result': game_result})

    else:
        request.session.flush()  # Clear the session data on initial GET request

    return render(request, 'hangman.html')
