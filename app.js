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



// Function to Submit Feedback with API call
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

        // Check for valid category and sentiment by verifying their type explicitly
        console.log("Received data:", data); // Log the entire response
        console.log("Type of data.category:", typeof data.category); // Check type of category
        console.log("Type of data.sentiment:", typeof data.sentiment); // Check type of sentiment

        if (typeof data.category !== "string" || typeof data.sentiment !== "string") {
            console.error("Invalid response structure from API:", data);
            return;
        }

        const category = data.category;
        const sentiment = data.sentiment;

        console.log("Received from backend:", data); // Log the backend response

        // Retrieve and update categories in localStorage
        const categories = JSON.parse(localStorage.getItem("categories"));
        console.log("Categories object in localStorage:", categories);  // Log all categories

        // Check if category exists in localStorage and update it
        if (categories[category]) {
            if (sentiment === "positive") {
                categories[category].positiveFeedback += 1;
                categories[category].ranking -= 1; // Positive feedback decreases ranking
            } else if (sentiment === "negative") {
                categories[category].negativeFeedback += 1;
                categories[category].ranking += 1; // Negative feedback increases ranking
            }
            console.log("Updated category in localStorage:", categories[category]);
        } else {
            console.error("Category not found in localStorage:", category);
        }

        // Save the updated categories back to localStorage
        localStorage.setItem("categories", JSON.stringify(categories));

        // Update other localStorage items if necessary
        const issues = JSON.parse(localStorage.getItem("issues"));
        let progressTracker = JSON.parse(localStorage.getItem("progressTracker"));

        // Add the new issue to issues array
        const newIssue = { id: issues.length + 1, content, category, department };
        issues.push(newIssue);
        localStorage.setItem("issues", JSON.stringify(issues));

        // Add entry to progress tracker if not already present
        if (!progressTracker.find(entry => entry.category === category && entry.department === department)) {
            progressTracker.push({
                department,
                category,
                status: "To Do",
                actionsTaken: []
            });
        }
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



// Updated Function to Display Top Issues (based on positive/negative feedback difference)
function displayTopIssues() {
    const categories = JSON.parse(localStorage.getItem("categories"));

    // Sort categories by the difference between negative and positive feedback
    const sortedCategories = Object.values(categories).sort((a, b) => {
        const diffA = a.negativeFeedback - a.positiveFeedback;
        const diffB = b.negativeFeedback - b.positiveFeedback;
        return diffB - diffA; // Sort by largest negative difference
    });

    // Display the top 3 issues based on the largest negative difference
    const topIssuesList = document.getElementById("top-issues-list");
    topIssuesList.innerHTML = sortedCategories.slice(0, 3).map(cat => {
        const difference = cat.negativeFeedback - cat.positiveFeedback;
        return `<li>${cat.name}: Negative Difference = ${difference}</li>`;
    }).join("");
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
    const departmentFilter = document.getElementById("progress-department-filter").value;
    const progressTracker = JSON.parse(localStorage.getItem("progressTracker"));
    const filteredProgress = departmentFilter === "all" ? progressTracker : progressTracker.filter(prog => prog.department === departmentFilter);

    const progressList = document.getElementById("progress-list");
    progressList.innerHTML = filteredProgress.map(prog => {
        return `<li>Department: ${prog.department} | Category: ${prog.category} | Status: ${prog.status} | Actions Taken: ${prog.actionsTaken.join(", ")}</li>`;
    }).join("");
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
