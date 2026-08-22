function Dashboard() {
  return {
    profileMenuOpen: false,
    settingsOpen: false,
    quizMakerVars: {
      quizMakerOpen: true,
      openQuizId: 12,
      selectedViewport: "build",

      quizData: {
        visibility: "unlisted",
      },

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
      quizzes: [
        {
          id: 1,
          created_at: "2026-08-01T09:15:00Z",
          updated_at: "2026-08-02T14:20:00Z",
          title: "Team Culture Pulse Check",
          description:
            "A quick pulse survey on team culture and communication.",
          created_by: 1,
          banner_image: "https://picsum.photos/seed/quiz1/600/300",
          tags: ["team", "culture", "communication"],
          metadata: {
            quiz_rating: 4.7,
            takers: 128,
            questions: 15,
          },
        },
        {
          id: 2,
          created_at: "2026-08-05T11:00:00Z",
          updated_at: "2026-08-05T11:00:00Z",
          title: "Product Feature Feedback",
          description: "Help us prioritize the next set of features.",
          created_by: 1,
          banner_image: "https://picsum.photos/seed/quiz2/600/300",
          metadata: {
            quiz_rating: 4.3,
            takers: 76,
            questions: 10,
          },
        },
        {
          id: 3,
          created_at: "2026-08-10T08:30:00Z",
          updated_at: "2026-08-12T16:45:00Z",
          title: "Onboarding Experience Survey",
          description: "Tell us how your first 30 days went.",
          created_by: 1,
          banner_image: "https://picsum.photos/seed/quiz3/600/300",
          metadata: {
            quiz_rating: 4.9,
            takers: 243,
            questions: 20,
          },
        },
        {
          id: 4,
          created_at: "2026-08-15T13:00:00Z",
          updated_at: "2026-08-15T13:00:00Z",
          title: "Remote Work Preferences",
          description: "",
          created_by: 1,
          banner_image: "https://picsum.photos/seed/quiz4/600/300",
          metadata: {
            quiz_rating: 4.5,
            takers: 91,
            questions: 12,
          },
        },
      ],
    },

    init() {
      this.$watch("profileMenuOpen", (open) => {
        if (open) {
          this.$nextTick(() => {
            if (window.lucide) lucide.createIcons();
          });
        }
      });
    },

    toggleProfileMenu() {
      this.profileMenuOpen = !this.profileMenuOpen;
    },

    changeSection(direction) {
      const sections = this.settingsVars.sections;

      const currentIndex = sections.findIndex(
        (s) => s.id === this.settingsVars.selectedSection
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
        (Date.now() - new Date(timestamp).getTime()) / 1000
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