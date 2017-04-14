namespace py sentiment
service SentimentService {
    string get_sentiment(1:string word, 2:string mode),
    string get_opinion_sentence(1:string text, 2:double ratio) 
}
