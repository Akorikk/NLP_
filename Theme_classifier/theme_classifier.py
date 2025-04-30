import spacy
import pandas as pd
import numpy as np
import torch
from transformers import pipeline

nlp = spacy.load("en_core_web_sm")  # Make sure this is loaded globally

class ThemeClassifier():
    def __init__(self, theme_list):
        self.model_name = "facebook/bart-large-mnli"
        self.device = 0 if torch.cuda.is_available() else -1  # torch device -1 for CPU in transformers
        self.theme_list = theme_list
        self.theme_classifier = self.load_model()

    def load_model(self):
        return pipeline(
            "zero-shot-classification",
            model=self.model_name,
            device=self.device
        )

    def get_themes_inference(self, script):
        doc = nlp(script)
        script_sentences_spacy = [sent.text for sent in doc.sents]

        sentence_batch_size = 20
        script_batches = []
        for index in range(0, len(script_sentences_spacy), sentence_batch_size):
            sent = " ".join(script_sentences_spacy[index:index + sentence_batch_size])
            script_batches.append(sent)

        theme_output = self.theme_classifier(
            script_batches[:2],  # Limit to 2 batches to save time
            self.theme_list,
            multi_label=True
        )

        themes = {}
        for output in theme_output:
            for label, score in zip(output["labels"], output["scores"]):
                if label not in themes:
                    themes[label] = []
                themes[label].append(score)

        themes = {key: np.mean(np.array(value)) for key, value in themes.items()}
        return themes

    def get_themes(self, dataset_path, save_path=None):
        
        if save_path is not None and os.path.exists(save_path):
            df = pd.read_csv(save_path)
            return df

        # Load dataset
        df = load_subtitles_dataset(dataset_path)  # <- you had `load_model` here by mistake

        # Run inference
        output_themes = df['script'].apply(self.get_themes_inference)
        theme_df = pd.DataFrame(output_themes.tolist())
        df[theme_df.columns] = theme_df

        if save_path is not None:
            df.to_csv(save_path, index=False)

        return df
