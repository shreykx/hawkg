function Dashboard() {
  return {
    profileMenuOpen: false,
    settingsOpen: false,
    async createQuiz() {
      try {
        const response = await fetch("/quiz/quizzes", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            title: "Untitled Quiz",
          }),
        });

        const data = await response.json();

        if (!response.ok) {
          throw new Error(data.detail || "Failed to create quiz");
        }

        this.quizMakerVars.openQuizId = data.id;
        console.log(this.quizMakerVars.openQuizId);
        
        this.quizMakerVars.quizMakerOpen = true;

        await this.fetchQuizzes();
      } catch (error) {
        console.error("Failed to create quiz:", error);
      }
    },
    quizMakerVars: {
      quizMakerOpen: false,
      openQuizId: null,
      openQuizMaker() {
        this.quizMakerOpen = true;
      },

      closeQuizMaker() {
        this.quizMakerOpen = false;
      },
    },
    settingsVars: {
      selectedSection: "account",

      sections: [
        { id: "account", label: "Account" },
        { id: "appearance", label: "Appearance" },
        { id: "security", label: "Security" },
        { id: "shortcuts", label: "(KBD) Shortcuts" },
      ],
      shortcuts: [
        { id: "search", label: "Search", keys: ["Ctrl", "K"] },
        {
          id: "settings",
          label: "Open settings",
          keys: ["Ctrl", "Shift", "I"],
        },
        {
          id: "previous",
          label: "Previous section",
          keys: ["Ctrl", "Alt", "↑"],
        },
        {
          id: "next",
          label: "Next section",
          keys: ["Ctrl", "Alt", "↓"],
        },
        {
          id: "escape",
          label: "Close / unfocus",
          keys: ["Esc"],
        },
        {
          id: "quiz-maker",
          label: "Open quiz maker",
          keys: ["Ctrl", "Alt", "N"],
        },
      ],

      socialSettings: {},
      appearanceSettings: {},
      securitySettings: {},
    },

    openSettings() {
      this.quizMakerVars.quizMakerOpen = false;
      this.settingsOpen = true;
    },

    quizDashSection: {
      quizzes: [],
    },

    init() {
      this.$watch("profileMenuOpen", (open) => {
        if (open) {
          this.$nextTick(() => {
            if (window.lucide) lucide.createIcons();
          });
        }
      });

      this.fetchQuizzes();
    },
    async fetchQuizzes() {
      try {
        const response = await fetch("/quiz/quizzes");
        const data = await response.json();
    
        if (!response.ok) {
          throw new Error("Failed to fetch quizzes");
        }
    
        this.quizDashSection.quizzes = data;
    
        this.$nextTick(() => {
          if (window.lucide) {
            lucide.createIcons();
          }
        });
      } catch (error) {
        console.error("Failed to fetch quizzes:", error);
      }
    },

    removeQuiz(quizId) {
      this.quizDashSection.quizzes = this.quizDashSection.quizzes.filter(
        (quiz) => quiz.id !== quizId,
      );
    },

    toggleProfileMenu() {
      this.profileMenuOpen = !this.profileMenuOpen;
    },
    
    openQuiz(quizId) {
      this.quizMakerVars.openQuizId = quizId;
      this.quizMakerVars.quizMakerOpen = true;
    },

    changeSection(direction) {
      const sections = this.settingsVars.sections;

      const currentIndex = sections.findIndex(
        (s) => s.id === this.settingsVars.selectedSection,
      );

      let newIndex = currentIndex + direction;

      if (newIndex < 0) {
        newIndex = sections.length - 1;
      }

      if (newIndex >= sections.length) {
        newIndex = 0;
      }

      this.settingsVars.selectedSection = sections[newIndex].id;
    },

    timeAgo(timestamp) {
      const seconds = Math.floor(
        (Date.now() - new Date(timestamp).getTime()) / 1000,
      );

      if (seconds < 60) return `${seconds}s ago`;

      const minutes = Math.floor(seconds / 60);
      if (minutes < 60) return `${minutes}m ago`;

      const hours = Math.floor(minutes / 60);
      if (hours < 24) return `${hours}h ago`;

      const days = Math.floor(hours / 24);
      if (days < 30) return `${days}d ago`;

      const months = Math.floor(days / 30);
      if (months < 12) return `${months}mo ago`;

      const years = Math.floor(months / 12);
      return `${years}y ago`;
    },

    formatDate(timestamp) {
      return new Date(timestamp).toLocaleDateString("en-GB", {
        day: "numeric",
        month: "short",
        year: "numeric",
      });
    },
  };
}
