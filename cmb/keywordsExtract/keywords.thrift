namespace py keywords
service KeywordsService {
    string get_keywords(1:string word, 2:i32 topN)
}
