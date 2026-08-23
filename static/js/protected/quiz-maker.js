function QuizMaker() {
  return {
    quizId: null,
    loading: true,
    quizData: null,
    saving: false,
    deleting: false,
    nextQuestionId: 0,

    init() {
      this.$watch("quizMakerVars.openQuizId", async (id) => {
        if (!id) return;

        this.quizId = id;
        console.log("Quiz opened:", this.quizId);

        await this.fetchQuiz();
      });
    },

    async fetchQuiz() {
      this.loading = true;

      const response = await fetch(`/quiz/${this.quizId}`);

      if (!response.ok) {
        throw new Error("Failed to fetch quiz");
      }

      this.quizData = await response.json();
      this.quizData.questions = (this.quizData.questions || []).map(
        (question) => ({ ...question, clientId: `question-${question.id}` }),
      );
      this.loading = false;
      this.$nextTick(() => {
        if (window.lucide) lucide.createIcons();
      });
    },

    addQuestion() {
      this.quizData.questions.push({
        clientId: `new-question-${this.nextQuestionId++}`,
        id: null,
        prompt: "",
        question_type: "free_text",
        order_index: this.quizData.questions.length,
        options: null,
        preferences: {},
      });
      this.$nextTick(() => {
        if (window.lucide) lucide.createIcons();
      });
    },

    deleteQuestion(index) {
      this.quizData.questions.splice(index, 1);
      this.updateQuestionOrder();
    },

    moveQuestion(index, direction) {
      const destination = index + direction;

      if (destination < 0 || destination >= this.quizData.questions.length) return;

      const [question] = this.quizData.questions.splice(index, 1);
      this.quizData.questions.splice(destination, 0, question);
      this.updateQuestionOrder();
    },

    updateQuestionOrder() {
      this.quizData.questions.forEach((question, index) => {
        question.order_index = index;
      });
    },

    async saveQuiz() {
      this.saving = true;

      try {
        const response = await fetch(`/quiz/${this.quizId}`, {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            title: this.quizData.title,
            description: this.quizData.description,
            preferences: this.quizData.preferences,
            banner_image: this.quizData.banner_image,
            visibility: this.quizData.visibility,
            questions: this.quizData.questions.map((question) => ({
              id: question.id,
              prompt: question.prompt,
            })),
          }),
        });

        const data = await response.json();

        if (!response.ok) {
          throw new Error(data.detail || "Failed to save quiz");
        }

        this.quizData.questions = data.questions.map((question, index) => ({
          ...this.quizData.questions[index],
          ...question,
        }));
        console.log("Quiz saved:", data.id);
      } catch (error) {
        console.error("Failed to save quiz:", error);
      } finally {
        this.saving = false;
      }
    },

    async deleteQuiz() {
      if (!window.confirm("Delete this quiz? This cannot be undone.")) return;

      this.deleting = true;

      try {
        const response = await fetch(`/quiz/${this.quizId}`, {
          method: "DELETE",
        });
        const data = await response.json();

        if (!response.ok) {
          throw new Error(data.detail || "Failed to delete quiz");
        }

        this.$dispatch("quiz-deleted", { quizId: this.quizId });
        this.quizMakerVars.closeQuizMaker();
        this.quizMakerVars.openQuizId = null;
        this.quizId = null;
        this.quizData = null;
      } catch (error) {
        console.error("Failed to delete quiz:", error);
      } finally {
        this.deleting = false;
      }
    },
  };
}
