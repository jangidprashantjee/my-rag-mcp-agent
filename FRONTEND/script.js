
  async function sendQuery() {
    const textarea = document.getElementById("prompt");
    const prompt = textarea.value.trim();
    const responseDiv = document.getElementById("response");
  
    if (!prompt) return; 
    const interaction = document.createElement("div");
    interaction.className = "interaction";
    const promptEl = document.createElement("div");
    promptEl.className = "prompt";
    promptEl.textContent = "You: " + prompt;
    interaction.appendChild(promptEl);
    const answerEl = document.createElement("div");
    answerEl.className = "response";
    answerEl.textContent = "Thinking...";
    interaction.appendChild(answerEl);
    responseDiv.appendChild(interaction);
  
    try {
      const res = await fetch("http://localhost:5000/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt }),
      });
  
      const data = await res.json();
      answerEl.textContent = "AI: " + (data.response || "No response");
    } catch (err) {
      answerEl.textContent = "Error: " + err.message;
      answerEl.className = "error";
    }
  
    textarea.value = ""; 
  }
  