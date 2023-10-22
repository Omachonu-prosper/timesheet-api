import uuid

def generate_verification_string():
    """
    Generate the string that would be used to verify the user activation from their email
    """
    verifyer = uuid.uuid1()
    return str(verifyer)