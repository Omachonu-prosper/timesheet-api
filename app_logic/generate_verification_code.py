import random
import string


def generate_verification_code():
    """
    Generate the code that would be used to verify the user activation from their email
    """
    # Define the character set from which you want to generate random characters
    character_set = string.ascii_letters + string.digits

    # Generate 3 random characters
    random_characters = ''.join(random.choice(character_set) for _ in range(5))

    return random_characters