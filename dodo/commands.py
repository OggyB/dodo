from pathlib import Path

from dodo.checker import check_all_domains, load_tlds, _is_specific_domain, check_specific_domain
from dodo.exporter import export_csv, export_json, print_results
from pyfiglet import figlet_format
from termcolor import colored

def run_dodo_shell():
    tlds = load_tlds()
    last_results = []

    print(colored(figlet_format("dodo", font="slant"), "cyan"))
    print(colored("Minimal domain availability checker 🦤", "cyan"))
    print(colored("Type a domain name to check or type 'help' for commands.\n", "white"))

    try:
        while True:
            user_input = input("> ").strip()
            if not user_input:
                continue

            command_parts = user_input.split()
            command = command_parts[0].lower()
            args = command_parts[1:]

            result = handle_command(command, args, tlds, last_results)

            if result == "exit":
                print("👋 Goodbye!")
                break
            elif isinstance(result, list):
                last_results.clear()
                last_results.extend(result)
            elif isinstance(result, str):
                print(result)
            print()
    except KeyboardInterrupt:
        print("\n👋 Interrupted. Exiting...")


def handle_command(command, args, tlds, last_results):
    if command in ["quit",
                   "exit",
                   "/q",
                   "\q",
                   "exit()",
                   "quit()"
                   "/exit",
                   "/quit",
                   "/exit()",
                   "/quit()"]:
        return "exit"

    elif command == "help":
        return """🦤 Available commands:
- <domain>              Check availability across TLDs
- export csv <file>     Export last results as CSV
- export json <file>    Export last results as JSON
- help                  Show this help message
- quit                  Exit the program"""


    elif command == "export":

        if len(args) != 2 or args[0] not in ("csv", "json"):
            return "❌ Usage: export [csv|json] <filename>"

        if not last_results:
            return "⚠️ No previous results to export."

        try:

            content = export_csv(last_results) if args[0] == "csv" else export_json(last_results)

            desktop_path = Path.home() / "Desktop"

            output_file = desktop_path / args[1]

            with open(output_file, "w") as f:

                f.write(content)

            return f"💾 Results exported to Desktop as '{args[1]}'"

        except Exception as e:

            return f"❌ Failed to export: {str(e)}"

    elif _is_specific_domain(command):
        print(f"🔍 Checking specific domain '{command}'...\n")
        result, error = check_specific_domain(command)
        if result is None:
            result = f"❌ Error: {error}\n"
        else:
            status = "✅ Available" if result else "❌ Taken"
            result = f"{command}: {status}\n"
        return result

    elif command.isalnum():
        print(f"🔍 Checking availability for '{command}'...\n")
        results = check_all_domains(command, tlds)
        print_results(results)
        return results

    else:
        return f"❓ Unknown command: '{command}' (type 'help')"