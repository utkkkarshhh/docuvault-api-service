class ResponseMessages:
    HEALTHY_SERVICE = "API Service is healthy and running."
    USER_CREATED_SUCCESSFULLY = "User has been registered successfully"
    SIGN_IN_SUCCESSFUL = "Login successful"
    USER_DETAILS_FETCHED = "User details fetched successfully"

class HTTPResponseMessages:
    HTTP_REQUEST_ERROR = "Error while making HTTP request"
    STATUS_CODE_ERROR = "Unexpected status code received"
    AUTHENTICATION_ERROR = "Authentication failed. Please check your credentials"
    INVALID_METHOD = "Invalid HTTP method used for this endpoint."
    UNSUPPORTED_DATA = "Unsupported media type"
    UNACCEPTABLE_DATA = "Unacceptable data"

class ExceptionMessages:
    DATA_NOT_AVAILABLE = "Data not available"
    DOES_NOT_EXIST = "Resource does not exist"
    SOMETHING_WENT_WRONG = "Something went wrong"
    ERROR_WHILE_CREATING_USER = "An error occured while creating user"
    USERNAME_ALREADY_EXISTS = "Username already exists"
    EMAIL_ALREADY_EXISTS = "Email already exists"
    PASSWORD_LENGTH_INVALID = "Password must be at least 8 characters long"
    INVALID_REGISTRATION_TOKEN = "Invalid registration token"
    INCORRECT_USERNAME_OR_EMAIL = "Incorrect Username or Email"
    INCORRECT_PASSWORD = 'Incorrect password'
    AUTH_CREDENTIALS_INVALID = 'Authentication credentials were not provided or invalid'
    TOKEN_EXPIRED = 'Token has expired'
    TOKEN_INVALID = 'Token invalid'
    USER_DOES_NOT_EXIST = "User does not exist"
    TOKEN_NOT_ACTIVE_INVALID = "Token is not active or invalid"
    NO_TOKEN_DATA = "No token data found in request object"
    USER_NOT_FOUND = "User not found"
    