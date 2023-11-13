from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter


cmd_list = [
    "available commands:",
    "hello - just say hello",
    "help - show available cmd",
    "add - add record or add additional phone - format 'name phone'",
    "bd_add - add birthday - format 'name date birthday (YYYY-MM-DD)'",
    "mail_add - add mail - format 'name nickname@domain.yy'",
    "mail_change - change mail - format 'name old mail new mail'",
    "location_add - add location/or replace if data already exist",
    "add_notes - ",
    "search_note - ",
    "show_bd_by_days - ",
    "days_to_bd - days to birthday - format 'name'",
    "change - change record - format 'name old phone new phone'",
    "delete - delete record - format 'name'",
    "phone - get phone by name - format 'phone name'",
    "show_all - show all phone book",
    "sort_folder - sort dirty folder by Audio, Docs, Archives, Music, Images, Other",
    "search - search by name or phone number",
    "goodbye/close/exit - shutdown this script",
]

completer = WordCompleter(cmd_list)
