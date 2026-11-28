"""CCLI - a small menu-driven helper for git, GitHub and installing programs.

Run it with `ccli` (after the first-run PATH setup) from any terminal.
Every menu has a [0] Back option, and leaving a prompt blank cancels it.
Type 'exit' at any prompt, or press Ctrl+C, to leave CCLI.
"""

import os
import shlex
import shutil
import subprocess
import sys

IS_WINDOWS = os.name == "nt"

BACK_WORDS = ("0", "b", "back")  # all of these pick the Back option in a menu
BLANK_HINT = "(leave blank to go back)"


class ExitCCLI(Exception):
    """Raised from anywhere to leave CCLI cleanly (no traceback)."""


# =============================================================================
# First-run setup
# =============================================================================

def ensure_on_path():
    """Add this Python's folder to the user's PATH so `ccli` works anywhere.

    Windows only. If PATH was changed, tell the user to restart and exit,
    because the new PATH doesn't apply to already-open terminals.
    """
    if not IS_WINDOWS:
        return

    import winreg  # Windows-only module, so imported here instead of at the top

    folder = os.path.dirname(sys.executable)

    def normalise(path):
        """Make paths comparable: expand %VARS%, fix slashes, ignore case."""
        return os.path.normcase(os.path.normpath(os.path.expandvars(path)))

    try:
        access = winreg.KEY_READ | winreg.KEY_WRITE
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment", 0, access) as key:
            try:
                current_path, _ = winreg.QueryValueEx(key, "Path")
            except FileNotFoundError:
                current_path = ""  # the user has no PATH variable yet

            entries = [normalise(p) for p in current_path.split(";") if p.strip()]
            if normalise(folder) in entries:
                return  # already set up, nothing to do

            new_path = current_path.rstrip(";") + ";" + folder if current_path else folder
            winreg.SetValueEx(key, "Path", 0, winreg.REG_EXPAND_SZ, new_path)

    except OSError as error:
        print(f"Couldn't update PATH automatically: {error}")
        input("\npress Enter to continue...")
        return

    print("Welcome to CCLI!")
    print("Before you get started, we'll need you to restart your PC.")
    print("This is so our changes to PATH take effect!")
    print("Then, just run 'ccli' in a terminal")
    print("Happy coding!")
    raise ExitCCLI


# =============================================================================
# Small helpers used everywhere
# =============================================================================

def clear():
    """Clear the terminal."""
    os.system("cls" if IS_WINDOWS else "clear")


def ask(prompt="> "):
    """Read a line of input.

    Ctrl+C, Ctrl+Z (EOF) and typing 'exit' all leave CCLI cleanly.
    """
    try:
        answer = input(prompt).strip()
    except (KeyboardInterrupt, EOFError):
        raise ExitCCLI
    if answer.lower() == "exit":
        raise ExitCCLI
    return answer


def pause():
    """Wait for Enter so the user can read output before the screen clears."""
    try:
        input("\n\npress Enter to continue...")
    except (KeyboardInterrupt, EOFError):
        raise ExitCCLI


def run(command, capture=False):
    """Run an external command.

    Returns the CompletedProcess, or None if the program isn't installed
    (instead of crashing with FileNotFoundError).
    """
    try:
        return subprocess.run(command, capture_output=capture, text=capture)
    except FileNotFoundError:
        print(f"'{command[0]}' was not found. Is it installed and on your PATH?")
        return None


def succeeded(result):
    """True if a command from run() actually ran and exited successfully."""
    return result is not None and result.returncode == 0


def confirm(question):
    """Ask a yes/no question. Anything other than 'y' counts as no."""
    print(f"\n{question} [y/n]")
    return ask().lower() == "y"


def is_git_repo():
    """True if git is installed and the current folder is inside a repository."""
    if not shutil.which("git"):
        return False
    result = subprocess.run(
        ["git", "rev-parse", "--is-inside-work-tree"],
        capture_output=True, text=True,
    )
    return result.returncode == 0


def current_branch():
    """Name of the checked-out branch, or '' if it can't be worked out."""
    result = run(["git", "branch", "--show-current"], capture=True)
    return result.stdout.strip() if result else ""


def show_menu(title, options, tip=None, back_label="Back"):
    """Display a numbered menu until the user picks something valid.

    `options` maps keys to labels, e.g. {"1": "Stage files"}.
    Returns the chosen key, or None if the user picked Back ([0]).
    A mistyped choice just shows a message and asks again.
    """
    error = ""
    while True:
        clear()
        print(title)
        if tip:
            print(tip)
        print()

        for key, label in options.items():
            print(f"[{key}]: {label}")
        print(f"[0]: {back_label}")

        if error:
            print(f"\n{error}")
        print("\nPick an option from the above list")
        choice = ask()

        if choice.lower() in BACK_WORDS:
            return None
        if choice in options:
            return choice
        error = "That's not a valid option, try again."


