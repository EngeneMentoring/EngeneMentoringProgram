function deleteNote(noteId) {
  fetch("/delete-note", {
    method: "POST",
    body: JSON.stringify({ noteId: noteId }),
  }).then((_res) => {
    window.location.href = "/user";
  });
}

function toggleNotePrivateness(private, noteId) {
  fetch("/toggle-note-private", {
    method: "POST",
    body: JSON.stringify({ private: private, noteId: noteId }),
  }).then((_res) => {
    window.location.href = "/user";
  });
}

function toggleNoteGreenness(green, noteId) {
  fetch("/toggle-note-green", {
    method: "POST",
    body: JSON.stringify({ green: green, noteId: noteId }),
  }).then((_res) => {
    window.location.href = "/admin";
  });
}