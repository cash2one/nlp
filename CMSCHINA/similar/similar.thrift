#file similar.thrift
# thrift --gen py tutorial.thrift
namespace py similar
service SimilarService {
    string synonym(1:string word, 2:string mode),
    string nearsynonym(1:string word, 2:i32 topn, 3:string mode)
    }
