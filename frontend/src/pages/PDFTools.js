import React, { useState } from 'react';
import axios from 'axios';

const API_URL = process.env.REACT_APP_BACKEND_URL || '';

function PDFTools() {
  const [selectedTool, setSelectedTool] = useState(null);
  const [uploadedFile, setUploadedFile] = useState(null);
  const [processing, setProcessing] = useState(false);
  const [result, setResult] = useState(null);

  const tools = [
    { id: 'merge', name: 'Merge PDF', icon: '🔗', description: 'Combine multiple PDFs into one' },
    { id: 'split', name: 'Split PDF', icon: '✂️', description: 'Split PDF into separate files' },
    { id: 'compress', name: 'Compress PDF', icon: '🗜️', description: 'Reduce PDF file size' },
    { id: 'rotate', name: 'Rotate PDF', icon: '🔄', description: 'Rotate PDF pages' },
    { id: 'watermark', name: 'Add Watermark', icon: '💧', description: 'Add text watermark to PDF' },
    { id: 'protect', name: 'Protect PDF', icon: '🔒', description: 'Password protect your PDF' },
    { id: 'extract', name: 'Extract Text', icon: '📝', description: 'Extract text from PDF' },
    { id: 'pdf-to-word', name: 'PDF to Word', icon: '📄', description: 'Convert PDF to Word document' },
    { id: 'word-to-pdf', name: 'Word to PDF', icon: '📋', description: 'Convert Word to PDF' },
    { id: 'unlock', name: 'Unlock PDF', icon: '🔓', description: 'Remove PDF password' },
    { id: 'sign', name: 'Sign PDF', icon: '✍️', description: 'Add digital signature' },
    { id: 'ocr', name: 'OCR PDF', icon: '👁️', description: 'Extract text from scanned PDF' }
  ];

  const handleFileUpload = async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);

    try {
      const token = localStorage.getItem('token');
      const response = await axios.post(`${API_URL}/api/pdf-tools/upload`, formData, {
        headers: { 
          Authorization: `Bearer ${token}`,
          'Content-Type': 'multipart/form-data'
        }
      });

      setUploadedFile(response.data);
      alert('PDF uploaded successfully!');
    } catch (error) {
      console.error('Error uploading PDF:', error);
      alert('Failed to upload PDF');
    }
  };

  const processPDF = async (toolId) => {
    if (!uploadedFile) {
      alert('Please upload a PDF first');
      return;
    }

    setProcessing(true);
    setResult(null);

    try {
      const token = localStorage.getItem('token');
      let endpoint = '';
      let payload = {};

      switch(toolId) {
        case 'compress':
          endpoint = '/api/pdf-tools/compress';
          payload = { file_path: uploadedFile.file_path, quality: 'medium' };
          break;
        case 'rotate':
          endpoint = '/api/pdf-tools/rotate';
          payload = { file_path: uploadedFile.file_path, angle: 90, pages: 'all' };
          break;
        case 'watermark':
          endpoint = '/api/pdf-tools/watermark';
          payload = { file_path: uploadedFile.file_path, watermark_text: 'HexaBid' };
          break;
        case 'protect':
          endpoint = '/api/pdf-tools/protect';
          payload = { file_path: uploadedFile.file_path, password: 'hexabid123' };
          break;
        case 'extract':
          endpoint = '/api/pdf-tools/extract-text';
          payload = { file_path: uploadedFile.file_path };
          break;
        default:
          alert('Tool coming soon!');
          setProcessing(false);
          return;
      }

      const response = await axios.post(`${API_URL}${endpoint}`, payload, {
        headers: { Authorization: `Bearer ${token}` }
      });

      setResult(response.data);
    } catch (error) {
      console.error('Error processing PDF:', error);
      alert('Processing failed: ' + (error.response?.data?.error || error.message));
    }

    setProcessing(false);
  };

  return (
    <div className="p-6">
      <div className="mb-6">
        <h1 className="text-3xl font-bold text-gray-800">PDF Tools</h1>
        <p className="text-gray-600 mt-2">20+ powerful PDF tools at your fingertips</p>
      </div>

      {/* Upload Section */}
      <div className="bg-white rounded-lg shadow p-6 mb-6">
        <h2 className="text-xl font-semibold mb-4">Upload PDF</h2>
        <div className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center">
          <input
            type="file"
            accept=".pdf"
            onChange={handleFileUpload}
            className="hidden"
            id="pdf-upload"
          />
          <label htmlFor="pdf-upload" className="cursor-pointer">
            <div className="text-4xl mb-2">📄</div>
            <p className="text-lg font-semibold text-gray-700">Click to upload PDF</p>
            <p className="text-sm text-gray-500 mt-1">or drag and drop</p>
          </label>
        </div>
        {uploadedFile && (
          <div className="mt-4 p-3 bg-green-50 border border-green-200 rounded">
            <p className="text-green-700">✓ {uploadedFile.filename} uploaded ({uploadedFile.info?.num_pages} pages)</p>
          </div>
        )}
      </div>

      {/* Tools Grid */}
      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-xl font-semibold mb-4">Select Tool</h2>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {tools.map(tool => (
            <button
              key={tool.id}
              onClick={() => {
                setSelectedTool(tool.id);
                processPDF(tool.id);
              }}
              disabled={processing}
              className="p-4 border-2 border-gray-200 rounded-lg hover:border-blue-500 hover:shadow-md transition disabled:opacity-50"
            >
              <div className="text-3xl mb-2">{tool.icon}</div>
              <p className="font-semibold text-sm">{tool.name}</p>
              <p className="text-xs text-gray-500 mt-1">{tool.description}</p>
            </button>
          ))}
        </div>
      </div>

      {/* Processing Status */}
      {processing && (
        <div className="mt-6 bg-blue-50 border border-blue-200 rounded-lg p-4">
          <p className="text-blue-700 font-semibold">⏳ Processing your PDF...</p>
        </div>
      )}

      {/* Result */}
      {result && result.success && (
        <div className="mt-6 bg-green-50 border border-green-200 rounded-lg p-6">
          <h3 className="text-lg font-semibold text-green-700 mb-3">✓ Processing Complete</h3>
          <div className="space-y-2 text-sm">
            <p><strong>Status:</strong> {result.message}</p>
            {result.output_file && <p><strong>Output File:</strong> {result.output_file}</p>}
            {result.compression_ratio && <p><strong>Compression:</strong> {result.compression_ratio} size reduction</p>}
            {result.num_pages && <p><strong>Pages:</strong> {result.num_pages}</p>}
          </div>
        </div>
      )}
    </div>
  );
}

export default PDFTools;
