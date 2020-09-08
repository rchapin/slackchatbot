import functools
import os
import random
import string
import yaml
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.linear_model import SGDClassifier

@functools.total_ordering
class ProbabilityCandidate(object):

    def __init__(self, target_id:int, probability:float):
        self.target_id = target_id
        self.probability = probability

    def __lt__(self, other):
        return 0

    def __eq__(self, other) -> int:
        return (self.target_id, self.probability) == (other)

class NlpProcessor(object):

    def __init__(self, loggers, configs):
        self.logger = loggers['logger']
        self.stats_logger = loggers['stats_logger']
        self.configs = configs
        self.probability_threshold = self.configs['answer_probability_threshold']
        self.secondary_probably_process_threshold = self.configs['secondary_probably_process_threshold']

        self.training_set_dir = self.configs['training_set_dir']
        self.initialize_model()
        self.logger.info(f'NlpProcessor initialized with probability_threshold={self.probability_threshold}')

    def initialize_model(self):
        self.training_set_data, self.training_set_target, self.training_set_target_names, self.answers = NlpProcessor.load_training_set(self.training_set_dir)

        # Tokenize the data
        self.count_vectorizer = CountVectorizer()
        x_train_counts = self.count_vectorizer.fit_transform(self.training_set_data)

        # Getting the frequencies of the data
        self.tfidf_transformer = TfidfTransformer()
        x_train_tfidf = self.tfidf_transformer.fit_transform(x_train_counts)

        self.classifier = SGDClassifier(loss='log')
        self.classifier.fit(x_train_tfidf, self.training_set_target)
        self.seconsecondary_classifier = None
        if self.configs['secondary_probability_enabled']:
            self.secondary_classifier = SGDClassifier(
                loss='hinge',
                penalty='l2',
                alpha=1e-3,
                random_state=42,
                max_iter=5,
                tol=None)
            self.secondary_classifier.fit(x_train_tfidf, self.training_set_target)

    def get_prediction(self, message:string):
        retval = None
        x_new_counts = self.count_vectorizer.transform([message])
        x_new_tfidf = self.tfidf_transformer.transform(x_new_counts)
        predicted_probabilities = self.classifier.predict_proba(x_new_tfidf)

        if predicted_probabilities is not None and len(predicted_probabilities) > 0:
            result = dict(zip(self.training_set_target_names, predicted_probabilities[0]))
            self.stats_logger.info(f'{result}, message={message}')

            highest_probable_target, highest_probability = NlpProcessor.get_highest_probable_target_id(
                predicted_probabilities[0],
                self.probability_threshold)
            probable_target = None
            probability = None
            if highest_probability >= self.probability_threshold:
                '''
                No need to process any further, we have a reasonable answer to
                be returned.
                '''
                probable_target = highest_probable_target
                probability = highest_probability
            else:
                '''
                If we are above the secondary processing threshold we will make
                the assumption that one of the currently trained classes is the
                correct answer and will reprocess the intput.
                '''
                if highest_probability >= self.secondary_probably_process_threshold:
                    self.logger.info(
                        f'Running a secondary probability on highest_probability={highest_probability}')
                    secondary_prediction = self.secondary_classifier.predict(x_new_tfidf)
                    probable_target = secondary_prediction[0] if len(secondary_prediction) > 0 else None

            if probable_target is not None:
                answer_key = self.training_set_target_names[probable_target]
                retval = self.answers.get(answer_key, None)
                prob_stats = {'probability': probability, 'answer_key': answer_key, 'message': message}
                self.stats_logger.info(prob_stats)

        return retval

    @staticmethod
    def get_highest_probable_target_id(probabilities:[] , threshold:float) -> tuple:
        retval = None
        current_max = 0
        idx = -1
        for probability in probabilities:
            idx += 1
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

        answers = {}
        target_names = []
        idx = 0
        data_tuples = []
        for category_name, category_data in training_data.items():
            target_names.append(category_name)
            answers[category_name] = category_data['answer']

            for question in category_data['questions']:
                data_tuples.append((idx, question))
            idx += 1

        random.shuffle(data_tuples)
        data = []
        target = []
        for index, question in data_tuples:
            data.append(question)
            target.append(index)

        return data, target, target_names, answers