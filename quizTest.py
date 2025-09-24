import spacy
nlp = spacy.load("en_core_web_sm")

def extract_keywords(text):
    doc = nlp(text)
    entities = [ent.text for ent in doc.ents]
    noun_chunks = [chunk.text for chunk in doc.noun_chunks if len(chunk.text.split()) > 1]
    return list(set(entities + noun_chunks))


sentence = "BART is a sequence-to-sequence model that combines the pretraining objectives from BERT and GPT. It’s pretrained by corrupting text in different ways like deleting words, shuffling sentences, or masking tokens and learning how to fix it. The encoder encodes the corrupted document and the corrupted text is fixed by the decoder. As it learns to recover the original text, BART gets really good at both understanding and generating language."
keywords = extract_keywords(sentence)
print("Keywords:", keywords)
