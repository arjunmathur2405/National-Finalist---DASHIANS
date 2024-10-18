import sys
import os

# Add the directory containing the modules to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from script.step1_handwritten_question_answer_to_text import recognize_handwritten_text_question, recognize_handwritten_text_answer
from script.step2_text_questio_answer_to_exel import txt_to_excel
# from models.step3_answer_generater_nlp_model import answer_generator
from models.step4_answer_sheet_evalution import answer_sheet_evaluation
from script.send_email import send_report
from script.save_history import save_history
from script.remove_temp import clean_directories,clean_files
from script.update_history_summary import update_history_summary
from script.interact_with_contract import interact_with_contract    

def main():
    # Converting Pdf to Txt using OCR
    recognize_handwritten_text_question()
    recognize_handwritten_text_answer()

    # Converting Txt to Excel
    txt_to_excel()

    # answer_generator()  # Useless as of Now 

    answer_sheet_evaluation()

    # interact_with_contract()

    # send_report()

    save_history()

    update_history_summary()


    clean_files()

    clean_directories()

    


if __name__ == "__main__":
    main()
