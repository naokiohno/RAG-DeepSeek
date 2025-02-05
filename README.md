# RAG-DeepSeek
Proof of concept application of RAG using the DeepSeek chat model.

Langchain's DeepSeek implementation is nearly indentical to its OpenAI counterpart, therefore, swapping OpenAI's GPT model to DeepSeek's Chat model is quite straightforward. In this demonstration, PDF files are used as a context for RAG. As DeepSeek doesn't provide its own embedder, OpenAI's embedder is retained.
