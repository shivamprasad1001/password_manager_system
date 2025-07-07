function copyToClipboard(text) {
    // Create a temporary input element
    const tempInput = document.createElement("input");
    tempInput.value = text;
    document.body.appendChild(tempInput);
    tempInput.select();
    try {
        // Copy the text to the clipboard
        document.execCommand("copy");
        alert("Copied to clipboard: " + text);
    } catch (err) {
        console.error("Failed to copy:", err);
        alert("Failed to copy text. Please try again.");
    } finally {
        // Clean up
        document.body.removeChild(tempInput);
    }
}