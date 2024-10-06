#include "sentence_embedding.h"
#include <cmath>
#include <stdexcept>

SentenceEmbedding::SentenceEmbedding(const std::string& sentence_, const std::vector<float>& embedding_)
    : sentence(sentence_), embedding(embedding_) {}

std::string SentenceEmbedding::get_sentence() const {
    return sentence;
}

std::vector<float> SentenceEmbedding::get_embedding() const {
    return embedding;
}

float dot_product(const std::vector<float>& a, const std::vector<float>& b) {
    if (a.size() != b.size()) {
        throw std::invalid_argument("Vectors must be of the same size for dot product.");
    }
    float result = 0.0;
    for (size_t i = 0; i < a.size(); ++i) {
        result += a[i] * b[i];
    }
    return result;
}

float magnitude(const std::vector<float>& v) {
    float sum = 0.0;
    for (float value : v) {
        sum += value * value;
    }
    return std::sqrt(sum);
}

float SentenceEmbedding::cosine_similarity(const SentenceEmbedding& other) const {
    const std::vector<float>& other_embedding = other.get_embedding();
    
    float dot_prod = dot_product(embedding, other_embedding);
    float magnitude_a = magnitude(embedding);
    float magnitude_b = magnitude(other_embedding);
    
    if (magnitude_a == 0 || magnitude_b == 0) {
        throw std::runtime_error("Cannot calculate cosine similarity with zero magnitude vector.");
    }

    return dot_prod / (magnitude_a * magnitude_b);
}

std::tuple<int, float> SentenceEmbedding::most_similar(const std::vector<SentenceEmbedding>& embeddings) const {
    int most_similar_index = -1;
    float highest_similarity = -1.0;
    
    for (size_t i = 0; i < embeddings.size(); ++i) {
        float similarity = cosine_similarity(embeddings[i]);
        if (similarity > highest_similarity) {
            highest_similarity = similarity;
            most_similar_index = i;
        }
    }

    return std::make_tuple(most_similar_index, highest_similarity);
}
