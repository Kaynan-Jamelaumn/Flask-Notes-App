function deleteNote(noteId){
    fetch("/delete-note", {
        method: "POST",
        body: JSON.stringify({ noteId: noteId }),
    }).then((_res) => {
        window.location.href = "/";
    }).catch((err) => console.log(err));
}