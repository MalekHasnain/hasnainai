SIDEBAR (exact, replace ACTIVE_TOPIC with class="active"):
<aside class="sidebar">
    <div class="brand">Hasnain<span>AI</span></div>
    <div class="tagline">HCCDA-AI prep &amp; practice</div>
    <nav>
      <a href="/index.html">🏠 Home</a>
      <a href="/concepts.html">📚 Core Concepts</a>
      <div style="color:var(--muted);font-size:.75rem;margin:14px 0 4px 10px;">TOPICS (class sequence)</div>
      <a href="/topics/confusion-matrix.html"><span class="num">01</span>Confusion Matrix</a>
      <a href="/topics/cnn.html"><span class="num">02</span>CNN</a>
      <a href="/topics/dbscan.html"><span class="num">03</span>DBSCAN</a>
      <a href="/topics/vgg16.html"><span class="num">04</span>VGG16</a>
      <a href="/topics/logistic-regression.html"><span class="num">05</span>Logistic Regression</a>
      <a href="/topics/simple-linear-regression.html"><span class="num">06</span>Simple Linear Regression</a>
      <a href="/topics/pca.html"><span class="num">07</span>PCA</a>
      <a href="/topics/kmeans.html"><span class="num">08</span>K-Means</a>
      <a href="/topics/multiple-regression.html"><span class="num">09</span>Multiple Regression</a>
      <a href="/topics/rnn.html"><span class="num">10</span>RNN</a>
      <div style="margin-top:18px;padding:10px;border:1px solid var(--border);border-radius:8px;background:#1f2630;">
        <div style="font-size:.78rem;color:var(--muted);">🤝 Collaborate on projects</div>
        <a href="https://wa.me/923446466664" target="_blank" rel="noopener" style="display:block;margin-top:4px;font-size:.85rem;">💬 WhatsApp: +92 344 646 6664</a>
      </div>
    </nav>
  </aside>

RULES FOR THE TOPIC PAGE (follow EXACTLY):
1. Full HTML5 doc: <!DOCTYPE html><html lang="en"><head> charset, viewport, <title>TOPIC — HasnainAI</title>, <link rel="stylesheet" href="/assets/style.css"> </head>
2. <body><div class="layout"> + the SIDEBAR above (mark this topic's link class="active").
3. <main> structure IN THIS ORDER:
   - <h1>Topic Name</h1>
   - <div class="meta"> chips: task type (Regression/Classification/Clustering/Dimensionality reduction/Neural network/Evaluation), dataset (Kaggle name), library (sklearn etc.)
   - <h2>What it is (short intro)</h2> — 2-4 paragraphs plain-English intro.
   - <h2>The math inside</h2> — formulas in <div class="formula">…</div> (use plain HTML/Unicode math like &Sigma;, &sigma;, &radic;, subscripts <sub></sub>, NOT LaTeX). For each formula, one plain sentence under it saying what it computes. Also define any NEW math/stat function this algorithm uses that is NOT already in /concepts.html — link it: <a href="/concepts.html">already explained in Core Concepts</a>. NEVER redefine: mean, variance, std, covariance, correlation, percentile/IQR, Euclidean/Manhattan distance, matrix/eigenvector/eigenvalue, determinant, gradient descent, sigmoid, softmax, log loss, derivative, argmax, normalization, train/test split, overfitting, underfitting, bias, cross-validation, augmentation, anomaly methods, supervised/unsupervised, regression/classification/clustering, feature/target, probability sample, imputer. If your topic needs a term not in that list, define it in a <div class="term"> box.
   - <h2>Diagram</h2> — use EXACTLY the image URL given for this topic: <figure><img src="URL" alt="..."><figcaption>Source: Wikipedia/Wikimedia Commons</figcaption></figure>. One sentence explaining what to notice in the diagram.
   - <h2>Dataset (Kaggle)</h2> — name + kagglehub slug + one-paragraph story of the dataset (rows, columns, target if any).
   - <h2>Practice code — run in Google Colab, top to bottom</h2> — a callout: <div class="callout">Blocks must run in order. Copy each block into Colab…</div>, then for EACH block:
       <div class="block-label">BLOCK N: title</div>
       short <p> why this block exists (1-2 sentences)</p>
       <pre><code>CODE with # comments in ENGLISH on nearly every line (why + what math it did)</code></pre>
     6-11 blocks per topic: imports → dataset download via kagglehub + glob → load/look → preprocessing (scaling/imputer if needed) → split if supervised → train → predict → evaluate (metrics relevant to the algo; confusion matrix for classifiers) → one insight/visualization block → one "use it on new input" block if sensible.
   - <h2>Real-world use cases &amp; companies</h2> — table or list: use case → who uses it (verifiable public examples, e.g. Netflix recommendations, PayPal fraud detection, Google Photos).
   - <h2>Combining with other algorithms (project ideas)</h2> — 2-4 concrete pipelines, each 2-3 sentences, referencing the other 9 topics by name.
   - <h2>Interview Q&amp;A</h2> — 6-10 <div class="qa"><div class="q">Q…</div><div class="a">A…</div></div> in ENGLISH. Include at least one question linking this algorithm to another from the 10 topics (e.g. "How is K-Means different from DBSCAN?"). Include teacher-style conceptual questions.
   - <div class="prevnext"> ← previous topic | next topic → </div> (link list given per topic)
   - <p class="footer-note">…</p>
4. Before </body> add this exact copy-button script:
<script>
document.querySelectorAll('pre').forEach(p => {
  const b = document.createElement('button');
  b.className = 'copy-btn'; b.textContent = 'Copy';
  b.onclick = () => { navigator.clipboard.writeText(p.innerText); b.textContent = 'Copied!'; setTimeout(()=>b.textContent='Copy',1200); };
  p.appendChild(b);
});
</script>
5. Comments in code: ENGLISH only. Page prose: English. Escape all <, >, & inside <pre><code> as &lt; &gt; &amp;.
6. Python must be correct: import everything used; pandas/numpy/sklearn/colab-safe (kagglehub, matplotlib, seaborn). No fabricated URLs.
