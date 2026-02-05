from django.core.exceptions import ValidationError

def validate_image_size(value):
    filesize= value.size
    
    if filesize > 7340032:
        raise ValidationError("The maximum image size that can be uploaded is 7MB")
    else:
        return value

def validate_file_size(value):
    filesize= value.size
    
    if filesize > 10485760:
        raise ValidationError("The maximum file size that can be uploaded is 10MB")
    else:
        return value
        
