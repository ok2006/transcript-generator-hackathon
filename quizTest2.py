

import spacy
import random


nlp = spacy.load("en_core_web_sm")

def generate_quiz(text, num_questions=3):
    """
    Generate quiz questions (Fill-in-the-Blank, True/False, MCQs) from text.
    """
    doc = nlp(text)
    sentences = [sent.text for sent in doc.sents if len(sent.text.split()) > 4]

    quizzes = []

    for sent in sentences[:num_questions]:
        ents = [ent.text for ent in nlp(sent).ents]  
        if not ents:
            continue
        keyword = ents[0]   

        # ---------- Fill-in-the-Blank ----------
        fb = sent.replace(keyword, "_____")
        quizzes.append({"type": "fill_blank", "q": fb, "a": keyword})

        # ---------- True/False ----------
        false_sent = sent.replace(keyword, "HTTP")  # simple replacement
        quizzes.append({"type": "true_false", "q": sent, "a": True})
        quizzes.append({"type": "true_false", "q": false_sent, "a": False})

        # ---------- MCQ ----------
        distractors = ["HTTP", "FTP", "UDP"]  # Simple distractor pool
        options = [keyword] + random.sample(distractors, 3)
        random.shuffle(options)
        quizzes.append({
            "type": "mcq",
            "q": sent.replace(keyword, "_____"),
            "options": options,
            "a": keyword
        })

    return quizzes



if __name__ == "__main__":
    text = """
    TCP/IP is the most widely used protocol suite.
    It has four layers: Application, Transport, Internet, and Network.
    """
    quiz = generate_quiz(text, num_questions=2)

    for q in quiz:
        print(q)
