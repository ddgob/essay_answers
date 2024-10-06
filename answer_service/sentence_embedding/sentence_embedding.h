#ifndef SENTENCE_EMBEDDING_H
#define SENTENCE_EMBEDDING_H

#include <vector>
#include <string>
#include <tuple>

class SentenceEmbedding {

    public:
        SentenceEmbedding(const std::string& sentence_, const std::vector<float>& embedding_);
        
        std::string get_sentence() const;
        std::vector<float> get_embedding() const;

        float cosine_similarity(const SentenceEmbedding& other) const;

        std::tuple<int, float> most_similar(const std::vector<SentenceEmbedding>& embeddings) const;

    private:
        std::string sentence;
        std::vector<float> embedding;
};

#endif
