document.getElementById("search-form").addEventListener("submit", function (e) {
    e.preventDefault();

    // Get filter values
    const style = document.getElementById("style").value;
    const artist = document.getElementById("artist").value;
    const technique = document.getElementById("technique").value;
    const popularity = document.getElementById("popularity").value;
    const keyword = document.getElementById("keyword").value;

    // Build request payload
    const payload = {
        style,
        artist,
        technique,
        keyword,
        popularity
    };

    // Make POST request to backend
    fetch("/search", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
    })
        .then((response) => response.json())
        .then((data) => {
            // Populate the Matching Results dropdown
            const matchingResults = document.getElementById("matching-results");
            matchingResults.innerHTML = '<option value="">-- Bir Eşleşme Seçin --</option>'; // Clear previous results

            data.forEach((row, index) => {
                const option = document.createElement("option");
                option.value = index; // Use index as the value to identify the song
                option.textContent = row["Turku Adi"]; // Display the song name
                matchingResults.appendChild(option);
            });

            // Store results globally for accessing details later
            window.searchResults = data;
        })
        .catch((error) => console.error("Error:", error));
});

// Listen for selection changes in the Matching Results dropdown
document.getElementById("matching-results").addEventListener("change", function (e) {
    const selectedIndex = e.target.value;

    if (selectedIndex) {
        // Get the selected result from global search results
        const selectedResult = window.searchResults[selectedIndex];

        // Display details in the Details section
        document.getElementById("song-name").textContent = selectedResult["Turku Adi"];
        document.getElementById("artist-detail").textContent = selectedResult["Ozan"];
        document.getElementById("lyrics-detail").textContent = selectedResult["Sozler (tum kitalar tek hucre icinde)"];
    } else {
        // Clear details if no match is selected
        document.getElementById("song-name").textContent = "";
        document.getElementById("artist-detail").textContent = "";
        document.getElementById("lyrics-detail").textContent = "";
    }
});
