
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
  
  async function uploadDoc() {
    const fileInput = document.getElementById("fileInput");
    const fileNameSpan = document.getElementById("fileName");
    if (fileInput.files.length > 0) {
      const fileName = fileInput.files[0].name;
      fileNameSpan.textContent = fileName;
    } else {
      fileNameSpan.textContent = "No file selected";
    }
    const file = fileInput.files[0];
    if (!file) {
      alert("No file selected");
      return;
    }
  
    const formData = new FormData();
    formData.append("files", file);
  
    try {
      const res = await fetch("http://localhost:5000/upload-docs", {
        method: "POST",
        body: formData,
      });
  
      const data = await res.json();
  
      if (res.ok) {
        document.getElementById("fileName").textContent = fileInput.files[0].name;
        document.getElementById("uploadStatus").textContent = "✔ Uploaded";
      } else {
        document.getElementById("fileName").textContent = "";
        document.getElementById("uploadStatus").textContent = "✘ Upload failed";
      }
    } catch (err) {
      alert("Error uploading document");
      console.error(err);
    }
  
    fileInput.value = ""; 
  }  

 