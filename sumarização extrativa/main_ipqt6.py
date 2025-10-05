import sys
import os
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
    QPushButton, QFileDialog, QTextEdit, QLabel, QFrame,
    QMessageBox 
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from utils.pdf_reader import pdf_reader
from utils.tokenizer import tokenizer_spacy
from sumarizacao.sumarizador import pontuador_de_lemmas, puntuador_de_sentencas, extração_das_melhores_sentencas

def run_sumarization_pipeline(file_path):
    print('Iniciando o processo de sumarização extrativa...')
    doc_text = pdf_reader(file_path)
    tokens = tokenizer_spacy(doc_text)
    dict_lemmas_pontuados = pontuador_de_lemmas(tokens)
    dict_sentencas_pontuados = puntuador_de_sentencas(tokens, dict_lemmas_pontuados)
    string_final = extração_das_melhores_sentencas(tokens, dict_sentencas_pontuados)
    
    return doc_text, string_final

class SumarizacaoWorker(QThread):
    finished = pyqtSignal(str, str) 
    error = pyqtSignal(str)         

    def __init__(self, file_path):
        super().__init__()
        self.file_path = file_path

    def run(self):
        try:
            doc_text, string_final = run_sumarization_pipeline(self.file_path)
            self.finished.emit(doc_text, string_final)
        except Exception as e:
            self.error.emit(f"Erro no pipeline de sumarização: {e}")
class SumarizadorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sumarizador Extrativo com spaCy")
        self.setGeometry(100, 100, 1000, 700)
        self.setStyleSheet(self._get_stylesheet())
        self.current_file_path = ""
        self.worker = None 
        self.setup_ui()

    def _get_stylesheet(self):
        return """
            QWidget {
                background-color: #f0f4f8; 
                color: #333333;
            }
            QLabel {
                font-size: 14px;
                font-weight: bold;
                color: #2c3e50;
                margin-top: 10px;
            }
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QTextEdit {
                background-color: white;
                border: 1px solid #bdc3c7;
                border-radius: 4px;
                padding: 5px;
            }
            QFrame#Separator {
                background-color: #bdc3c7;
            }
        """

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        control_layout = QHBoxLayout()
        
        self.select_button = QPushButton("1. Selecionar Arquivo PDF")
        self.select_button.clicked.connect(self.select_file)
        control_layout.addWidget(self.select_button)

        self.file_label = QLabel("Nenhum arquivo selecionado.")
        self.file_label.setFont(QFont("Arial", 10))
        control_layout.addWidget(self.file_label)
        
        self.start_button = QPushButton("2. INICIAR SUMARIZAÇÃO")
        self.start_button.clicked.connect(self.start_sumarization)
        self.start_button.setEnabled(False)
        control_layout.addWidget(self.start_button)
        
        main_layout.addLayout(control_layout)

        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        separator.setObjectName("Separator")
        main_layout.addWidget(separator)

        display_layout = QHBoxLayout()
        
        raw_text_layout = QVBoxLayout()
        raw_text_layout.addWidget(QLabel("Texto Bruto do Arquivo:"))
        self.raw_text_editor = QTextEdit()
        self.raw_text_editor.setReadOnly(True)
        raw_text_layout.addWidget(self.raw_text_editor)
        display_layout.addLayout(raw_text_layout)
        
        summary_layout = QVBoxLayout()
        summary_layout.addWidget(QLabel("Resumo Extrativo:"))
        self.summary_text_editor = QTextEdit()
        self.summary_text_editor.setReadOnly(True)
        summary_layout.addWidget(self.summary_text_editor)
        display_layout.addLayout(summary_layout)
        
        main_layout.addLayout(display_layout)
        
    def select_file(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self, 
            "Selecionar Arquivo PDF", 
            "", 
            "Arquivos PDF (*.pdf)"
        )
        
        if file_name:
            self.current_file_path = file_name
            base_name = os.path.basename(file_name)
            self.file_label.setText(f"Arquivo Selecionado: <b>{base_name}</b>")
            self.raw_text_editor.clear()
            self.summary_text_editor.clear()
            self.start_button.setEnabled(True)
                
    def handle_results(self, doc_text, string_final):
        self.raw_text_editor.setText(doc_text)
        self.summary_text_editor.setText(string_final)
        self.start_button.setEnabled(True)
        
    def handle_error(self, message):
        QMessageBox.critical(self, "Erro de Processamento", message)
        self.raw_text_editor.setText(f"Processamento falhou. Verifique os logs.")
        self.summary_text_editor.clear()
        self.start_button.setEnabled(True)
                
    def start_sumarization(self):
        if not self.current_file_path:
            QMessageBox.warning(self, "Arquivo Ausente", "Por favor, selecione um arquivo PDF.")
            return

        self.summary_text_editor.setText("Processando... Aguarde. O pipeline de sumarização (incluindo spaCy) está em execução.")
        self.start_button.setEnabled(False)
        self.raw_text_editor.setText("Lendo e processando texto...")

        self.worker = SumarizacaoWorker(self.current_file_path)
        self.worker.finished.connect(self.handle_results)
        self.worker.error.connect(self.handle_error)
        self.worker.start()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SumarizadorApp()
    window.show()
    sys.exit(app.exec())