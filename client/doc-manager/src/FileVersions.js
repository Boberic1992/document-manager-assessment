
import React, { useState, useEffect } from "react";

import "./FileVersions.css";

function FileVersionsList({ file_versions, onDelete }) {
  const [hoveredId, setHoveredId] = useState(null);
  return file_versions.map((file_version) => (
    <div
      className="file-version"
      key={file_version.id}
      onMouseEnter={() => setHoveredId(file_version.id)}
      onMouseLeave={() => setHoveredId(null)}
      style={{ position: "relative" }}
    >
      <h2>File Name: {file_version.file_name}</h2>
        <p>
          ID: {file_version.id} Version: {file_version.version_number}
        </p>
      <div className="file-version-actions">
        <a
          href={file_version.file}
          target="_blank"
          rel="noopener noreferrer"
          className="download-btn"
        >
          View / Download
        </a>
        <button
          className="delete-btn"
          onClick={() => onDelete(file_version.id)}
        >
          Delete
        </button>
      </div>
      {hoveredId === file_version.id && (
        <div className="file-details-tooltip">
          <strong>ID:</strong> {file_version.id}<br />
          <strong>Version:</strong> {file_version.version_number}<br />
          <strong>Uploaded:</strong> {new Date(file_version.created_at).toLocaleString()}<br />
          <strong>Content Hash:</strong> <span style={{fontFamily: "monospace"}}>{file_version.content_hash}</span>
        </div>
      )}
    </div>
  ));
}
function FileVersions({ token }) {
  const [data, setData] = useState([]);

  useEffect(() => {
    const dataFetch = async () => {
      const response = await fetch("http://localhost:8002/api/file_versions/", {
        headers: {
          Authorization: `Token ${token}`,
        },
      });
      const data = await response.json();
      setData(data);
    };

    dataFetch();
  }, [token]);

  const handleDelete = async (id) => {
    await fetch(`http://localhost:8002/api/file_versions/${id}/`, {
      method: "DELETE",
      headers: {
        Authorization: `Token ${token}`,
      },
    });
    setData(data => data.filter(fv => fv.id !== id));
  };

  return (
    <div>
      <h1>Found {data.length} File Versions</h1>
      <div>
        <FileVersionsList file_versions={data} onDelete={handleDelete} />
      </div>
    </div>
  );
}

export default FileVersions;
