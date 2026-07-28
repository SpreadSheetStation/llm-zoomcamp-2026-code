== Final Project ==

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

This can help us with easy identification (and this will come in handy later, for evaluation with ground truth). The doc_id is just for future/potential reference to get back to the source data on which the questions are based on.



