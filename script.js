async function searchDocuments() {
    let query = document.getElementById("searchQuery").value;
    
    let response = await fetch("http://127.0.0.1:8000/api/search", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query })
    });

    let data = await response.json();
    displayResults(data.documents);
}

function displayResults(documents) {
    let resultsDiv = document.getElementById("results");
    resultsDiv.innerHTML = "";

    if (documents.length === 0) {
        resultsDiv.innerHTML = "<p>No results found.</p>";
        return;
    }

    documents.forEach(doc => {
        let docElement = document.createElement("div");
        docElement.innerHTML = `<h3>${doc.title}</h3><p>${doc.summary}</p>`;
        resultsDiv.appendChild(docElement);
    });
}

async function uploadFile() {
    let fileInput = document.getElementById("fileInput");
    let file = fileInput.files[0];

    if (!file) return;

    let formData = new FormData();
    formData.append("file", file);

    let response = await fetch("http://127.0.0.1:8000/api/upload", {
        method: "POST",
        body: formData
    });

    let data = await response.json();
    document.getElementById("uploadStatus").innerText = data.message;
}

// Simulate admin access (set to false for regular users)
let isAdmin = true;
if (!isAdmin) {
    document.getElementById("adminUpload").style.display = "none";
}
