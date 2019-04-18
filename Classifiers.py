import pickle
import Preprocessor
import TwitterAPI


class Classifier(object):
    pickle = "pickle/"
    preprocessor = Preprocessor.Preprocessor()
    twitter_api = TwitterAPI.TwitterAPI()

    def __init__(self, prediction_type):
        self.prediction_type = prediction_type

    def get_prediction_type(self):
        return self.prediction_type


class TweetClassifier(Classifier):
    _proba_value = None
    _proba_score = None

    def __init__(self):
        prediction_type = "Tweet Classification"
        Classifier.__init__(self, prediction_type)
        print("Tweet Classification Initialized")

    def load_model(self):
        # load the SpamTweetDetectModel from directory
        filename = self.pickle + "SpamTweetDetectModel.sav"
        nltk_ensemble = pickle.load(open(filename, 'rb'))
        return nltk_ensemble

    def load_word_features(self):
        # load the SpamTweetDetectModel word_features from directory
        filename = self.pickle + "wordfeatures.p"
        word_features = pickle.load(open(filename, 'rb'))
        return word_features

    def classify(self, tweet_obj):
        # load from pickle
        nltk_ensemble_model = self.load_model()
        word_features = self.load_word_features()

        # preprocess tweet
        processed_tweet = self.preprocessor.preprocess_tweet(tweet_obj.text)

        # find features
        features_tweet = self.find_features(word_features, processed_tweet)

        # classify using model and get scores
        self._proba_score = nltk_ensemble_model.classify(features_tweet)
        self._proba_value = nltk_ensemble_model.prob_classify(features_tweet)

    def find_features(self, word_features, processed_tweet):
        features_tweet = self.preprocessor.find_features_tweet(word_features, processed_tweet)
        return features_tweet

    def get_proba_value(self):
        return self._proba_value

    def get_prediction_score(self):
        return self._proba_score


class UserClassifier(Classifier):
    _proba_value = None
    _proba_score = None

    def __init__(self):
        prediction_type = "User Classification"
        Classifier.__init__(self, prediction_type)
        print("User Classification Initialized")

    def load_model(self):
        filename = self.pickle + "SpamUserDetectModel.sav"
        model_decision_tree = pickle.load(open(filename, 'rb'))
        return model_decision_tree

    def classify(self, tweet_obj):
        # load from pickle
        decision_tree_model = self.load_model()

        # get user object from tweet object
        user_obj = self.find_tweet_user(tweet_obj)

        # get features from user obj
        user_features = self.get_features_user(user_obj)

        # classify and add score to classifier
        self._proba_score = decision_tree_model.predict(user_features)
        self._proba_value = decision_tree_model.predict_proba(user_features)

    def get_proba_value(self):
        return self._proba_value

    def get_prediction_score(self):
        return self._proba_score

    def find_tweet_user(self, tweet_obj):
        tweet_user = self.twitter_api.findTweetUser(tweet_obj)
        return tweet_user

    def get_features_user(self, user_obj):
        user_features = self.preprocessor.preprocess_user(user_obj)
        return user_features