import webbrowser
import pywhatkit as kit


# Map contact names (as you will say them) to phone numbers in international format
WHATSAPP_CONTACTS = {
    # Examples (replace with your real contacts):
    # "john": "+911234567890",
    # "mom": "+911234567890",
}


def open_whatsapp_web():
    """Open WhatsApp Web in the default browser."""
    webbrowser.open("https://web.whatsapp.com")


def handle_whatsapp_command(command: str, speak_callback):
    """
    Handle a command of the form:
    'send whatsapp to <name> message <your message here>'

    - command: full text command (already lowercased in Main.py)
    - speak_callback: function to speak back to user (e.g. ZenithAssistant.speak)
    """
    try:
        # Remove the leading phrase
        rest = command.replace("send whatsapp to", "", 1).strip()

        if " message " not in rest:
            speak_callback(
                "Please say the message after the word 'message'. For example, "
                "'send whatsapp to John message hello how are you'."
            )
            return

        name_part, message = rest.split(" message ", 1)
        contact_name = name_part.strip().lower()
        message = message.strip()

        if not contact_name or not message:
            speak_callback("Please provide both a contact name and a message.")
            return

        phone_number = WHATSAPP_CONTACTS.get(contact_name)
        if not phone_number:
            speak_callback(f"I don't have a WhatsApp number saved for {contact_name}.")
            return

        speak_callback(f"Sending your WhatsApp message to {contact_name}.")
        try:
            kit.sendwhatmsg_instantly(phone_number, message)
        except Exception:
            speak_callback("I couldn't send the WhatsApp message right now.")
    except Exception:
        speak_callback("Something went wrong while preparing your WhatsApp message.")

