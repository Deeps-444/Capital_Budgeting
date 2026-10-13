import { useRef, useState } from "react";
import { extractProjectDocument } from "../services/v2Api";

export default function DocumentUpload({ onExtracted }) {
  const inputRef = useRef(null);
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  function handleFileChange(event) {
    const selected = event.target.files?.[0];

    setError("");
    setFile(null);

    if (!selected) return;

    const allowedExtensions = [".pdf", ".docx", ".txt"];
    const extension = selected.name
      .slice(selected.name.lastIndexOf("."))
      .toLowerCase();

    if (!allowedExtensions.includes(extension)) {
      setError("Please select a PDF, DOCX, or TXT file.");
      event.target.value = "";
      return;
    }

    if (selected.size > 10 * 1024 * 1024) {
      setError("The file must be 10 MB or smaller.");
      event.target.value = "";
      return;
    }

    setFile(selected);
  }

  async function handleUpload() {
    if (!file || loading) return;

    setLoading(true);
    setError("");

    try {
      const result = await extractProjectDocument(file);

      if (!result?.extractedDetails) {
        throw new Error("The API returned no extracted project details.");
      }

      onExtracted(result.extractedDetails);
    } catch (err) {
      setError(
        err.response?.data?.detail ||
          err.message ||
          "Document extraction failed. Please try again.",
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <section className="v2-upload-card">
      <div className="v2-section-heading">
        <span className="v2-step-number">01</span>
        <div>
          <h2>Upload project document</h2>
          <p>Extract project information from an existing proposal.</p>
        </div>
      </div>

      <div
        className="v2-dropzone"
        onClick={() => inputRef.current?.click()}
        onDragOver={(event) => event.preventDefault()}
        onDrop={(event) => {
          event.preventDefault();
          const droppedFile = event.dataTransfer.files?.[0];

          if (droppedFile && inputRef.current) {
            const transfer = new DataTransfer();
            transfer.items.add(droppedFile);
            inputRef.current.files = transfer.files;
            inputRef.current.dispatchEvent(
              new Event("change", { bubbles: true }),
            );
          }
        }}
        role="button"
        tabIndex={0}
        onKeyDown={(event) => {
          if (event.key === "Enter" || event.key === " ") {
            event.preventDefault();
            inputRef.current?.click();
          }
        }}
      >
        <div className="v2-upload-icon">↑</div>
        <strong>Choose a file or drag it here</strong>
        <span>PDF, DOCX, or TXT · Maximum 10 MB</span>

        <input
          ref={inputRef}
          type="file"
          accept=".pdf,.docx,.txt"
          onChange={handleFileChange}
          hidden
        />
      </div>

      {file && (
        <div className="v2-selected-file">
          <div>
            <strong>{file.name}</strong>
            <span>{(file.size / 1024).toFixed(1)} KB</span>
          </div>
          <button
            type="button"
            className="v2-text-button"
            onClick={() => {
              setFile(null);
              if (inputRef.current) inputRef.current.value = "";
            }}
            disabled={loading}
          >
            Remove
          </button>
        </div>
      )}

      {error && (
        <div className="v2-error" role="alert">
          {error}
        </div>
      )}

      <button
        type="button"
        className="v2-primary-button"
        onClick={handleUpload}
        disabled={!file || loading}
      >
        {loading ? "Extracting project details…" : "Extract project details"}
      </button>

      {loading && (
        <p className="v2-helper-text">
          The document is being processed. This may take a little while.
        </p>
      )}
    </section>
  );
}
