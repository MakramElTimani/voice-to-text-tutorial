let recorder;
let audioStream;

// Get access to the microphone
async function startRecording() {
  audioStream = await navigator.mediaDevices.getUserMedia({ audio: true });
  const audioContext = new AudioContext();
  const input = audioContext.createMediaStreamSource(audioStream);
  recorder = new Recorder(input, { numChannels: 1 });
  recorder.record();
}

function stopRecording() {
  recorder.stop();
  recorder.exportWAV((blob) => {
    // Create an MP3 file from the recorded WAV blob
    const formData = new FormData();
    formData.append("file", blob, "audio.mp3");

    // Send the MP3 file to the backend
    fetch("http://127.0.0.1:8000/transcribe-audio/", {
      method: "POST",
      body: formData,
    })
      .then((response) => response.json())
      .then((data) => {
        document.getElementById("transcriptionText").innerText =
          data.transcribed_text;
        document.getElementById("language").innerText = data.lang;
      })
      .catch((err) => console.error(err));
  });
}

document.getElementById("startBtn").onclick = function () {
  startRecording();
  document.getElementById("startBtn").disabled = true;
  document.getElementById("stopBtn").disabled = false;
};

document.getElementById("stopBtn").onclick = function () {
  stopRecording();
  document.getElementById("startBtn").disabled = false;
  document.getElementById("stopBtn").disabled = true;
};
