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





// Initial Display of All Views
displayTopIssues();
displayStatistics();
displayProgress();
