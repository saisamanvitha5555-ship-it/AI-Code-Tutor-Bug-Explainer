document.addEventListener("DOMContentLoaded", function () {

    console.log("AI Code Tutor JavaScript loaded.");

    const codeEditor = document.getElementById("codeEditor");
    const languageSelect = document.getElementById("language");

    const clearBtn = document.getElementById("clearBtn");
    const sampleBtn = document.getElementById("sampleBtn");
    const analyzeBtn = document.getElementById("analyzeBtn");
    const runBtn = document.getElementById("runBtn");
    const explainBtn = document.getElementById("explainBtn");

    const analysisContent =
        document.getElementById("analysisContent");

    const output =
        document.getElementById("output");

    const historyContent =
        document.getElementById("historyContent");

    const refreshHistoryBtn =
        document.getElementById("refreshHistoryBtn");

    const chatMessages =
        document.getElementById("chatMessages");

    const chatInput =
        document.getElementById("chatInput");

    const sendChatBtn =
        document.getElementById("sendChatBtn");

    const tutorMode =
        document.getElementById("tutorMode");

    const editorFile =
        document.querySelector(".editor-file");

    const readyStatus =
        document.querySelector(".ready-status span");


    // =========================================================
    // SAMPLE PROGRAMS
    // =========================================================

    const sampleCodes = {

        python:
`def add(a, b):
    return a + b

result = add(10, 20)
print(result)`,

        c:
`#include <stdio.h>

int main() {
    int a = 10;
    int b = 20;

    int result = a + b;

    printf("%d\\n", result);

    return 0;
}`,

        cpp:
`#include <iostream>
using namespace std;

int main() {
    int a = 10;
    int b = 20;

    int result = a + b;

    cout << result << endl;

    return 0;
}`,

        java:
`public class Main {
    public static void main(String[] args) {

        int a = 10;
        int b = 20;

        int result = a + b;

        System.out.println(result);
    }
}`,

        javascript:
`function add(a, b) {
    return a + b;
}

let result = add(10, 20);

console.log(result);`
    };


    // =========================================================
    // FILE NAMES
    // =========================================================

    const fileNames = {
        python: "main.py",
        c: "main.c",
        cpp: "main.cpp",
        java: "Main.java",
        javascript: "main.js"
    };


    // =========================================================
    // HELPER FUNCTIONS
    // =========================================================

    function getCode() {

        if (!codeEditor) {
            return "";
        }

        return codeEditor.value;
    }


    function setCode(code) {

        if (!codeEditor) {
            return;
        }

        codeEditor.value = code;

        codeEditor.focus();

        codeEditor.selectionStart =
            codeEditor.value.length;

        codeEditor.selectionEnd =
            codeEditor.value.length;
    }


    function setStatus(message) {

        if (readyStatus) {
            readyStatus.textContent = message;
        }
    }


    function escapeHtml(text) {

        if (text === null || text === undefined) {
            return "";
        }

        return String(text)
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");
    }


    function updateFileName() {

        if (!languageSelect || !editorFile) {
            return;
        }

        const language = languageSelect.value;

        editorFile.textContent =
            fileNames[language] || "main.code";
    }


    function resetAnalysis() {

        if (!analysisContent) {
            return;
        }

        analysisContent.innerHTML = `
            <div class="empty-state">
                <div class="empty-icon">✦</div>
                <h3>Ready to Analyze</h3>
                <p>
                    Write some code and click
                    <strong>Analyze Code</strong>
                    to get AI-powered feedback.
                </p>
            </div>
        `;
    }


    function resetOutput() {

        if (!output) {
            return;
        }

        output.innerHTML = `
            <div class="output-empty">
                Run your program to see the output here.
            </div>
        `;
    }


    function showAnalysis(text) {

        if (!analysisContent) {
            return;
        }

        analysisContent.innerHTML = `
            <div class="analysis-result">
                <pre>${escapeHtml(text)}</pre>
            </div>
        `;
    }


    function showOutput(text, success) {

        if (!output) {
            return;
        }

        const className =
            success ? "output-success" : "output-error";

        output.innerHTML = `
            <div class="${className}">
                <pre>${escapeHtml(text)}</pre>
            </div>
        `;
    }


    // =========================================================
    // LANGUAGE CHANGE
    // =========================================================

    if (languageSelect) {

        languageSelect.addEventListener(
            "change",
            function () {

                setCode("");

                updateFileName();

                resetAnalysis();

                resetOutput();

                setStatus("Ready");
            }
        );
    }


    // =========================================================
    // SAMPLE CODE
    // =========================================================

    if (sampleBtn) {

        sampleBtn.addEventListener(
            "click",
            function () {

                const language =
                    languageSelect.value;

                const sample =
                    sampleCodes[language];

                if (!sample) {

                    alert(
                        "Sample code is not available for this language."
                    );

                    return;
                }

                setCode(sample);

                updateFileName();

                resetAnalysis();

                resetOutput();

                setStatus("Sample loaded");

                console.log(
                    "Sample code loaded:",
                    language
                );
            }
        );
    }


    // =========================================================
    // CLEAR
    // =========================================================

    if (clearBtn) {

        clearBtn.addEventListener(
            "click",
            function () {

                setCode("");

                resetAnalysis();

                resetOutput();

                setStatus("Ready");
            }
        );
    }


    // =========================================================
    // ANALYZE CODE
    // =========================================================

    if (analyzeBtn) {

        analyzeBtn.addEventListener(
            "click",
            async function () {

                const code = getCode();

                const language =
                    languageSelect.value;

                if (!code.trim()) {

                    alert(
                        "Please write some code first."
                    );

                    return;
                }

                analyzeBtn.disabled = true;
                analyzeBtn.textContent = "Analyzing...";

                setStatus("Analyzing...");

                try {

                    const response =
                        await fetch("/analyze", {

                            method: "POST",

                            headers: {
                                "Content-Type":
                                    "application/json"
                            },

                            body: JSON.stringify({
                                code: code,
                                language: language
                            })
                        });


                    const data =
                        await response.json();


                    if (!response.ok ||
                        data.success === false) {

                        throw new Error(
                            data.error ||
                            "Analysis failed."
                        );
                    }


                    showAnalysis(
                        data.analysis ||
                        "No analysis returned."
                    );

                    setStatus(
                        "Analysis complete"
                    );

                    loadHistory();

                } catch (error) {

                    console.error(
                        "Analyze error:",
                        error
                    );

                    showAnalysis(
                        "Error: " + error.message
                    );

                    setStatus(
                        "Analysis failed"
                    );

                } finally {

                    analyzeBtn.disabled = false;

                    analyzeBtn.textContent =
                        "✦ Analyze Code";
                }
            }
        );
    }


    // =========================================================
    // RUN CODE
    // =========================================================

    if (runBtn) {

        runBtn.addEventListener(
            "click",
            async function () {

                const code = getCode();

                const language =
                    languageSelect.value;

                if (!code.trim()) {

                    alert(
                        "Please write some code first."
                    );

                    return;
                }

                runBtn.disabled = true;
                runBtn.textContent = "Running...";

                setStatus("Running...");

                try {

                    const response =
                        await fetch("/run", {

                            method: "POST",

                            headers: {
                                "Content-Type":
                                    "application/json"
                            },

                            body: JSON.stringify({
                                code: code,
                                language: language
                            })
                        });


                    const data =
                        await response.json();


                    if (data.success) {

                        showOutput(
                            data.output ||
                            "Program executed successfully.",
                            true
                        );

                        setStatus(
                            "Program finished"
                        );

                    } else {

                        let errorText =
                            data.output ||
                            data.error ||
                            "Program execution failed.";

                        showOutput(
                            errorText,
                            false
                        );

                        if (data.ai_explanation) {

                            showAnalysis(
                                data.ai_explanation
                            );
                        }

                        setStatus(
                            "Program has an error"
                        );
                    }

                } catch (error) {

                    console.error(
                        "Run error:",
                        error
                    );

                    showOutput(
                        "Error: " + error.message,
                        false
                    );

                    setStatus(
                        "Execution failed"
                    );

                } finally {

                    runBtn.disabled = false;

                    runBtn.textContent =
                        "▶ Run Code";
                }
            }
        );
    }


    // =========================================================
    // EXPLAIN CODE
    // =========================================================

    if (explainBtn) {

        explainBtn.addEventListener(
            "click",
            async function () {

                const code = getCode();

                const language =
                    languageSelect.value;

                if (!code.trim()) {

                    alert(
                        "Please write some code first."
                    );

                    return;
                }

                explainBtn.disabled = true;

                explainBtn.textContent =
                    "Explaining...";

                setStatus(
                    "Generating explanation..."
                );

                try {

                    const response =
                        await fetch(
                            "/explain-line-by-line",
                            {
                                method: "POST",

                                headers: {
                                    "Content-Type":
                                        "application/json"
                                },

                                body: JSON.stringify({
                                    code: code,
                                    language: language
                                })
                            }
                        );


                    const data =
                        await response.json();


                    if (!response.ok ||
                        data.success === false) {

                        throw new Error(
                            data.error ||
                            "Explanation failed."
                        );
                    }


                    showAnalysis(
                        data.explanation ||
                        "No explanation returned."
                    );

                    setStatus(
                        "Explanation complete"
                    );

                } catch (error) {

                    console.error(
                        "Explain error:",
                        error
                    );

                    showAnalysis(
                        "Error: " + error.message
                    );

                    setStatus(
                        "Explanation failed"
                    );

                } finally {

                    explainBtn.disabled = false;

                    explainBtn.textContent =
                        "Explain Code";
                }
            }
        );
    }


    // =========================================================
    // HISTORY
    // =========================================================

    async function loadHistory() {

        if (!historyContent) {
            return;
        }

        try {

            const response =
                await fetch("/history");

            const data =
                await response.json();


            if (!response.ok ||
                data.success === false) {

                throw new Error(
                    data.error ||
                    "Could not load history."
                );
            }


            const history =
                data.history || [];


            if (history.length === 0) {

                historyContent.innerHTML = `
                    <div class="empty-state">
                        <div class="empty-icon">◷</div>
                        <h3>No History Yet</h3>
                        <p>
                            Your analyzed programs
                            will appear here.
                        </p>
                    </div>
                `;

                return;
            }


            historyContent.innerHTML =
                history.map(function (item) {

                    return `
                        <div
                            class="history-item"
                            data-id="${item.id}"
                        >

                            <div class="history-details">

                                <div class="history-top">

                                    <strong>
                                        ${escapeHtml(
                                            item.language
                                        )}
                                    </strong>

                                    <span>
                                        ${escapeHtml(
                                            item.created_at
                                        )}
                                    </span>

                                </div>

                                <pre>${escapeHtml(
                                    item.code
                                )}</pre>

                            </div>

                            <div class="history-actions">

                                <button
                                    type="button"
                                    class="btn btn-secondary history-load"
                                    data-id="${item.id}"
                                >
                                    Load
                                </button>

                                <button
                                    type="button"
                                    class="btn btn-danger history-delete"
                                    data-id="${item.id}"
                                >
                                    Delete
                                </button>

                            </div>

                        </div>
                    `;

                }).join("");


        } catch (error) {

            console.error(
                "History error:",
                error
            );

            historyContent.innerHTML = `
                <div class="empty-state">
                    <h3>Unable to Load History</h3>
                    <p>
                        ${escapeHtml(
                            error.message
                        )}
                    </p>
                </div>
            `;
        }
    }


    // =========================================================
    // HISTORY CLICK EVENTS
    // =========================================================

    if (historyContent) {

        historyContent.addEventListener(
            "click",
            async function (event) {

                const loadButton =
                    event.target.closest(
                        ".history-load"
                    );

                const deleteButton =
                    event.target.closest(
                        ".history-delete"
                    );


                // -----------------------------
                // LOAD HISTORY
                // -----------------------------

                if (loadButton) {

                    const id =
                        loadButton.dataset.id;

                    try {

                        const response =
                            await fetch("/history");

                        const data =
                            await response.json();

                        const item =
                            (data.history || [])
                                .find(function (record) {
                                    return String(record.id)
                                        === String(id);
                                });


                        if (!item) {
                            alert(
                                "History record not found."
                            );
                            return;
                        }


                        languageSelect.value =
                            item.language;

                        updateFileName();

                        setCode(item.code);

                        if (item.analysis) {

                            showAnalysis(
                                item.analysis
                            );
                        }

                        setStatus(
                            "History loaded"
                        );

                        document
                            .getElementById("workspace")
                            .scrollIntoView({
                                behavior: "smooth"
                            });

                    } catch (error) {

                        alert(
                            "Could not load history."
                        );
                    }

                    return;
                }


                // -----------------------------
                // DELETE HISTORY
                // -----------------------------

                if (deleteButton) {

                    const id =
                        deleteButton.dataset.id;


                    const confirmed =
                        confirm(
                            "Delete this history record?"
                        );


                    if (!confirmed) {
                        return;
                    }


                    try {

                        const response =
                            await fetch(
                                "/history/" + id,
                                {
                                    method: "DELETE"
                                }
                            );


                        const data =
                            await response.json();


                        if (!response.ok ||
                            data.success === false) {

                            throw new Error(
                                data.error ||
                                "Delete failed."
                            );
                        }


                        loadHistory();

                    } catch (error) {

                        alert(
                            "Could not delete history: " +
                            error.message
                        );
                    }
                }
            }
        );
    }


    if (refreshHistoryBtn) {

        refreshHistoryBtn.addEventListener(
            "click",
            function () {

                loadHistory();

                setStatus(
                    "History refreshed"
                );
            }
        );
    }


    // =========================================================
    // AI TUTOR
    // =========================================================

    async function sendTutorQuestion(question) {

        if (!question.trim()) {
            return;
        }


        const code = getCode();

        const language =
            languageSelect.value;

        const tutor_mode =
            tutorMode.value;


        // Show user message

        const userMessage =
            document.createElement("div");

        userMessage.className =
            "chat-message user-message";

        userMessage.innerHTML = `
            <div class="message-content">
                <p>
                    ${escapeHtml(question)}
                </p>
            </div>
        `;

        chatMessages.appendChild(
            userMessage
        );


        chatInput.value = "";

        chatMessages.scrollTop =
            chatMessages.scrollHeight;


        sendChatBtn.disabled = true;

        try {

            const response =
                await fetch("/ask-ai", {

                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({

                        code: code,

                        language: language,

                        question: question,

                        tutor_mode: tutor_mode
                    })
                });


            const data =
                await response.json();


            if (!response.ok ||
                data.success === false) {

                throw new Error(
                    data.error ||
                    "AI Tutor request failed."
                );
            }


            const aiMessage =
                document.createElement("div");

            aiMessage.className =
                "chat-message ai-message";

            aiMessage.innerHTML = `
                <div class="message-avatar">
                    AI
                </div>

                <div class="message-content">
                    <p>
                        ${escapeHtml(
                            data.answer ||
                            "No answer returned."
                        )}
                    </p>
                </div>
            `;

            chatMessages.appendChild(
                aiMessage
            );


            chatMessages.scrollTop =
                chatMessages.scrollHeight;


        } catch (error) {

            const errorMessage =
                document.createElement("div");

            errorMessage.className =
                "chat-message ai-message";

            errorMessage.innerHTML = `
                <div class="message-avatar">
                    AI
                </div>

                <div class="message-content">
                    <p>
                        Error:
                        ${escapeHtml(
                            error.message
                        )}
                    </p>
                </div>
            `;

            chatMessages.appendChild(
                errorMessage
            );

        } finally {

            sendChatBtn.disabled = false;
        }
    }


    if (sendChatBtn) {

        sendChatBtn.addEventListener(
            "click",
            function () {

                sendTutorQuestion(
                    chatInput.value
                );
            }
        );
    }


    if (chatInput) {

        chatInput.addEventListener(
            "keydown",
            function (event) {

                if (
                    event.key === "Enter" &&
                    !event.shiftKey
                ) {

                    event.preventDefault();

                    sendTutorQuestion(
                        chatInput.value
                    );
                }
            }
        );
    }


    // =========================================================
    // INITIAL SETUP
    // =========================================================

    updateFileName();

    setCode("");

    resetAnalysis();

    resetOutput();

    loadHistory();

    setStatus("Ready");

    console.log(
        "AI Code Tutor initialized successfully."
    );

});