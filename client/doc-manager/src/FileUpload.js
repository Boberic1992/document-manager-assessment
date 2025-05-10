import React, { useState } from "react";
import axios from "axios";

function FileUpload({ token, onUpload }) {
  const [file, setFile] = useState(null)
  const [error, setError] = useState("")
  const [success, setSuccess] = useState("")
  const defaultPath = "/documents/reviews/review.pdf"

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setSuccess("");
    if (!file) {
      setError("Please select a file.");
      return;
    }
    const formData = new FormData();
    formData.append("file", file);
    formData.append("path", defaultPath);

    try {
      await axios.post("http://localhost:8002/api/file_versions/", formData, {
        headers: {
          Authorization: `Token ${token}`,
          "Content-Type": "multipart/form-data",
        },
      });
      setSuccess("File uploaded successfully!");
      setFile(null);
      if (onUpload) onUpload();
    } catch (err) {
      setError("Upload failed.");
    }
  };

  return (
    <form className="file-upload-form" onSubmit={handleSubmit}>
      <h2>Upload File</h2>
      <div>
        <input
          type="file"
          onChange={e => setFile(e.target.files[0])}
          required
          style={{ marginBottom: "1rem", width: "100%" }}
        />
      </div>
      {error && <div style={{ color: "red" }}>{error}</div>}
      {success && <div style={{ color: "green" }}>{success}</div>}
      <button type="submit">Upload</button>
    </form>
  );
}

export default FileUpload;