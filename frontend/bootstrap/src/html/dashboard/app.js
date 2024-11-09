// Expanded WHO-based categories
const initialCategories = {
    underused_skills: { name: "Under-use of Skills", positiveFeedback: 0, negativeFeedback: 0, ranking: 0 },
    excessive_workload: { name: "Excessive Workload", positiveFeedback: 0, negativeFeedback: 0, ranking: 0 },
    long_hours: { name: "Long, Unsocial or Inflexible Hours", positiveFeedback: 0, negativeFeedback: 0, ranking: 0 },
    lack_of_control: { name: "Lack of Control Over Job Design", positiveFeedback: 0, negativeFeedback: 0, ranking: 0 },
    unsafe_conditions: { name: "Unsafe or Poor Physical Conditions", positiveFeedback: 0, negativeFeedback: 0, ranking: 0 },
    negative_culture: { name: "Negative Organizational Culture", positiveFeedback: 0, negativeFeedback: 0, ranking: 0 },
    limited_support: { name: "Limited Support from Colleagues", positiveFeedback: 0, negativeFeedback: 0, ranking: 0 },
    violence_harassment: { name: "Violence, Harassment, or Bullying", positiveFeedback: 0, negativeFeedback: 0, ranking: 0 },
    discrimination: { name: "Discrimination and Exclusion", positiveFeedback: 0, negativeFeedback: 0, ranking: 0 },
    unclear_role: { name: "Unclear Job Role", positiveFeedback: 0, negativeFeedback: 0, ranking: 0 },
    under_promotion: { name: "Under- or Over-promotion", positiveFeedback: 0, negativeFeedback: 0, ranking: 0 },
    job_insecurity: { name: "Job Insecurity or Inadequate Pay", positiveFeedback: 0, negativeFeedback: 0, ranking: 0 },
    work_home_conflict: { name: "Conflicting Home/Work Demands", positiveFeedback: 0, negativeFeedback: 0, ranking: 0 }
};

if (!localStorage.getItem("categories")) localStorage.setItem("categories", JSON.stringify(initialCategories));
if (!localStorage.getItem("issues")) localStorage.setItem("issues", JSON.stringify([]));
if (!localStorage.getItem("progressTracker")) localStorage.setItem("progressTracker", JSON.stringify([]));
if (!localStorage.getItem("visibilitySettings")) localStorage.setItem("visibilitySettings", JSON.stringify({ visibilityOption: "company-wide" }));

// Populate categories in the feedback form
const categorySelect = document.getElementById("feedback-category");
Object.keys(initialCategories).forEach(categoryKey => {
    const option = document.createElement("option");
    option.value = categoryKey;
    option.textContent = initialCategories[categoryKey].name;
    categorySelect.appendChild(option);
});



async function submitFeedback() {
    const department = document.getElementById("feedback-department").value;
    const content = document.getElementById("feedback-content").value;

    try {
        // Send the feedback content to Flask API for classification
        const response = await fetch("http://127.0.0.1:5000/classify_feedback", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ content })
        });

        // Parse the response from the server
        const data = await response.json();

        // Log received data and check response structure
        console.log("Received data:", data);
        if (typeof data.category !== "string" || typeof data.sentiment !== "string" || typeof data.summary !== "string") {
            console.error("Invalid response structure from API:", data);
            return;
        }

        const { category, sentiment, summary } = data;

        // Retrieve and update categories in localStorage
        const categories = JSON.parse(localStorage.getItem("categories"));
        console.log("Categories object in localStorage:", categories);

        // Update category feedback counters
        if (categories[category]) {
            if (sentiment === "positive") {
                categories[category].positiveFeedback += 1;
                categories[category].ranking -= 1;
            } else if (sentiment === "negative") {
                categories[category].negativeFeedback += 1;
                categories[category].ranking += 1;
            }
            console.log("Updated category in localStorage:", categories[category]);
        } else {
            console.error("Category not found in localStorage:", category);
        }

        // Save the updated categories back to localStorage
        localStorage.setItem("categories", JSON.stringify(categories));

        // Update issues and progress tracker
        const issues = JSON.parse(localStorage.getItem("issues"));

        const newIssue = {
            id: issues.length + 1,
            summary,       // High-level summary from AI
            content,       // Detailed user input
            department,    // Department chosen by user
            category       // AI-determined category
        };
        issues.push(newIssue);
        localStorage.setItem("issues", JSON.stringify(issues));

        // Add entry to progress tracker if not already present
        let progressTracker = JSON.parse(localStorage.getItem("progressTracker"));
        progressTracker.push({
            issueId: newIssue.id,       // Link to the issue ID for cross-reference
            department,
            category,
            summary,
            status: "To Do",            // Default status for new issues
            tags: [category],           // Tags to track issue nature
            actionsTaken: []            // Array to store progress notes or actions
        });
        localStorage.setItem("progressTracker", JSON.stringify(progressTracker));

        // Update the UI
        displayTopIssues();
        displayStatistics();
        displayProgress();
        document.getElementById("feedback-content").value = "";

    } catch (error) {
        console.error("Error submitting feedback:", error);
    }
}



