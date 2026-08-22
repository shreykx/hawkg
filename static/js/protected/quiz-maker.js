function QuizMaker(quizId) {
  return {
    quizId,
    loading: true,
    error: null,
    quizData: null,

    init() {
      this.fetchQuiz();
    },

    async fetchQuiz() {
      try {
        this.loading = true;
        this.error = null;

        const response = await fetch(`/quiz/${this.quizId}`);

        if (response.status === 404) {
          this.error = "Quiz not found.";
          return;
        }

        if (!response.ok) {
          throw new Error("Failed to load quiz");
        }

        this.quizData = await response.json();
      } catch (error) {
        console.error("Failed to fetch quiz:", error);
        this.error = "Something went wrong while loading the quiz.";
      } finally {
        this.loading = false;
      }
    },
  };
}