from django.shortcuts import render, HttpResponse
from .models import Session
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Documents, Users
from firebase_admin import auth
from PyPDF2 import PdfReader
import uuid
import chromadb

import firebase_admin
from firebase_admin import credentials

cred = credentials.Certificate("docanpr-890f4-firebase-adminsdk-fbsvc-e554b19dce.json")
firebase_admin.initialize_app(cred)
chroma_client = chromadb.Client()

@api_view(['POST'])
def uploadDocument(request):
    id_token = request.headers.get("Authorization")
    if not id_token:
        return Response({'error': 'No login key provided.'})
    if id_token.startswith('Bearer '):
        id_token = id_token[7:]
    try:
        decoded_token = auth.verify_id_token(id_token)
        uid = decoded_token['uid']
    except Exception as e:
        return Response({'error': 'Unable to verify identification'})
    file = request.files['file']
    if file:
        reader = PdfReader(file)
        text = ''
        for page in reader.pages:
            text += page.extract_text()
        coll_uid = str(uuid.uuid4())
        doc_uid = str(uuid.uuid4())
        collection = chroma_client.create_collection(name=coll_uid)
        while i < len(text):
            collection.add(ids = [i], documents = [text[i: min(i+1000, len(text))]])
            i += 800
        file.save(f'uploads/{doc_uid}.pdf')
        document = Documents.objects.create(
            user_id = uid,
            doc_id = doc_uid,
            collection_id = coll_uid
        )
    else:
        return Response({'error': 'No file given'})