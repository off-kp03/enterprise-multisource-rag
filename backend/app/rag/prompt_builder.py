from typing import List, Dict

class PromptBuilder:
    """
    Builds grounded prompts for RAG using retrieved documents.
    """

    def build(
        self,
        question: str,
        retrieved_chunks: List[Dict],
    ) -> Dict[str, str]:
        
        """
        Returns a dict with system_prompt and user_prompt.
        """

        if not retrieved_chunks:
            raise ValueError("No retrieved documents provided")

        context_blocks = []

        for idx, chunk in enumerate(retrieved_chunks, start=1):
            metadata = chunk.get("metadata", {})
            source = metadata.get("source", "unknown")
            page = metadata.get("page", "N/A")
            file_name = metadata.get("file_name", "unknown")

            block = (
                f"[Source {idx}]\n"
                f"File: {file_name}\n"
                f"Page: {page}\n"
                f"Content:\n{chunk.get('text')}\n"
            )
            context_blocks.append(block)

        context = "\n".join(context_blocks)

        system_prompt = (
            "You are an assistant answering questions using ONLY the provided sources.\n"
            "Rules:\n"
            "- Use only the information in the sources.\n"
            "- Do not make up facts.\n"
            "- If the answer is not present, say you don't know.\n"
            "- Cite sources using [Source X] notation.\n"
        )

        user_prompt = (
            f"Question:\n{question}\n\n"
            f"Sources:\n{context}\n\n"
            "Answer the question using the sources above. "
            "Include citations in your answer."
        )

        return {
            "system_prompt": system_prompt,
            "user_prompt": user_prompt,
        }
