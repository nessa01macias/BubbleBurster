
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



