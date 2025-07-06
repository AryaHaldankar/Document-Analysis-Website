from django.shortcuts import render, HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Documents
from django import forms
import json
from PyPDF2 import PdfReader
import uuid
import os
import chromadb
from jinja2 import Template
from dotenv import load_dotenv
from google import genai

chroma_client = chromadb.PersistentClient(path = "/home/arya/Documents/Projects/Document-Analysis-Website/server/serverapp/uploads")

class fileForm(forms.Form):
    file = forms.FileField()

load_dotenv()
llm_api = os.getenv('GOOGLE_API_KEY')
llm_client = genai.Client(api_key = llm_api)

prompt_template = Template('''
Refer the following snippets taken from documents relevant to the user's query:\n
{{snips}}\n
User Query: {{query}}
''')

@api_view(['GET'])
def getDocumentList(request):
    uid = request.uid
    try:
        docs = Documents.objects.filter(user_id = uid) 
        list_docs = []
        for doc in docs:
            list_docs.append((doc.doc_name, doc.doc_id))
        return Response({'docs_list': list_docs})
    except Exception as e:
        return Response({'error': f'{e}'})

@api_view(['GET'])
def getLLMResponse(request):
    data = json.loads(request.body)
    doc_ids = data.get('docid')
    query = data.get('query')
    print(doc_ids)
    snips = ''
    try:
        for doc_id in doc_ids:
            doc = Documents.objects.get(doc_id = doc_id)
            coll_res = getPages(doc.collection_id)
            if coll_res == -1:
                raise Exception
            snips = snips + coll_res['documents'][0][0] +'\n'
        prompt = prompt_template.render(snips = snips, query = query)
        print(prompt)
        response = llm_client.models.generate_content(
            model = 'gemini-2.5-flash',
            contents = prompt
        )
        return Response({'llm_response': response.text})
    except Exception as e:
        return Response({'error': f'{e}'})

def getPages(coll_uid):
    try:
        collection = chroma_client.get_collection(name = coll_uid)
        results = collection.query(query_texts = [''], n_results = 1)
        return results
    except Exception as e:
        return -1

@api_view(['POST'])
def uploadDocument(request):
    uid = request.uid
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
                user_id = uid,
                doc_name = file.name,
                doc_id = doc_uid,
                collection_id = coll_uid
            )
            return Response({'status': 'File saved.', 'coll_uid': coll_uid, 'doc_uid': doc_uid})
        except Exception as e:
            return Response({'error': f'Error storing file. {e}'})
    else:
        return Response({'error': 'No file given'})