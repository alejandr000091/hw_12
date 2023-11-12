from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter

cmd_list = ["hello", "help", "add", "mail_add", "mail_change", "bd_add", "location_add",
            "days_to_bd", "change", "delete", "phone", "show_all", "save_ab", "search", "load_ab", "good bye", "close", "exit"]

completer = WordCompleter(cmd_list)

while True:
    user_input = prompt("Enter command: ", completer=completer)
    if user_input.lower() in ("good bye", "close", "exit"):
        break

    print(f"You entered: {user_input}")