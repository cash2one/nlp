namespace py segment
service SegmentService {
    string get_pos_tag(1:string word, 2:list<string> user_dicts),
    string get_ner(1:string word)
}
