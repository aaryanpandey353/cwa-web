const codeEditor = CodeMirror.fromTextArea(document.getElementById('code-editor'), {
    lineNumbers: true,
    mode: 'python',
});

const runButton = document.getElementById('run-button');
const outputElement = document.getElementById('output');

runButton.addEventListener('click', () => {
    const code = codeEditor.getValue();

    // Make a request to your Flask backend to execute the code
    fetch('/execute', {
        method: 'POST',
        body: new URLSearchParams({
            code: code,
        }),
    })
        .then(response => response.text())
        .then(output => {
            outputElement.textContent = output;
        });
});
