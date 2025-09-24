# ---------- IMPORTS ----------
import spacy
import random
from transformers import pipeline

# ---------- SUMMARIZER ----------
summarizer = pipeline("summarization", model="google/pegasus-xsum")

def summarize_text(text, max_len=100, min_len=50):
    """
    Summarize the input text using PEGASUS.
    """
    summary = summarizer(text, max_length=max_len, min_length=min_len, do_sample=False)
    return summary[0]['summary_text']

# ---------- QUIZ GENERATOR ----------
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
        false_sent = sent.replace(keyword, "HTTP")  # naive replacement
        quizzes.append({"type": "true_false", "q": sent, "a": True})
        quizzes.append({"type": "true_false", "q": false_sent, "a": False})

        # ---------- MCQ ----------
        distractors = ["HTTP", "FTP", "UDP"]  # demo distractor pool
        options = [keyword] + random.sample(distractors, 3)
        random.shuffle(options)
        quizzes.append({
            "type": "mcq",
            "q": sent.replace(keyword, "_____"),
            "options": options,
            "a": keyword
        })

    return quizzes

# ---------- DEMO RUN ----------
if __name__ == "__main__":
    text = """
    Cleopatra VII Thea Philopator (69 BC – 30 BC) was Queen of the Ptolemaic Kingdom of Egypt 
    from 51 to 30 BC, and the last active Hellenistic pharaoh. She was a descendant of Ptolemy I Soter, 
    a general of Alexander the Great. Cleopatra initially co-ruled with her brother Ptolemy XIII but 
    their conflict led to civil war. After Julius Caesar intervened in Egypt, Cleopatra became co-ruler 
    with her younger brother Ptolemy XIV, and later her son Caesarion. Her reign ended when Egypt was 
    annexed by Rome after her death in 30 BC.
    """

    # Step 1: Summarize
    summary = summarize_text(text, max_len=80, min_len=40)
    print("===== SUMMARY =====")
    print(summary)

    # Step 2: Generate Quiz
    quiz = generate_quiz(summary, num_questions=2)

    print("\n===== QUIZ =====")
    for q in quiz:
        print(q)
