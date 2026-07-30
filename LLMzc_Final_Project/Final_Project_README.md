== Final Project ==
-Search tool is lexical-search-based and I tried to keep it simple, since the article is also relatively short and simple. 
-However, I do have decided to create an agentic RAG, so the LLM can decides when to search, what to search for, and when to stop searching and provide the final answer.
-Since I have a very small dataset, I decided to build the search index at startup each time with minsearch, which goes swiftly.


// DataSource //
I decided to use a relatively shorter Wikipedia article as my DataSource: "Dancing plague of 1518"
and saved this as WikiArticle.txt which you can find under the DataSource folder; and manually chunked per paragraph by adding triple dashes "---" for each chunk.
Link: https://en.wikipedia.org/wiki/Dancing_plague_of_1518

This resulted in 5 chunks since this was a relatively short article. Each of these chunks has a unique doc_id:
    doc_001
    doc_002
    doc_003
    doc_004
    doc_005
The doc_id is just for future/potential reference to get back to the source data on which the questions are based on. I neatly extracted the chunks in with a jupyter notebook and saved them as a CSV file (dancing_plague_chunks.csv) organised per doc_id and section.

== The QA Knowledge Base "the FAQ" ==
For each chunk/doc_id I thought up 2 questions manually via Google Sheets and downloaded this as a .csv file (which you can find in the DataSource folder):
qa_knowledge_base.csv
Each Q&A therefore has a unique qa_id:
    qa_001
    qa_002
    qa_003
    qa_004
    qa_005
    qa_006
    qa_007
    qa_008
    qa_009
    qa_010
This can help us with easy identification (and this will come in handy later, for evaluation with ground truth).



== Future potential implementations ==
So we have our current search that goes over our QA Knowledge Base, which are aka "the FAQ" of this project.
For a future expansion to this project, I might add an extra search tool, a "second layer" RAG search tool as a safety net for the agent. After searching the "first layer", if the agent has concluded it cannot find the answer, it is will use the "second layer" as a last resort. Here the agent will be exposed to a Knowledge Base where each chunk is categorised per section. The agent searches on section  (e.g. a question about modern theories will bring his search easily to the Modern theories section) and the "second layer" search tool will retrieve the chunk of that section. In this way it is a RAG application (no full content stuffing here, regardless that it is a relative short article).

Data provided for this KB will look like this:
3 columns:
doc_id | section | chunk