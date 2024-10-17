"""
A tool to search for contacts and prepare messages on macOS.
"""

from .base import ToolSpec, ToolUse
import logging
import subprocess

logger = logging.getLogger(__name__)

def run_applescript(script):
    """Run an AppleScript and return the result."""
    process = subprocess.Popen(['osascript', '-e', script], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = process.communicate()
    if err:
        logger.error(f"AppleScript error: {err}")
    return out.decode().strip()

def search_contacts(contact_name):
    """Search for contacts with the given name."""
    script = f'''
    tell application "Contacts"
        set matchingContacts to (every person whose name contains "{contact_name}")
        set contactList to {{}}
        repeat with aContact in matchingContacts
            set thePhones to phones of aContact
            if (count of thePhones) > 0 then
                set thePhone to value of first item of thePhones
                set end of contactList to ((name of aContact) & " - " & thePhone)
            end if
        end repeat
        return contactList as list
    end tell
    '''
    return run_applescript(script).split(", ")

def prepare_message(phone_number, message):
    """Prepare a message in the Messages app without sending it."""
    script = f'''
    tell application "Messages"
        set targetService to 1st service whose service type = iMessage
        set targetBuddy to buddy "{phone_number}" of targetService
        set newMessage to make new outgoing message with properties {{buddy:targetBuddy, content:"{message}"}}
        activate
    end tell
    '''
    run_applescript(script)

def contact_and_message(contact_name, message):
    """Search for a contact and prepare a message."""
    print(f"Searching for contact '{contact_name}'...")
    contacts = search_contacts(contact_name)
    
    print(f"Found contact")
    
    if len(contacts) == 0:
        return f"No contacts found with the name '{contact_name}'."
    elif len(contacts) > 1:
        contact_list = "\n".join(contacts)
        return f"Multiple contacts found with the name '{contact_name}'. Please specify which one:\n{contact_list}"
    else:
        name, phone = contacts[0].split(" - ")
        print("preparing message")
        prepare_message(phone, message)
        print("Message prepared")
        return f"Message prepared for {name} ({phone}). Please check the Messages app to send it."

instructions = """
To use the contact tool, provide a contact name and a message. The tool will search for the contact in the macOS Contacts app and prepare a message in the Messages app.

If multiple contacts are found, you'll need to specify which one to use by running the function again with the full name and phone number.

Usage: contact_and_message("Contact Name", "Your message here")
""".strip()

examples = f"""
### Example usage of the contact tool
User: Can you text John Smith "Hey, are we still on for lunch tomorrow?"
Assistant: Certainly! I'll use the contact tool to prepare this message for John Smith.

{ToolUse("ipython", [], 'contact_and_message("John Smith", "Hey, are we still on for lunch tomorrow?")').to_output()}
System: Multiple contacts found with the name 'John Smith'. Please specify which one:
John Smith - +1 (123) 456-7890
John Smith - +1 (987) 654-3210
System: Message prepared for John Smith (+1 (123) 456-7890). Please check the Messages app to send it.
""".strip()

tool = ToolSpec(
    name="contact",
    desc="Search for contacts and prepare messages",
    instructions=instructions,
    examples=examples,
    functions=[contact_and_message],
    available=True,
)
__doc__ = tool.get_doc(__doc__)