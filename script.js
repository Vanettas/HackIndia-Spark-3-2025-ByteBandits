// Dynamically detect backend URL based on current origin
const API_BASE_URL = `${window.location.origin.replace(":5500", ":8000")}`;  // Replace frontend port with backend port

console.log("Backend URL:", API_BASE_URL);  // Debugging

// 🔹 Function to check admin login and enable upload section
function checkAdmin() {
    const enteredPassword = document.getElementById("adminPassword").value;
    const correctPassword = "admin123";  // Set your secure admin password (Change this in production)

    if (enteredPassword === correctPassword) {
        document.getElementById("adminUpload").style.display = "block";  // Show upload section
        document.getElementById("adminLogin").style.display = "none";  // Hide login form
        alert("Admin access granted!");
    } else {
        alert("Incorrect password! Access denied.");
    }
}

// 🔹 Function to search documents using FastAPI
async function searchDocuments() {
    let query = document.getElementById("searchQuery").value.trim();

    if (!query) {
        alert("Please enter a search query.");
        return;
    }

    try {
        let response = await fetch(`${API_BASE_URL}/api/search`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ query })
        });

        if (!response.ok) {
            throw new Error(`Search failed: ${response.statusText}`);
        }

        let data = await response.json();
        if (data.error) {
            alert(`Error: ${data.error}`);
            return;
        }

        displayResults(data.documents);
    } catch (error) {
        console.error("Error:", error);
        alert("Failed to fetch search results.");
    }
}

async function uploadAndSummarize() {
    let fileInput = document.getElementById("summaryFileInput");
    let file = fileInput.files[0];

    if (!file) {
        alert("Please select a file to upload.");
        return;
    }

    let formData = new FormData();
    formData.append("file", file);  // 🔹 Ensure key is "file", matching FastAPI

    try {
        let response = await fetch(`${API_BASE_URL}/api/upload`, {
            method: "POST",
            body: formData
        });

        if (!response.ok) {
            throw new Error(`Upload failed: ${response.statusText}`);
        }

        let data = await response.json();
        document.getElementById("uploadStatus").innerText = `Uploaded to Firebase: ${data.file_url}`;

        // 🔹 Summarize the uploaded document
        summarizeText(data.file_url);

    } catch (error) {
        console.error("Error:", error);
        alert("File upload failed.");
    }
}


// 🔹 Function to summarize text using FastAPI
async function summarizeText(fileUrl) {
    try {
        let response = await fetch(`${API_BASE_URL}/api/summarize`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ file_url: fileUrl })
        });

        if (!response.ok) {
            throw new Error(`Summarization failed: ${response.statusText}`);
        }

        let data = await response.json();
        document.getElementById("summaryResult").innerText = data.summary || "Error: Could not generate summary.";

    } catch (error) {
        console.error("Error:", error);
        alert("Summarization failed.");
    }
}
// 🔹 Function to display search results
function displayResults(documents) {
    let resultsDiv = document.getElementById("results");
    resultsDiv.innerHTML = "";

    if (!documents || documents.length === 0) {
        resultsDiv.innerHTML = "<p>No results found.</p>";
        return;
    }

    documents.forEach(doc => {
        let docElement = document.createElement("div");
        docElement.className = "result-item";
        docElement.innerHTML = `<h3>${doc.title}</h3><p>${doc.summary}</p>`;
        resultsDiv.appendChild(docElement);
    });
}
