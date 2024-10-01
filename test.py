import re

def get_message_size(message):
    return str(message.split()[2])

message_size = get_message_size("m 10 100")

pattern = fr"^m\s([1-9]|10)\s{message_size}\n$"

test_string = f"m 10 100\n"

if re.match(pattern, test_string):
    print(f"'{test_string.strip()}' is valid")
else:
    print(f"'{test_string.strip()}' is invalid")