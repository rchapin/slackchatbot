import os
import string
import yaml
from sklearn.utils import Bunch
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.linear_model import SGDClassifier

class NlpProcessor(object):

    def __init__(self, logger, configs):
        self.logger = logger
        self.configs = configs
        self.probability_threshold = self.configs['answer_probability_threshold']
        self.training_set_dir = self.configs['training_set_dir']
        self.initialize_model()

    def initialize_model(self):
        self.training_set_data, self.training_set_target, self.training_set_target_names, self.answers = NlpProcessor.load_training_set(self.training_set_dir)

        # Tokenize the data
        self.count_vectorizer = CountVectorizer()
        x_train_counts = self.count_vectorizer.fit_transform(self.training_set_data)

        # Getting the frequencies of the data
        self.tfidf_transformer = TfidfTransformer()
        x_train_tfidf = self.tfidf_transformer.fit_transform(x_train_counts)

        # FIXME: make all of the following knobs configs
        self.classifier = SGDClassifier(
            loss='modified_huber',
            penalty='l2',
            alpha=1e-3,
            random_state=42,
            max_iter=5,
            tol=None)
        self.classifier.fit(x_train_tfidf, self.training_set_target)

    def get_prediction(self, message:string):
        retval = None
        x_new_counts = self.count_vectorizer.transform([message])
        x_new_tfidf = self.tfidf_transformer.transform(x_new_counts)
        predicted_probabilities = self.classifier.predict_proba(x_new_tfidf)

        if predicted_probabilities is not None and len(predicted_probabilities) > 0:
            probable_target, probability = NlpProcessor.get_probable_target_id(
                predicted_probabilities[0],
                self.probability_threshold)
            if probable_target is not None:
                self.logger.info(f'probability={probability} for message={message}')
                answer_key = self.training_set_target_names[probable_target]
                retval = self.answers.get(answer_key, None)

        return retval

    @staticmethod
    def get_probable_target_id(probabilities:[] , threshold:float) -> tuple:
        retval = None
        current_max = 0
        idx = -1
        for probability in probabilities:
            idx += 1
            if probability >= threshold:
                if probability > current_max:
                    current_max = probability
                    retval = idx
        return retval, current_max

    @staticmethod
    def load_training_set(input_path:str) -> tuple:
        '''
        Generate an array with the names of the categories
        bundle.target_names = [ 'spanish', 'call-counter' ]

        The data is an array of all of the documents
        bundle.data = [ 'doc1 content', 'doc2 content, etc]

        The target array is an array that has an entry for each element in
        the data array, the number points to the index in the target_names
        array
        bundle.target [ 0, 1, 1, 0]
        '''
        training_data = {}
        for file in os.listdir(input_path):
            if file.endswith('.yaml'):
                input_file_path = os.path.join(input_path, file)
                with open(input_file_path, 'r') as fh:
                    input_entry = yaml.load(fh, Loader=yaml.FullLoader)
                    training_data[input_entry['name']] = dict(
                        questions=input_entry['questions'],
                        answer=input_entry['answer'],
                        )
        # Build the arrays to return in the Bunch
        answers = {}
        target_names = []
        data = []
        target = []
        idx = 0
        for category_name, category_data in training_data.items():
            target_names.append(category_name)
            answers[category_name] = category_data['answer']
            for question in category_data['questions']:
                '''
                Append to the data array and then append the idx value
                to the corresponding target array.
                '''
                data.append(question)
                target.append(idx)
            idx += 1

#         training_set = Bunch(target_names=target_names, data=data, target=target)
        return data, target, target_names, answers