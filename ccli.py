import subprocess, os, sys, time



print("Welcome to CCLI\n\nWhat would you like to do today?\n")

print("[1]: Version control")

print("\nPick an option from the above list")
usrChoice = input("> ")

if usrChoice == "1":
    # VERSION CONTROL STUFF

    print("\n")
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Version Control")
    print("\n[1]: Stage files")
    print("[2]: Create a commit")
    print("[3]: Push an update")
    print("[4]: Branch")

    print("\nPick an option from the above list")
    usrChoice = input("> ")

    if usrChoice == "1":
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Stage Files\n")
        print("Type 'exit' to stop staging.")
        print("TIP: Type '.' to stage all files.\n\n")
        while True:
            print("Input the name of a file to stage it.")
            usrChoice = input("> ")
            if usrChoice != "exit":
                subprocess.run(["git","add",usrChoice])
            else:
                break
        print("Files staged successfully!")
        time.sleep(2)
        os.system('cls' if os.name == 'nt' else 'clear')
    elif usrChoice == "2":
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Create a commit")
        print("\nInput the commit message")
        usrChoice = input("> ")
        if usrChoice != "exit":
            subprocess.run(["git","commit","-m",usrChoice])
            exit(0)
    elif usrChoice == "3":
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Push to remote")
        print("\nAre you sure you would like to push? [y/n]")
        usrChoice = input("> ")
        if usrChoice.lower() != "y":
            exit(0)
        else:
            print("\nPushing!\n")
            subprocess.run(["git","push"])
            os.system('cls' if os.name == 'nt' else 'clear')
    elif usrChoice == "4":
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Branching")

        print("\n[1]: View available branches")
        print("[2]: Switch branches")
        print("[3]: Create a branch")
        print("[4]: Delete a branch")

        print("\nPick an option from the above list")
        usrChoice = input("> ")
        
        os.system('cls' if os.name == 'nt' else 'clear')

        if usrChoice == "1":
            print("Branches:\n")
            subprocess.run(["git","branch"])
            print("\n")
        elif usrChoice == "2":
            print("\nEnter the name of the branch")
            usrChoice = input("> ")
            subprocess.run(["git","switch", usrChoice])