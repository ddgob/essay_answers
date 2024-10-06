#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include "sentence_embedding.h"

namespace py = pybind11;

PYBIND11_MODULE(sentence_embedding, m) {
    py::class_<SentenceEmbedding>(m, "SentenceEmbedding")
        .def(py::init<const std::string&, const std::vector<float>&>())
        .def("get_sentence", &SentenceEmbedding::get_sentence)
        .def("get_embedding", &SentenceEmbedding::get_embedding)
        .def("cosine_similarity", &SentenceEmbedding::cosine_similarity)
        .def("most_similar", &SentenceEmbedding::most_similar);
}
