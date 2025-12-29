const input = document.getElementById("queryInput");
const form = document.getElementById("query-form");
const statusEl = document.getElementById("status");
const results = document.getElementById("results");

let lastQuery = "";

// Disable input while processing
function setLoading(isLoading) {
  input.disabled = isLoading;
}

// Show status message
function showStatus(text) {
  statusEl.textContent = text;
  statusEl.classList.remove("hidden");
  results.classList.add("hidden"); // hide previous results
}

// Render result cards
function renderResultCards(result) {
  results.innerHTML = "";
  results.classList.remove("hidden");
  results.classList.add("show");
  statusEl.classList.add("hidden"); 

  Object.entries(result).forEach(([key, value],index) => {
    const card = document.createElement("div");
    card.className = "result-card";

  

    const title = document.createElement("div");
    title.className = "result-title";
    title.textContent = key.replace(/_/g, " ");

    const val = document.createElement("div");
    val.className = "result-value";
    val.textContent = value;

    card.append(title, val);
    results.appendChild(card);

    setTimeout(() => card.classList.add("show"), index * 50);
  });
}

// Clear messages/results when typing
input.addEventListener("input", () => {
  statusEl.classList.add("hidden");
  results.classList.add("hidden");
  results.innerHTML = "";
});

// Handle form submit
form.addEventListener("submit", async (e) => {
  e.preventDefault();
  const query = input.value.trim();
  lastQuery = query;

  if (!query) {
    showStatus("Please enter a query.");
    return;
  }

  setLoading(true);
  showStatus("Thinking…");

  try {
    const response = await fetch("http://127.0.0.1:8000/query", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query })
    });

    if (!response.ok) {
      throw new Error(`Server error: ${response.statusEl}`);
    }

    const data = await response.json();
    console.log(data);

    // Backend asks for location
    if (data.status === "NEED_LOCATION") {
      showStatus(
        "I need your location to answer this. Asking for permission…"
      );
      requestLocation();
      return;
    }

    // Backend returns message (error/info)
    if (data.message) {
      showStatus(data.message);
      setLoading(false);
      return;
    }

    // Backend returns result data
    if (data.result) {
      renderResultCards(data.result);
      setLoading(false);
      return;
    }

    // Unexpected response
    showStatus("I couldn’t understand the response.");
    setLoading(false);

  } catch (error) {
    console.error(error);
    showStatus("Something went wrong. Please try again.");
    setLoading(false);
  }
});

// Request location if needed
function requestLocation() {
  if (!navigator.geolocation) {
    showStatus("Location is not supported. Please mention a city.");
    setLoading(false);
    return;
  }

  navigator.geolocation.getCurrentPosition(
    async (position) => {
      showStatus("Fetching data using your location…");
      setLoading(true);

      try {
        const response = await fetch(
          "http://127.0.0.1:8000/weather-by-location",
          {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
              latitude: position.coords.latitude,
              longitude: position.coords.longitude
            })
          }
        );

        if (!response.ok) {
          throw new Error("Location request failed");
        }

        const result = await response.json();
        renderResultCards(result.result);
      } catch (err) {
        console.error(err);
        showStatus("Failed to fetch data using location.");
      } finally {
        setLoading(false);
      }
    },
    () => {
      showStatus(
        "Location access denied. Please specify a city name instead."
      );
      setLoading(false);
    }
  );
}

















