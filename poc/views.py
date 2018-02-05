from django.shortcuts import render

import os
import spacy
from spacy import displacy

# Create your views here.
def index(request):
    nlp = spacy.load(os.environ['MODEL_LOCATION'] + "anatomy")
    doc = nlp(u'STUDY:   X-RAY CHEST  REASON FOR EXAM:   Male, 56 years old.  Cough  TECHNIQUE:   PA and lateral views of the chest.  COMPARISON:   None. ___________________________________  FINDINGS:  The lungs are clear and expanded.  Mild blunting of the posterior costophrenic angles.  This is most likely the right costophrenic angle suggesting mild effusion or pleural thickening.  Normal size heart.   Normal mediastinum and hila.  Normal visualized pulmonary arteries.  Normal visualized aortic arch and descending thoracic aorta.  Normal visualized thoracic spine.  Normal visualized ribs, clavicles, and shoulders.  There is no demonstrated abnormality of the visualized soft tissue structures of the upper abdomen. ___________________________________  IMPRESSION:  Mild blunting of one of the posterior costophrenic angles.  This is most likely the right costophrenic angle suggesting mild effusion or pleural thickening.  Lungs are essentially clear.  No prior studies available for my review')

    options = {'compact': True, 'distance': 105}
    html = displacy.render(doc, style="ent")

    return render(request, 'poc/index.html', {'request' : request, 'doc': doc, 'html' : html})