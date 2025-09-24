
from transformers import pipeline


summarizer = pipeline("summarization", model="google/pegasus-xsum")

text = """
CCleopatra VII Thea Philopator (Koine Greek: Κλεοπάτρα Θεά Φιλοπάτωρ, lit. 'Cleopatra father-loving goddess';[note 4] 70/69 BC – 10 or 12 August 30 BC) was Queen of the Ptolemaic Kingdom of Egypt from 51 to 30 BC, and the last active Hellenistic pharaoh.[note 5] A member of the Ptolemaic dynasty, she was a descendant of its founder Ptolemy I Soter, a Macedonian Greek general and companion of Alexander the Great.[note 6] Her first language was Koine Greek, and she is the only Ptolemaic ruler known to have learned the Egyptian language, among several others.[note 7] After her death, Egypt became a province of the Roman Empire, marking the end of the Hellenistic period in the Mediterranean, which had begun during the reign of Alexander (336–323 BC).[note 8]

Born in Alexandria, Cleopatra was the daughter of Ptolemy XII Auletes, who named her his heir before his death in 51 BC. Cleopatra began her reign alongside her brother Ptolemy XIII, but falling-out between them led to a civil war. Roman statesman Pompey fled to Egypt after losing the 48 BC Battle of Pharsalus against his rival Julius Caesar, the Roman dictator, in Caesar's civil war. Pompey had been a political ally of Ptolemy XII, but Ptolemy XIII had him ambushed and killed before Caesar arrived and occupied Alexandria. Caesar then attempted to reconcile the rival Ptolemaic siblings, but Ptolemy XIII's forces besieged Cleopatra and Caesar at the palace. Shortly after the siege was lifted by reinforcements, Ptolemy XIII died in the Battle of the Nile. Caesar declared Cleopatra and her brother Ptolemy XIV joint rulers, and maintained a private affair with Cleopatra which produced a son, Caesarion. Cleopatra traveled to Rome as a client queen in 46 and 44 BC, where she stayed at Caesar's villa. After Caesar's assassination, followed shortly afterwards by the sudden death of Ptolemy XIV (possibly murdered on Cleopatra's order), she named Caesarion co-ruler as Ptolemy XV.""
"""

summary = summarizer(text, max_length=100, min_length=50, do_sample=False)

print("Original:\n", text)
print("\nGenerated Summary:\n", summary[0]['summary_text'])