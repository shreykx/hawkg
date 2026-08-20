function Base() {
    return {
        signin: {
            identifier: null,
            password: null,
            button: null,
            googleButton: null,
            showPassword: false,
        },

        signup: {
            email: null,
            username: null,
            displayName: null,
            password: null,
            button: null,
            googleButton: null,
            showPassword: false,
        },
        notification: {
            visible: false,
            title: "",
            message: "",
            type: "error",
            shake: false,
        },
        init() {
            this.signin.identifier = this.$refs.signinIdentifier;
            this.signin.password = this.$refs.signinPassword;
            this.signin.button = this.$refs.signinButton;
            this.signin.googleButton = this.$refs.signinGoogleButton;

            this.signup.email = this.$refs.signupEmail;
            this.signup.username = this.$refs.signupUsername;
            this.signup.displayName = this.$refs.signupDisplayName;
            this.signup.password = this.$refs.signupPassword;
            this.signup.button = this.$refs.signupButton;
            this.signup.googleButton = this.$refs.signupGoogleButton;

            // Nav may call createIcons before auth markup exists; refresh after Alpine mounts.
            this.$nextTick(() => {
                if (window.lucide) lucide.createIcons();
            });
        },
        signinSubmit() {
            const identifier = this.signin.identifier.value.trim();
            const password = this.signin.password.value;
        
            if (!identifier || !password) {
                this.notify("Missing fields.", "Please enter your email or username and password.");
                return;
            }
            this.signin.button.disabled = true;
            this.$refs.signinForm.submit();
        },
        
        signupSubmit() {
            const email = this.signup.email.value.trim();
            const username = this.signup.username.value.trim();
            const password = this.signup.password.value;
        
            const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        
            if (!email || !username || !password) {
                this.notify("Missing fields.", "Please fill in your email, username, and password.");
                return;
            }
        
            if (!emailPattern.test(email)) {
                this.notify("Invalid email.", "Please enter a valid email address.");
                return;
            }
        
            if (username.length < 3) {
                this.notify("Invalid username.", "Username must be at least 3 characters.");
                return;
            }
        
            if (password.length < 8) {
                this.notify("Password too short.", "Password must be at least 8 characters.");
                return;
            }
            this.signup.button.disabled = true;
            this.$refs.signupForm.submit();
        },
        notify(title = "Something went wrong", message = "", duration = null) {
            this.notification.title = title;
            this.notification.message = message;
            this.notification.visible = true;

            if (duration) {
                setTimeout(() => {
                    this.notification.visible = false;
                }, duration);
            }
        },
    }
}