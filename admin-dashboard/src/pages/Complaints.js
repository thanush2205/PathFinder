// Complaints page with table and status management
import React, { useState, useEffect } from 'react';
import { complaintsAPI } from '../services/api';
import '../styles/Complaints.css';

function Complaints() {
  const [complaints, setComplaints] = useState([]);
  const [filter, setFilter] = useState('all');
  const [selectedComplaint, setSelectedComplaint] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchComplaints();
  }, [filter]);

  const fetchComplaints = async () => {
    setLoading(true);
    try {
      const data = await complaintsAPI.getAll(filter === 'all' ? null : filter);
      setComplaints(data);
    } catch (err) {
      console.error('Failed to fetch complaints', err);
    } finally {
      setLoading(false);
    }
  };

  const handleStatusChange = async (id, status, response) => {
    try {
      await complaintsAPI.update(id, { status, admin_response: response });
      fetchComplaints();
      setSelectedComplaint(null);
    } catch (err) {
      alert('Failed to update complaint');
    }
  };

  const getStatusBadge = (status) => {
    const colors = { open: 'red', in_progress: 'orange', resolved: 'green', closed: 'gray' };
    return <span className={`status-badge ${colors[status]}`}>{status}</span>;
  };

  return (
    <div className="complaints-page">
      <div className="page-header">
        <h1>Complaints Management</h1>
        <div className="filters">
          {['all', 'open', 'in_progress', 'resolved'].map(f => (
            <button key={f} className={filter === f ? 'active' : ''} onClick={() => setFilter(f)}>
              {f.replace('_', ' ').toUpperCase()}
            </button>
          ))}
        </div>
      </div>

      {loading ? <div className="loading">Loading...</div> : (
        <div className="complaints-table">
          <table>
            <thead>
              <tr>
                <th>ID</th>
                <th>User ID</th>
                <th>Message</th>
                <th>Date</th>
                <th>Status</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {complaints.map(complaint => (
                <tr key={complaint.id}>
                  <td>{complaint.id.substring(0, 8)}</td>
                  <td>{complaint.user_id.substring(0, 8)}</td>
                  <td>{complaint.message.substring(0, 50)}...</td>
                  <td>{new Date(complaint.timestamp).toLocaleDateString()}</td>
                  <td>{getStatusBadge(complaint.status)}</td>
                  <td>
                    <button onClick={() => setSelectedComplaint(complaint)}>View/Update</button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {selectedComplaint && (
        <ComplaintModal
          complaint={selectedComplaint}
          onClose={() => setSelectedComplaint(null)}
          onUpdate={handleStatusChange}
        />
      )}
    </div>
  );
}

function ComplaintModal({ complaint, onClose, onUpdate }) {
  const [status, setStatus] = useState(complaint.status);
  const [response, setResponse] = useState(complaint.admin_response || '');

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={e => e.stopPropagation()}>
        <h2>Complaint Details</h2>
        <p><strong>User:</strong> {complaint.user_id}</p>
        <p><strong>Message:</strong> {complaint.message}</p>
        <p><strong>Date:</strong> {new Date(complaint.timestamp).toLocaleString()}</p>
        
        <div className="form-group">
          <label>Status:</label>
          <select value={status} onChange={e => setStatus(e.target.value)}>
            <option value="open">Open</option>
            <option value="in_progress">In Progress</option>
            <option value="resolved">Resolved</option>
            <option value="closed">Closed</option>
          </select>
        </div>

        <div className="form-group">
          <label>Admin Response:</label>
          <textarea value={response} onChange={e => setResponse(e.target.value)} rows="4" />
        </div>

        <div className="modal-actions">
          <button onClick={() => onUpdate(complaint.id, status, response)}>Update</button>
          <button onClick={onClose}>Cancel</button>
        </div>
      </div>
    </div>
  );
}

export default Complaints;
