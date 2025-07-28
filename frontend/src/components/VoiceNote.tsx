import React, { useState, useRef, useEffect } from 'react';

interface VoiceNoteProps {
  transactionId?: number;
  onUploadSuccess?: () => void;
}

const VoiceNote: React.FC<VoiceNoteProps> = ({ transactionId, onUploadSuccess }) => {
  const [recording, setRecording] = useState(false);
  const [audioURL, setAudioURL] = useState<string | null>(null);
  const [audioBlob, setAudioBlob] = useState<Blob | null>(null);
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const audioChunksRef = useRef<Blob[]>([]);

  useEffect(() => {
    if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
      alert('Your browser does not support audio recording.');
    }
  }, []);

  const startRecording = async () => {
    if (!navigator.mediaDevices) return;
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    mediaRecorderRef.current = new MediaRecorder(stream);
    audioChunksRef.current = [];

    mediaRecorderRef.current.ondataavailable = (event) => {
      audioChunksRef.current.push(event.data);
    };

    mediaRecorderRef.current.onstop = () => {
      const blob = new Blob(audioChunksRef.current, { type: 'audio/webm' });
      setAudioBlob(blob);
      const url = URL.createObjectURL(blob);
      setAudioURL(url);
    };

    mediaRecorderRef.current.start();
    setRecording(true);
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current && recording) {
      mediaRecorderRef.current.stop();
      setRecording(false);
    }
  };

  const uploadAudio = async () => {
    if (!audioBlob) return;
    const formData = new FormData();
    formData.append('file', audioBlob, 'voice_note.webm');
    if (transactionId) {
      formData.append('transaction_id', transactionId.toString());
    }

    try {
      const token = localStorage.getItem('token');
      const response = await fetch('https://finlogix-e0jc.onrender.com/audio/upload', {
        method: 'POST',
        body: formData,
        headers: {
          Authorization: token ? `Bearer ${token}` : '',
        },
        credentials: 'include',
      });
      console.log('Upload response status:', response.status);
      const responseText = await response.text();
      console.log('Upload response text:', responseText);
      if (response.ok) {
        alert('Audio uploaded successfully!');
        setAudioBlob(null);
        setAudioURL(null);
        if (onUploadSuccess) {
          onUploadSuccess();
        }
      } else {
        alert('Failed to upload audio: ' + responseText);
      }
    } catch (error) {
      alert('Error uploading audio: ' + error);
    }
  };

  return (
    <div>
      <h3>Voice Note</h3>
      {!recording && <button onClick={startRecording}>Start Recording</button>}
      {recording && <button onClick={stopRecording}>Stop Recording</button>}
      {audioURL && (
        <div>
          <audio src={audioURL} controls />
          <button onClick={uploadAudio}>Upload Voice Note</button>
        </div>
      )}
    </div>
  );
};

export default VoiceNote;
