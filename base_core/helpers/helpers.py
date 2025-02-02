from django.contrib.auth import get_user_model

def get_object_or_none(class_model,**kwargs):
    try:
        return class_model.objects.get(**kwargs)
    except class_model.DoesNotExist:
        return None
    

def get_token_user_or_none(request):
    User = get_user_model()
    try:
        instance = User.objects.get(id=request.user.id)
    except Exception:
        instance = None
    finally:
        return instance
