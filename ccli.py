import subprocess, os, sys, time

def ClearTerminal():
    os.system('cls' if os.name == 'nt' else 'clear')

while True:
    ClearTerminal()
    print("Welcome to CCLI\n\nWhat would you like to do today?")
    print("TIP: type 'exit' to exit.")

    print("\n[1]: Version control")
    print("[2]: Github")
    print("[3]: Install Programs")

    print("\nPick an option from the above list")
    usrChoice = input("> ")

    if usrChoice == "1":
        # VERSION CONTROL STUFF

        print("\n")
        ClearTerminal()
        print("Version Control")
        print("\n[1]: Stage files")
        print("[2]: Create a commit")
        print("[3]: Push an update")
        print("[4]: Branch")

        print("\nPick an option from the above list")
        usrChoice = input("> ")

        if usrChoice == "1":
            ClearTerminal()
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
            ClearTerminal()
        elif usrChoice == "2":
            ClearTerminal()
            print("Create a commit")
            print("\nInput the commit message")
            usrChoice = input("> ")
            if usrChoice != "exit":
                subprocess.run(["git","commit","-m",usrChoice])
                exit(0)
        elif usrChoice == "3":
            ClearTerminal()
            print("Push to remote")
            print("\nAre you sure you would like to push? [y/n]")
            usrChoice = input("> ")
            if usrChoice.lower() != "y":
                exit(0)
            else:
                print("\nPushing!\n")
                subprocess.run(["git","push"])
                ClearTerminal()
        elif usrChoice == "4":
            ClearTerminal()
            print("Branching")

            print("\n[1]: View available branches")
            print("[2]: Switch branches")
            print("[3]: Create a branch")
            print("[4]: Delete a branch")

            print("\nPick an option from the above list")
            usrChoice = input("> ")
            
            ClearTerminal()

            if usrChoice == "1":
                print("Branches:\n")
                subprocess.run(["git","branch"])
                print("\n")
            elif usrChoice == "2":
                print("\nEnter the name of the branch")
                usrChoice = input("> ")
                subprocess.run(["git","switch", usrChoice])
            elif usrChoice == "3":
                print("\nEnter the name of the branch")
                usrChoice = input("> ")
                subprocess.run(["git","checkout", "-b", usrChoice])
            elif usrChoice == "4":
                print("\nEnter the name of the branch")
                usrChoice = input("> ")

                print("Are you sure you would like to delete "+usrChoice+"? [y/n]")

                usrChoiceYesNo = input("> ")

                if usrChoiceYesNo.lower() != "y":
                    exit(0)
                else:
                    subprocess.run(["git", "branch", "-d", usrChoice])



    elif usrChoice == "2":
        # GITHUB CONTROL STUFF

        print("\n")
        ClearTerminal()
        print("Github")
        print("\n[1]: Create a new repo")
        print("[2]: Clone a repo")
        print("[3]: List repos")

        print("\nPick an option from the above list")
        usrChoice = input("> ")
        if usrChoice == "1":
            ClearTerminal()
            subprocess.run(["gh", "repo", "create"])
        elif usrChoice == "2":
            ClearTerminal()
            print("\nEnter the name of the repo")
            usrChoice = input("> ")
            subprocess.run(["gh", "repo", "clone", usrChoice])
        elif usrChoice == "3":
            subprocess.run(["gh", "repo", "list"])

    elif usrChoice == "3":
        ClearTerminal()
        print("Install Programs")
        print("\n[1]: pip")
        print("[2]: winget")
        print("[3]: apt")
        print("[4]: pacman")
        
        print("\nPick an option from the above list")
        usrChoice = input("> ")
        if usrChoice == "1":
            ClearTerminal()
            print("Pip")
            print("\nEnter the name of the Program")
            usrChoice = input("> ")
            subprocess.run(["python","-m", "pip", "install", usrChoice])


    elif usrChoice == "exit":
        break