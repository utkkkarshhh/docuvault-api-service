class ResponseMessages:
    HEALTHY_SERVICE = "API Service is healthy and running."
    USER_CREATED_SUCCESSFULLY = "User has been registered successfully"
    SIGN_IN_SUCCESSFUL = "Login successful"
    USER_DETAILS_FETCHED = "User details fetched successfully"
    USER_DETAILS_UPDATED = "User details updated successfully"
    PASSWORD_UPDATED_SUCCESSFULLY = "Password updated successfully"
    PASSWORD_NOT_UPDATED = "Password not updated. Please try again later"
    USER_DELETED_SUCCESSFULLY = "User deleted successfully"

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
    USERNAME_ALREADY_TAKEN = "This username is already taken"
    EMAIL_ALREADY_EXISTS = "Email already exists"
    EMAIL_ALREADY_REGISTERED = "This email is already registered with another account"
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
    NEW_AND_CONFIRM_PASS_NOT_MATCH = "New password and confirm password do not match"
    NEW_PASS_CANT_BE_EXISTING = "New password can't be your existing password"
    ERROR_WHILE_DELETING = "Error While deleting user : {}"
    ACCOUNT_WAS_DELETED = "Your account was deleted. Please reach out at utkarshbhardwajmail@gmail.com"
    UPLOAD_LIMIT_EXCEEDED = "Upload limit has been exceeded"
