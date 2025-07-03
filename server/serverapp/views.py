from django.shortcuts import render, HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Documents
from django import forms
from firebase_admin import auth
from PyPDF2 import PdfReader
import uuid
import chromadb

import firebase_admin
from firebase_admin import credentials

cred = credentials.Certificate("/home/arya/Documents/Projects/Document-Analysis-Website/server/serverapp/docanpr-890f4-firebase-adminsdk-fbsvc-e554b19dce.json")
firebase_admin.initialize_app(cred)
chroma_client = chromadb.PersistentClient(path = "/home/arya/Documents/Projects/Document-Analysis-Website/server/serverapp/uploads")

class fileForm(forms.Form):
    file = forms.FileField()

@api_view(['GET'])#to test
def getDocument(request):
    coll_uid = request.data.get('coll_uid')
    try:
        collection = chroma_client.get_collection(name = coll_uid)
        results = collection.query(query_texts = [''], n_results = 5)
        return Response({'pages': results})
    except Exception as e:
        return Response({'error': f'{e}'})

@api_view(['POST'])
def uploadDocument(request):
    print(request.FILES)
    form = fileForm(request.POST, request.FILES)
    if form.is_valid():
        try:
            file = request.FILES['file']
            reader = PdfReader(file)
            text = ''
            for page in reader.pages:
                text += page.extract_text()
            coll_uid = str(uuid.uuid4())
            doc_uid = str(uuid.uuid4())
            collection = chroma_client.create_collection(name=coll_uid)
            i = 0
            while i < len(text):
                collection.add(ids = [str(i)], documents = [text[i: min(i+1000, len(text))]])
                i += 800
            file_path = f'/home/arya/Documents/Projects/Document-Analysis-Website/server/serverapp/uploads/{doc_uid}.pdf'
            with open(file_path, 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)
            _ = Documents.objects.create(
                doc_id = doc_uid,
                collection_id = coll_uid
            )
            return Response({'status': 'File saved.', 'coll_uid': coll_uid, 'doc_uid': doc_uid})
        except Exception as e:
            return Response({'error': f'Error storing file. {e}'})
    else:
        return Response({'error': 'No file given'})