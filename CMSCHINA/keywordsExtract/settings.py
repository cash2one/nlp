# bigram parameters
bigram_min_count = 2
bigram_threshold = 4

# trigram parameters
trigram_min_count = 2
trigram_threshold =3

#baidu df param
all_doc_num = 10000000000

# parameter to remove redundant phrase
similarity_threshold = 0.65

# output numbers
topN = 10000

# input files
stopwords = 'user_dicts/stopwords.txt'  # stopwords
df_file = 'user_dicts/cmschina_df.txt'
user_file = 'user_dicts/user_dict.txt'
noise_file = 'user_dicts/noise_dict.txt'
finance_file = 'user_dicts/jr.txt'
# new_cmschina_df param
cmschina_doc_num = 1506837
