// 表单验证增强
document.addEventListener('DOMContentLoaded', function() {
    // 注册表单密码确认验证
    const registerForm = document.querySelector('form[action*="register"]');
    if (registerForm) {
        const password = registerForm.querySelector('#password');
        const confirmPassword = registerForm.querySelector('#confirm_password');
        
        registerForm.addEventListener('submit', function(e) {
            if (password.value !== confirmPassword.value) {
                e.preventDefault();
                alert('两次输入的密码不一致，请重新输入');
                confirmPassword.focus();
            }
        });
    }

    // 评论表单字数限制
    const commentForm = document.querySelector('.comment-form');
    if (commentForm) {
        const textarea = commentForm.querySelector('textarea');
        textarea.addEventListener('input', function() {
            if (this.value.length > 1000) {
                this.value = this.value.substring(0, 1000);
                alert('评论内容不能超过1000字');
            }
        });
    }

    // 自动消失的提示消息
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.opacity = '0';
            setTimeout(() => alert.remove(), 500);
        }, 5000);
    });
});