# =============================================================================
# [1] Version control
# =============================================================================

def version_control_menu():
    """Entry point for git actions. Needs git and a repository."""
    if not shutil.which("git"):
        print("Git isn't installed (or isn't on your PATH).")
        pause()
        return

    if not is_git_repo():
        clear()
        print("This folder is not a git repository.")
        print(f"\n  {os.getcwd()}")
        print("\nRun 'git init' here, or cd into a repository and start CCLI again.")
        pause()
        raise ExitCCLI

    while True:
        choice = show_menu("Version Control", {
            "1": "Stage files",
            "2": "Create a commit",
            "3": "Push an update",
            "4": "Branch",
        })

        if choice is None:
            return
        elif choice == "1":
            stage_files()
        elif choice == "2":
            create_commit()
        elif choice == "3":
            push_to_remote()
        elif choice == "4":
            branch_menu()


def stage_files():
    """`git add` one or more files, then offer to commit them straight away."""
    clear()
    print("Stage Files\n")
    run(["git", "status", "--short"])  # show what's changed to help the user pick

    print("\nTIP: Type '.' to stage all files. Separate several files with spaces.")
    print(f"\nInput the name(s) of the file(s) to stage {BLANK_HINT}")
    names = ask()

    if not names:
        return

    try:
        files = shlex.split(names, posix=not IS_WINDOWS)  # handles "quoted names"
    except ValueError as error:
        print(f"Couldn't read that input: {error}")
        pause()
        return

    if not succeeded(run(["git", "add", *files])):
        pause()
        return

    print("\nStaged. Current status:\n")
    run(["git", "status", "--short"])

    if confirm("Create a commit now?"):
        create_commit()
    else:
        pause()


def create_commit():
    """`git commit` with a message, then offer to push it straight away."""
    clear()
    print("Create a commit")

    staged = run(["git", "diff", "--cached", "--name-only"], capture=True)
    if staged and not staged.stdout.strip():
        print("\nNothing is staged. Stage some files first.")
        pause()
        return

    print(f"\nInput the commit message {BLANK_HINT}")
    message = ask()

    if not message:
        return

    if succeeded(run(["git", "commit", "-m", message])) and confirm("Push this commit now?"):
        push_to_remote(ask_first=False)  # they just said yes, so don't ask again
    else:
        pause()


def push_to_remote(ask_first=True):
    """`git push`, setting the upstream automatically on a branch's first push."""
    clear()
    print("Push to remote")

    branch = current_branch()
    if ask_first:
        target = f"'{branch}'" if branch else "your changes"
        if not confirm(f"Are you sure you would like to push {target}?"):
            return

    print("\nPushing!\n")

    # A brand-new branch has no upstream, and a plain `git push` would fail.
    upstream = run(
        ["git", "rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}"],
        capture=True,
    )

    if not succeeded(upstream) and branch:
        print(f"No upstream set for '{branch}', pushing with -u origin.\n")
        run(["git", "push", "-u", "origin", branch])
    else:
        run(["git", "push"])
    pause()


def branch_menu():
    """List, switch, create or delete branches."""
    while True:
        choice = show_menu("Branching", {
            "1": "View available branches",
            "2": "Switch branches",
            "3": "Create a branch",
            "4": "Delete a branch",
        })

        if choice is None:
            return

        clear()

        if choice == "1":
            print("Branches:\n")
            run(["git", "branch"])
            pause()
            continue

        # For switching and deleting, show the existing branches so the user
        # doesn't have to remember the exact name.
        if choice in ("2", "4"):
            print("Branches:\n")
            run(["git", "branch"])
            print()

        print(f"Enter the name of the branch {BLANK_HINT}")
        name = ask()
        if not name:
            continue

        if choice == "2":
            run(["git", "switch", name])
        elif choice == "3":
            run(["git", "switch", "-c", name])
        elif choice == "4":
            delete_branch(name)
        pause()


def delete_branch(name):
    """Delete a branch safely, offering a force delete only if git refuses."""
    if not confirm(f"Are you sure you would like to delete {name}?"):
        return

    result = run(["git", "branch", "-d", name], capture=True)
    if result is None:
        return

    print(result.stdout + result.stderr)

    # `-d` refuses to delete a branch with unmerged commits. Explain, then let
    # the user decide instead of leaving them at a dead end.
    if result.returncode != 0 and "not fully merged" in result.stderr:
        print("This branch has commits that haven't been merged. Force deleting")
        print("will permanently lose them.")
        if confirm(f"Force delete {name}?"):
            run(["git", "branch", "-D", name])


