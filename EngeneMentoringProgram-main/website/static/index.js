function deleteNote(noteId) {
  fetch("/delete-note", {
    method: "POST",
    body: JSON.stringify({ noteId: noteId }),
  }).then((_res) => {
    window.location.href = "/user";
  });
}

// function toggleNotePrivateness(private, noteId) {
//   fetch("/toggle-note-private", {
//     method: "POST",
//     body: JSON.stringify({ private: private, noteId: noteId }),
//   }).then((_res) => {
//     window.location.href = "/user";
//   });
// }

function toggleNoteStatus(status, noteId) {
  fetch("/toggle-note-status", {
    method: "POST",
    body: JSON.stringify({ status: status, noteId: noteId }),
  }).then((_res) => {
    window.location.href = "/admin";
  });
}