/* Optional enhancement. Answers and explanations remain available in HTML. */
(() => {
  "use strict";
  const quiz = document.querySelector("[data-quiz]");
  if (!quiz) return;
  const questions = Array.from(quiz.querySelectorAll("[data-question]"));
  const results = new Map();
  const progress = quiz.querySelector("#quiz-progress");
  const finish = quiz.querySelector("[data-finish]");
  const score = quiz.querySelector("[data-score]");
  const completion = quiz.querySelector("[data-completion]");
  document.querySelectorAll(".js-only").forEach((element) => {
    if (element !== finish) element.hidden = false;
  });
  const hint = document.querySelector(".no-js-hint");
  if (hint) hint.textContent = "Choose an answer, then check your thinking. You can also reveal any explanation directly. No timer, no account, no need to rush.";

  function updateProgress() {
    progress.textContent = `${results.size} of ${questions.length} questions checked.`;
    if (results.size === questions.length) {
      const correct = Array.from(results.values()).filter(Boolean).length;
      score.textContent = `You answered ${correct} of ${questions.length} correctly.`;
      finish.hidden = false;
      completion.textContent = `Mission complete. ${score.textContent}`;
    } else {
      completion.textContent = "";
    }
  }

  questions.forEach((question) => {
    const check = question.querySelector("[data-check]");
    const feedback = question.querySelector("[data-feedback]");
    const explanation = question.querySelector("details");
    check.addEventListener("click", () => {
      const selected = question.querySelector("input:checked");
      if (!selected) {
        feedback.textContent = "Choose an answer first, or reveal the explanation below.";
        question.querySelector("input").focus();
        return;
      }
      const correct = selected.value === question.dataset.answer;
      feedback.textContent = correct
        ? "Correct. Here’s the interesting part…"
        : `Good question to learn from. The answer is ${question.dataset.answer}; here’s why.`;
      results.set(question.id, correct);
      explanation.open = true;
      updateProgress();
    });
    question.querySelectorAll("input").forEach((input) => {
      input.addEventListener("change", () => {
        if (!results.has(question.id)) return;
        results.delete(question.id);
        feedback.textContent = "Answer changed. Check it when you’re ready.";
        finish.hidden = true;
        score.textContent = "";
        updateProgress();
      });
    });
  });

  quiz.querySelector("[data-reset]").addEventListener("click", () => {
    results.clear();
    questions.forEach((question) => {
      question.querySelectorAll("input").forEach((input) => { input.checked = false; });
      question.querySelector("[data-feedback]").textContent = "";
      question.querySelector("details").open = false;
    });
    finish.hidden = true;
    score.textContent = "";
    updateProgress();
    questions[0].querySelector("input").focus();
  });
})();