// Updated Function to Display Top Issues with Sorting and Clickable Links
function displayTopIssues() {
    const categories = JSON.parse(localStorage.getItem("categories"));
    const issues = JSON.parse(localStorage.getItem("issues"));

    // Sort categories by the difference between negative and positive feedback
    const sortedCategories = Object.values(categories).sort((a, b) => {
        const diffA = a.negativeFeedback - a.positiveFeedback;
        const diffB = b.negativeFeedback - b.positiveFeedback;
        return diffB - diffA; // Sort by largest negative difference
    });

    const topIssuesList = document.getElementById("top-issues-list");

    // Display the top issues based on sorted categories
    topIssuesList.innerHTML = sortedCategories.slice(0, 3).map(cat => {
        // Find the first issue related to this category (if available)
        const relatedIssue = issues.find(issue => issue.category === cat.name);
        const difference = cat.negativeFeedback - cat.positiveFeedback;

        return relatedIssue
            ? `<li onclick="viewIssueInProgress(${relatedIssue.id})">${relatedIssue.summary}: Negative Difference = ${difference}</li>`
            : `<li>${cat.name}: No issues found in this category</li>`;
    }).join("");
}

// Function to set the selected issue in Progress Tracker
function viewIssueInProgress(issueId) {
    localStorage.setItem("selectedIssueId", issueId); // Store selected issue ID for Progress Tracker
    displayProgress(); // Refresh Progress Tracker to show the selected issue
}



// Function to Send User Input to Backend Chatbot
async function sendToChatbot() {
    const input = document.getElementById("chat-input").value;
    const chatbox = document.getElementById("chatbox");

    // Display user input in the chatbox
    chatbox.innerHTML += `<p>You: ${input}</p>`;
    document.getElementById("chat-input").value = ""; // Clear input field

    try {
        // Send user input to the Flask backend
        const response = await fetch("http://127.0.0.1:5000/get_chat_response", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ message: input })
        });

        // Parse the response from the backend
        const data = await response.json();
        const botResponse = data.response || "Sorry, I couldn't understand that."; // Default response if none provided

        // Display the bot's response in the chatbox
        chatbox.innerHTML += `<p>Bot: ${botResponse}</p>`;
    } catch (error) {
        console.error("Error communicating with chatbot:", error);
        chatbox.innerHTML += `<p>Bot: Sorry, there was an error processing your request.</p>`;
    }
}





// Function to Display Homepage Statistics
function displayStatistics() {
    const categories = JSON.parse(localStorage.getItem("categories"));
    const statisticsDiv = document.getElementById("statistics");
    const stats = Object.values(categories).map(cat => `<p>${cat.name} - Positive: ${cat.positiveFeedback}, Negative: ${cat.negativeFeedback}</p>`).join("");
    statisticsDiv.innerHTML = stats;
}




// Updated Function to Track Progress
function displayProgress() {
    const selectedIssueId = localStorage.getItem("selectedIssueId");
    const progressTracker = JSON.parse(localStorage.getItem("progressTracker"));
    const selectedIssue = progressTracker.find(entry => entry.issueId == selectedIssueId);

    const progressList = document.getElementById("progress-list");
    if (selectedIssue) {
        progressList.innerHTML = `
            <h3>${selectedIssue.summary}</h3>
            <p><strong>Department:</strong> ${selectedIssue.department}</p>
            <p><strong>Status:</strong> ${selectedIssue.status}</p>
            <p><strong>Tags:</strong> ${selectedIssue.tags.join(", ")}</p>
            <p><strong>Details:</strong> ${selectedIssue.content}</p>
            <p><strong>AI Advice:</strong> Add advice or insights here</p>
            <p><strong>Company Notes:</strong> ${selectedIssue.actionsTaken.join("<br>")}</p>
            <div><strong>Progress:</strong>
                <progress value="${getProgressValue(selectedIssue.status)}" max="100"></progress>
            </div>
        `;
    } else {
        progressList.innerHTML = "<p>Select an issue from Top Issues to view its progress.</p>";
    }
}





// Function to Update Visibility Settings
function updateVisibility() {
    const visibilityOption = document.getElementById("visibility-option").value;
    localStorage.setItem("visibilitySettings", JSON.stringify({ visibilityOption }));
    alert(`Visibility updated to ${visibilityOption}`);
}




// Initial Display of All Views
displayTopIssues();
displayStatistics();
displayProgress();
