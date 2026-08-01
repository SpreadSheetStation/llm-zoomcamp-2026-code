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

// GroundTruth //
Inside the GroundTruth folder there is a python script called generate_ground_truth.py which generates 5 new questions for each of my 10 original questions and puts them in a CSV: my_ground_truth.csv

== Search Evaluation ==
(This fulfils the Retrieval evaluation point of the evaluation criteria of the final project that is mentioned in project.md)
The python script search_evaluation tests 6 different boost combinations and tell us which one performs best. We can use this to evaluate multiple retrieval approaches, so we can use the best boost values we found in our final fp_rag_helper.py script
(I already adjusted fp_rag_helper.py with the best boost values found)

== LLM Evalution: Standard RAG vs Agentic RAG ==
For LLM Evaluation, I decided to put my Agentic RAG to the test, and see if Agentic RAG is really getting us better results compared to our Standard RAG.

Therefore I evaluated the two approaches, testing both approaches on your ground truth questions and compare their answers.

First I,
-Generated RAG answers (for all my ground truth questions using fp_rag_helper.py)
-Generated Agent answers (for all my ground truth questions using agentic_assistant.py)

Then I used an LLM judge to compare each answer against the original answer; calculated the score for each approach and eventually picked the best approach for your final project.

== Interface == https://youtu.be/1WOQJ6EYvTo
Streamlit UI App
CLI is also available

== Monitoring == https://youtu.be/1WOQJ6EYvTo
The project includes a monitoring system that tracks user interactions and displays metrics on a dashboard.

// Feedback Collection
When a user asks a question in the chat app, they can rate the answer with thumbs up or thumbs down. This feedback is saved to a CSV file (feedback.csv) along with:
-The question asked
-The answer given
-Response time
-Timestamp

// Dashboard
A separate Streamlit dashboard displays real-time metrics from the feedback data:
-Total Questions:    	    Total number of questions asked
-Thumbs Up / Down:	        Count of helpful vs. not helpful answers
-Feedback Distribution:	    Pie chart showing percentage of helpful vs. not helpful answers
-Most Asked Topics:  	    Donut chart showing which topics users ask about most
-Response Time Performance:	Gauge chart showing average response time to answer questions
-Response Time Over Time:	Line chart tracking response time trends
-Questions Per Day:      	Bar chart showing daily question volume
-Recent Feedback:           Most recent data feedback

/How to Use
1. Chat App: Run 
streamlit run streamlit_app.py --server.port 8501
 and ask questions. Click thumbs up or down to provide feedback.

2. Dashboard: Run 
streamlit run dashboard.py --server.port 8502 
and click the "Refresh Data" button to see updated metrics.

The dashboard displays charts using the data collected from user feedback. Each new interaction is appended to feedback.csv, and the dashboard updates when refreshed.

### Why CSV Instead of a Database?

For this capstone, I chose CSV over PostgreSQL for monitoring data storage. The main reasons:

- **Simplicity:** No Docker or database setup required—reviewers can run the app immediately.
- **Portability:** The `feedback.csv` file is self-contained and included in the repo.
- **Sufficient Scale:** With low expected traffic, CSV handles the data volume just fine.
- **Better Review Experience:** Peer reviewers see sample data and charts instantly without extra configuration.

While a database would be better for production-scale systems, the CSV approach is simpler, more reproducible, and fully meets the monitoring evaluation criteria for this project.