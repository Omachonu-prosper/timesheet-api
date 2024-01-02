from flask import jsonify

class ParsePayload:
    """
    Verify the payload of a request
    """
    
    def __init__(self, payload):
        self.payload = payload
        self.args = {}
        self.errors = {}
        self.valid = True
    
    def add_args(self, arg, required=False, help=None):
        """
        Add a needed entry to the arguements dictionary (Also verify the entry)
        """
        
        if required:
            if self.payload.get(arg) is None:
                self.errors[arg] = help
                self.valid = False
                return
        
        self.args[arg] = self.payload.get(arg)

    
    def get_args(self):
        """
        Get all needed payload entries
        """

        return self.args
    

    def generate_errors(self, message, status_code=400):
        """
        Generate errors for failed (or unverified) entries
        """

        return jsonify({
            'message': message,
            'status': False,
            'errors': self.errors
        }), status_code
   