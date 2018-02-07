#!/usr/bin/python3

import json
import plac
import sys
import spacy
from pathlib import Path
import random

@plac.annotations(
    model=("Model name. Defaults to blank 'en' model.", "option", "m", str),
    new_model_name=("New model name for model meta.", "option", "nm", str),
    output_dir=("Optional output directory", "option", "o", Path),
    n_iter=("Number of training iterations", "option", "n", int),
    input_file=("Training data file location", "option","f",Path),
    use_gpu=("Use GPU for training", "flag","gpu"),)
def main(use_gpu, model=None, new_model_name='whistler', output_dir=None, n_iter=20, input_file=None):

    print(use_gpu)

    # Load the training data (json). TODO Valdate file format
    if input_file is None:
        sys.exit("You did not specify an input file.  There is nothing to train");
    else: 
        with open(input_file, 'r') as f:
            train_data = json.load(f)

    # Check if there is an output directory.  If not, don't run
    if output_dir is None:
        sys.exit("You did not specify an output directory.  If you train, your data will not be saved")        

    #Find or create a new model
    if model is not None:
        nlp = spacy.load(model) 
        print("Loaded model '%s'" % model)
    else:
        nlp = spacy.blank('en') 
        print("Created blank 'en' model")

    # Add entity recognizer to model if it's not in the pipeline
    # nlp.create_pipe works for built-ins that are registered with spaCy
    if 'ner' not in nlp.pipe_names:
        ner = nlp.create_pipe('ner')
        nlp.add_pipe(ner)
    # otherwise, get it, so we can add labels to it
    else:
        ner = nlp.get_pipe('ner')

    # Create the labels
    for label in train_data['labels']:
        print('Create Label: ' + label)
        ner.add_label(label)   

    # get names of other pipes to disable them during training
    other_pipes = [pipe for pipe in nlp.pipe_names if pipe != 'ner']
    with nlp.disable_pipes(*other_pipes): 
        print("Starting training")
        if use_gpu:
            optimizer = nlp.begin_training(device=0)
        else:
            optimizer = nlp.begin_training()
        for itn in range(n_iter):
            print("Starting iteration " + str(n_iter))
            random.shuffle(train_data['data'])
            losses = {}
            for text, annotations in train_data['data']:
                nlp.update([text], [annotations], sgd=optimizer, drop=0.35,
                           losses=losses)
            print(losses)

    # save model to output directory
    if output_dir is not None:
        output_dir = Path(output_dir)
        if not output_dir.exists():
            output_dir.mkdir()
        nlp.meta['name'] = new_model_name  # rename model
        nlp.to_disk(output_dir)
        print("Saved model to", output_dir)

if __name__ == '__main__':
    plac.call(main)
