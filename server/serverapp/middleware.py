import firebase_admin
from firebase_admin import credentials, auth
from django.http import JsonResponse

class FirebaseAuth:
    def __init__(self, get_response):
        self.get_response = get_response
        cred = credentials.Certificate("/home/arya/Documents/Projects/Document-Analysis-Website/server/serverapp/docanpr-890f4-firebase-adminsdk-fbsvc-e554b19dce.json")
        firebase_admin.initialize_app(cred)
    def __call__(self, request):
        try:
            token = request.META.get('HTTP_AUTHORIZATION')
            if token.startswith('Bearer '):
                token = token[7:]
            decoded_token = auth.verify_id_token(token)
            request.uid = decoded_token['uid']
            return self.get_response(request)
        except Exception as e:
            return JsonResponse({'error': f'{e}'})