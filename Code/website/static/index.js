function deleteNote(noteId) {
  fetch("/delete-note", {
    method: "POST",
    body: JSON.stringify({ noteId: noteId }),
  }).then((_res) => {
    window.location.href = "/user";
  });
}

function toggleNote(private, noteId) {
  fetch("/toggle-note", {
    method: "POST",
    body: JSON.stringify({ private: private, noteId: noteId }),
  }).then((_res) => {
    window.location.href = "/user";
  });
}