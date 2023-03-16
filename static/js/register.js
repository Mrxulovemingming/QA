function bindEmailCaptchaClick() {
    $("#captcha-btn").click(function (event) {
        // 获取验证码按钮的 JQuery 对象
        var $this = $(this);
        // 阻止默认的事件
        event.preventDefault();
        var email = $("input[name='email']").val(); // 通过name获取输入框信息
        $.ajax({
            url: "/auth/captcha?email=" + email,
            method: "GET",
            success: function (result) {
                var code = result['code'];
                if (code == 200) {
                    var countdown = 60;
                    $this.off("click");
                    var timer = setInterval(function () {
                        $this.text(countdown);
                        countdown = countdown-1;
                        if (countdown <= 0) {
                            clearInterval(timer); // 清掉定时器
                            $this.text("获取验证码");
                            // 重新绑定事件
                            bindEmailCaptchaClick();
                        }
                    }, 1000);
                    alert("邮箱验证码发送成功！");
                } else {
                    alert(result['msg']);
                }
            },
            fail: function (error) {
                console.log(error);
            }
        });
    });
}

// 整个网页加载完毕后再执行
$(function () {
    bindEmailCaptchaClick()
});