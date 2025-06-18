from random import randint 

print("Let's play Rock, Paper, Scissors!")

#creating a list of play options

t = ["Rock", "Paper", "Scissors"]

while True:
    player = input("Rock, Paper, or Scissors?: ")
    
    if player not in t:
        print("Invalid input. Not cheating!")
        break
    computer = t[randint(0,2)]

    if player == computer:
        print("Tie!")
    elif player == "Rock":
        if computer == "Paper":
            print("You lose!", computer, "covers", player)
        else:
            print("You win!", player, "smashes", computer)
    elif player == "Paper":
        if computer == "Scissors":
            print("You lose!", computer, "cuts", player)
        else:
            print("You win!", player, "covers", computer)
    elif player == "Scissors":
        if computer == "Rock":
            print("You lose!", computer, "smashes", player)
        else:
            print("You win!", player, "cuts", computer)


               
