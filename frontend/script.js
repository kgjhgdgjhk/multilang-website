// إدارة الترجمات واللغة
class TranslationManager {
    constructor() {
        this.currentLang = localStorage.getItem('preferredLanguage') || 'en';
        this.translations = {};
    }

    async loadTranslations(lang = null) {
        if (lang) {
            this.currentLang = lang;
            localStorage.setItem('preferredLanguage', lang);
        }

        try {
            const response = await fetch(`/api/translations/${this.currentLang}`);
            this.translations = await response.json();
            this.applyTranslations();
            this.updateLanguageSelector();
        } catch (error) {
            console.error('Failed to load translations:', error);
        }
    }

    applyTranslations() {
        // تحديث جميع العناصر التي تحتوي على خاصية data-i18n
        document.querySelectorAll('[data-i18n]').forEach(element => {
            const key = element.getAttribute('data-i18n');
            if (this.translations[key]) {
                if (element.tagName === 'INPUT' && element.type !== 'submit') {
                    element.placeholder = this.translations[key];
                } else {
                    element.textContent = this.translations[key];
                }
            }
        });
    }

    updateLanguageSelector() {
        const buttons = document.querySelectorAll('.lang-btn');
        buttons.forEach(btn => {
            if (btn.dataset.lang === this.currentLang) {
                btn.classList.add('active');
                btn.style.background = 'rgba(255, 255, 255, 0.4)';
            } else {
                btn.classList.remove('active');
                btn.style.background = '';
            }
        });
    }

    get(key) {
        return this.translations[key] || key;
    }
}

// إدارة المصادقة
class AuthManager {
    constructor() {
        this.token = localStorage.getItem('auth_token');
    }

    isLoggedIn() {
        return !!this.token;
    }

    async login(username, password) {
        try {
            const formData = new FormData();
            formData.append('username', username);
            formData.append('password', password);

            const response = await fetch('/api/login', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                throw new Error('Login failed');
            }

            const data = await response.json();
            this.token = data.access_token;
            localStorage.setItem('auth_token', this.token);
            
            this.showMessage('Login successful!', 'success');
            setTimeout(() => {
                window.location.href = '/dashboard';
            }, 1500);
            
            return true;
        } catch (error) {
            this.showMessage('Invalid username or password', 'error');
            return false;
        }
    }

    async register(userData) {
        try {
            const formData = new FormData();
            for (const key in userData) {
                formData.append(key, userData[key]);
            }

            const response = await fetch('/api/register', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();
            
            if (!response.ok) {
                throw new Error(data.message || 'Registration failed');
            }

            this.showMessage('Registration successful! You can now login.', 'success');
            
            setTimeout(() => {
                window.location.href = '/login';
            }, 2000);
            
            return true;
        } catch (error) {
            this.showMessage(error.message || 'Registration failed', 'error');
            return false;
        }
    }

    logout() {
        this.token = null;
        localStorage.removeItem('auth_token');
        window.location.href = '/';
    }

    showMessage(text, type) {
        let messageDiv = document.getElementById('message');
        if (!messageDiv) {
            messageDiv = document.createElement('div');
            messageDiv.id = 'message';
            messageDiv.className = 'message';
            document.querySelector('main').prepend(messageDiv);
        }
        
        messageDiv.textContent = text;
        messageDiv.className = `message ${type}`;
        messageDiv.style.display = 'block';
        
        setTimeout(() => {
            messageDiv.style.display = 'none';
        }, 5000);
    }
}

// تهيئة التطبيق
class App {
    constructor() {
        this.translationManager = new TranslationManager();
        this.authManager = new AuthManager();
        this.init();
    }

    async init() {
        // تحميل الترجمات
        await this.translationManager.loadTranslations();
        
        // إضافة معالجات الأحداث
        this.setupEventListeners();
        
        // تحديث واجهة المستخدم بناءً على حالة المصادقة
        this.updateUI();
    }

    setupEventListeners() {
        // معالج تغيير اللغة
        document.querySelectorAll('.lang-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const lang = e.target.dataset.lang;
                this.translationManager.loadTranslations(lang);
            });
        });

        // معالج تسجيل الدخول
        const loginForm = document.getElementById('loginForm');
        if (loginForm) {
            loginForm.addEventListener('submit', async (e) => {
                e.preventDefault();
                const username = document.getElementById('username').value;
                const password = document.getElementById('password').value;
                await this.authManager.login(username, password);
            });
        }

        // معالج التسجيل
        const registerForm = document.getElementById('registerForm');
        if (registerForm) {
            registerForm.addEventListener('submit', async (e) => {
                e.preventDefault();
                const userData = {
                    username: document.getElementById('reg-username').value,
                    email: document.getElementById('reg-email').value,
                    full_name: document.getElementById('reg-fullname').value,
                    password: document.getElementById('reg-password').value,
                    language: this.translationManager.currentLang
                };
                await this.authManager.register(userData);
            });
        }

        // معالج تسجيل الخروج
        const logoutBtn = document.getElementById('logoutBtn');
        if (logoutBtn) {
            logoutBtn.addEventListener('click', () => {
                this.authManager.logout();
            });
        }
    }

    updateUI() {
        const loginBtn = document.getElementById('loginBtn');
        const logoutBtn = document.getElementById('logoutBtn');
        const registerBtn = document.getElementById('registerBtn');
        const dashboardLink = document.getElementById('dashboardLink');

        if (this.authManager.isLoggedIn()) {
            if (loginBtn) loginBtn.style.display = 'none';
            if (registerBtn) registerBtn.style.display = 'none';
            if (logoutBtn) logoutBtn.style.display = 'inline-block';
            if (dashboardLink) dashboardLink.style.display = 'inline-block';
        } else {
            if (loginBtn) loginBtn.style.display = 'inline-block';
            if (registerBtn) registerBtn.style.display = 'inline-block';
            if (logoutBtn) logoutBtn.style.display = 'none';
            if (dashboardLink) dashboardLink.style.display = 'none';
        }
    }
}

// بدء تشغيل التطبيق عند تحميل الصفحة
document.addEventListener('DOMContentLoaded', () => {
    window.app = new App();
});