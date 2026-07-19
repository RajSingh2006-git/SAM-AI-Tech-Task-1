/* ═══════════════════════════════════════════════════════════════
   Mail Spam Detector — Frontend Logic (AJAX, no page reload)
   ═══════════════════════════════════════════════════════════════ */

document.addEventListener("DOMContentLoaded", () => {
    const textarea    = document.getElementById("email-input");
    const predictBtn  = document.getElementById("predict-btn");
    const clearBtn    = document.getElementById("clear-btn");
    const resultBox   = document.getElementById("result-box");
    const resultIcon  = document.getElementById("result-icon");
    const resultLabel = document.getElementById("result-label");
    const resultConf  = document.getElementById("result-confidence");
    const errorBox    = document.getElementById("error-box");
    const errorText   = document.getElementById("error-text");
    const btnText     = predictBtn.querySelector(".btn-text");
    const btnIcon     = predictBtn.querySelector(".btn-icon");
    const btnLoader   = predictBtn.querySelector(".btn-loader");

    // ── Predict ──────────────────────────────────────────────────
    predictBtn.addEventListener("click", async () => {
        const message = textarea.value.trim();

        // Hide previous results
        hideResult();
        hideError();

        if (!message) {
            showError("Please enter a message to analyze.");
            textarea.focus();
            return;
        }

        // Loading state
        setLoading(true);

        try {
            const response = await fetch("/predict", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ message }),
            });

            const data = await response.json();

            if (!response.ok) {
                showError(data.error || "Something went wrong. Please try again.");
                return;
            }

            showResult(data.prediction, data.confidence);
        } catch (err) {
            showError("Could not reach the server. Make sure Flask is running.");
            console.error(err);
        } finally {
            setLoading(false);
        }
    });

    // ── Clear ────────────────────────────────────────────────────
    clearBtn.addEventListener("click", () => {
        textarea.value = "";
        hideResult();
        hideError();
        textarea.focus();
    });

    // ── Keyboard shortcut: Ctrl/Cmd + Enter ──────────────────────
    textarea.addEventListener("keydown", (e) => {
        if ((e.ctrlKey || e.metaKey) && e.key === "Enter") {
            e.preventDefault();
            predictBtn.click();
        }
    });

    // ── Helpers ──────────────────────────────────────────────────
    function setLoading(isLoading) {
        predictBtn.disabled = isLoading;
        btnText.hidden    = isLoading;
        btnIcon.hidden    = isLoading;
        btnLoader.hidden  = !isLoading;
    }

    function showResult(prediction, confidence) {
        const isHam = prediction === "Ham";

        resultBox.hidden = false;
        resultBox.className = `result-box ${isHam ? "ham" : "spam"}`;

        resultIcon.textContent = isHam ? "✅" : "🚫";
        resultLabel.textContent = isHam
            ? "Safe Message (Ham)"
            : "⚠ Spam Detected";
        resultConf.textContent = `Model confidence: ${confidence}%`;

        // Re-trigger animation
        resultBox.style.animation = "none";
        resultBox.offsetHeight; // force reflow
        resultBox.style.animation = "";
    }

    function hideResult() {
        resultBox.hidden = true;
        resultBox.className = "result-box";
    }

    function showError(msg) {
        errorBox.hidden = false;
        errorText.textContent = msg;

        // Re-trigger shake
        errorBox.style.animation = "none";
        errorBox.offsetHeight;
        errorBox.style.animation = "";
    }

    function hideError() {
        errorBox.hidden = true;
    }
});