# =============================================================================
# [2] GitHub
# =============================================================================

def github_menu():
    """Create, clone and list repos using the GitHub CLI (`gh`)."""
    if not shutil.which("gh"):
        print("The GitHub CLI ('gh') isn't installed (or isn't on your PATH).")
        print("Get it from https://cli.github.com or run: winget install GitHub.cli")
        pause()
        return

    while True:
        choice = show_menu("Github", {
            "1": "Create a new repo",
            "2": "Clone a repo",
            "3": "List repos",
        })

        if choice is None:
            return

        clear()

        if choice == "1":
            run(["gh", "repo", "create"])  # gh walks the user through its own prompts
            pause()
        elif choice == "2":
            clone_repo()
        elif choice == "3":
            run(["gh", "repo", "list"])
            pause()


def clone_repo():
    """Clone a repo, with a hint if the name looks wrong."""
    print(f"Enter the name of the repo (e.g. owner/repo) {BLANK_HINT}")
    name = ask()

    if not name:
        return

    if "/" not in name and "://" not in name:
        print("\nThat doesn't look like owner/repo, so gh will assume it's one of")
        print("your own repositories.")

    run(["gh", "repo", "clone", name])
    pause()


# =============================================================================
# [3] Install programs
# =============================================================================

def install_menu():
    """Install programs with whichever package managers suit this system."""
    options = {"1": "pip"}
    if IS_WINDOWS:
        options["2"] = "winget"
    else:
        if shutil.which("apt"):
            options["3"] = "apt"
        if shutil.which("pacman"):
            options["4"] = "pacman"

    while True:
        choice = show_menu("Install Programs", options)

        if choice is None:
            return
        elif choice == "1":
            install_with_pip()
        elif choice == "2":
            use_winget()
        elif choice == "3":
            install_with_apt()
        elif choice == "4":
            install_with_pacman()


def prompt_for_name(title, label="program"):
    """Show a title and ask for a name. Returns '' if the user left it blank."""
    clear()
    print(f"{title}\n\nEnter the name of the {label} {BLANK_HINT}")
    return ask()


def install_with_pip():
    name = prompt_for_name("Pip", label="package")
    if name:
        # sys.executable makes sure we install into the Python running CCLI
        run([sys.executable, "-m", "pip", "install", name])
        pause()


def winget_install(name):
    """Install with winget. Treats 'Publisher.App' style names as exact IDs."""
    looks_like_id = "." in name and " " not in name
    if looks_like_id:
        run(["winget", "install", "--id", name, "--exact"])
    else:
        run(["winget", "install", name])


def use_winget():
    while True:
        choice = show_menu("Winget", {
            "1": "Search for a program",
            "2": "Install an application",
            "3": "Uninstall an application",
        })
        if choice is None:
            return

        print(f"\nEnter the name of the program {BLANK_HINT}")
        name = ask()
        if not name:
            continue

        if choice == "1":
            run(["winget", "search", name])

            # Searching is usually the first step to installing, so offer it now.
            if confirm("Install one of these now?"):
                print(f"\nEnter the name or ID of the program to install {BLANK_HINT}")
                print("TIP: the ID (e.g. Mozilla.Firefox) is the most precise.")
                picked = ask()
                if picked:
                    winget_install(picked)
        elif choice == "2":
            winget_install(name)
        elif choice == "3":
            run(["winget", "uninstall", name])

        pause()


def install_with_apt():
    name = prompt_for_name("APT (Debian)")
    if name:
        run(["sudo", "apt", "install", name])
        pause()


def install_with_pacman():
    name = prompt_for_name("Pacman (Arch)")
    if name:
        run(["sudo", "pacman", "-S", name])
        pause()


# =============================================================================
# Main loop
# =============================================================================

def main():
    ensure_on_path()

    while True:
        choice = show_menu(
            "Welcome to CCLI\n\nWhat would you like to do today?",
            {
                "1": "Version control",
                "2": "Github",
                "3": "Install Programs",
            },
            tip="TIP: type 'exit' (or press Ctrl+C) to exit.",
            back_label="Exit",
        )

        if choice is None:  # [0] on the main menu means leave CCLI
            raise ExitCCLI
        elif choice == "1":
            version_control_menu()
        elif choice == "2":
            github_menu()
        elif choice == "3":
            install_menu()


if __name__ == "__main__":
    try:
        main()
    except (ExitCCLI, KeyboardInterrupt):
        pass
    print("\nExiting CCLI...")
