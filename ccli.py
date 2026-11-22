import subprocess, os, sys, time, winreg

if os.name == "nt":
    folder = os.path.dirname(sys.executable)
    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment", 0, winreg.KEY_ALL_ACCESS) as k:
        path, _ = winreg.QueryValueEx(k, "Path")
        if folder.lower() not in path.lower():
            winreg.SetValueEx(k, "Path", 0, winreg.REG_EXPAND_SZ, path + ";" + folder)
            print("Welcome to CCLI!")
            print("Before you get started, we'll need you to restart your PC.")
            print("This is so our changes to PATH take effect!")
            print("Then, just run 'ccli' in a terminal")
            print("Happy coding!")

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
            print("TIP: Type '.' to stage all files.\n\n")
            print("Input the name of a file to stage it.")
            usrChoice = input("> ")
            subprocess.run(["git","add",usrChoice])
            input("\n\npress any key to continue...")
        elif usrChoice == "2":
            ClearTerminal()
            print("Create a commit")
            print("\nInput the commit message")
            usrChoice = input("> ")
            if usrChoice != "exit":
                subprocess.run(["git","commit","-m",usrChoice])
                input("\n\npress any key to continue...")
                
        elif usrChoice == "3":
            ClearTerminal()
            print("Push to remote")
            print("\nAre you sure you would like to push? [y/n]")
            usrChoice = input("> ")
            if usrChoice.lower() != "y":
                print(".")
            else:
                print("\nPushing!\n")
                subprocess.run(["git","push"])
                input("\n\npress any key to continue...")
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
                input("\n\npress any key to continue...")
            elif usrChoice == "2":
                print("\nEnter the name of the branch")
                usrChoice = input("> ")
                subprocess.run(["git","switch", usrChoice])
                input("\n\npress any key to continue...")
            elif usrChoice == "3":
                print("\nEnter the name of the branch")
                usrChoice = input("> ")
                subprocess.run(["git","checkout", "-b", usrChoice])
                input("\n\npress any key to continue...")
            elif usrChoice == "4":
                print("\nEnter the name of the branch")
                usrChoice = input("> ")

                print("Are you sure you would like to delete "+usrChoice+"? [y/n]")

                usrChoiceYesNo = input("> ")

                if usrChoiceYesNo.lower() != "y":
                    print(".")
                else:
                    subprocess.run(["git", "branch", "-d", usrChoice])
                    input("\n\npress any key to continue...")



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
            input("\n\npress any key to continue...")
        elif usrChoice == "2":
            ClearTerminal()
            print("\nEnter the name of the repo")
            usrChoice = input("> ")
            subprocess.run(["gh", "repo", "clone", usrChoice])
            input("\n\npress any key to continue...")
        elif usrChoice == "3":
            subprocess.run(["gh", "repo", "list"])
            input("\n\npress any key to continue...")

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
            input("\n\npress any key to continue...")
        elif usrChoice == "2":
            ClearTerminal()
            print("Winget")
            print("\n[1]: Search for a program")
            print("[2]: Install an application")
            print("[3]: Uninstall an application")

            print("\nPick an option from the above list")
            usrChoice = input("> ")

            operation = "search"

            if usrChoice == "2":
                operation = "install"
            elif usrChoice == "3":
                operation = "uninstall"

            print("\nEnter the name of the program")
            usrChoice = input("> ")

            subprocess.run(["winget", operation, usrChoice])

            input("\n\npress any key to continue...")
        elif usrChoice == "3":
            ClearTerminal()
            print("APT (Debian)")
            print("\nEnter the name of the Program")
            usrChoice = input("> ")
            subprocess.run(["sudo","apt", "install", usrChoice])
            input("\n\npress any key to continue...")
        elif usrChoice == "4":
            ClearTerminal()
            print("Pacman (Arch)")
            print("\nEnter the name of the Program")
            usrChoice = input("> ")
            subprocess.run(["sudo","pacman", "-Ss", usrChoice])
            input("\n\npress any key to continue...")
            



    elif usrChoice == "exit":
        break