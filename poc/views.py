from django.shortcuts import render

import os
import spacy
from spacy import displacy

from .models import SpacyModel

# Create your views here.
def index(request):
    modelList = SpacyModel.objects.all();
    return render(request,'poc/index.html', {'modelList' : modelList})

def displayResults(request):
    nlp = spacy.load(os.environ['MODEL_LOCATION'] + request.POST.get('model',''))
    doc = nlp(request.POST.get('text', ''))
    html = displacy.render(doc, style="ent")
    return render(request, 'poc/displayResults.html', {'request' : request, 'doc': doc, 'html' : html})