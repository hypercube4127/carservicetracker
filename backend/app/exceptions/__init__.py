class AppError(Exception):
  def __init__(self, message):
    self.message = message
    super().__init__(self.message)

class ValidationError(AppError):
  pass

class DatabaseError(AppError):
  pass

class ObjectNotFoundError(AppError):
  pass

class PermissionDeniedError(AppError):
  pass