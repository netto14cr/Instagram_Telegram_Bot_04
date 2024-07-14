class MessageManager:
    def __init__(self):
        self.language_code = "en-US"  # Default language for recognition
        self.language = "en"  # Default language for bot messages

    def get_text(self, key):
        texts = {
            "en": {
                "start": "Welcome to the Instagram_Metrics Bot! This bot helps you retrieve metrics data from your Instagram account. \n\nPlease choose an action.",
                "login_prompt": "Enter your Instagram username:",
                "password_prompt": "Enter your Instagram password:",
                "2fa_prompt": "Two-factor authentication is required. Please send the 2FA code.",
                "auth_success": "Successfully authenticated! ✅",
                "auth_failed": "Authentication failed. Please try again. ❌",
                "followers": "My followers 👥",
                "not_following_back": "Not following back ❌",
                "following_not_followed": "Following but not followed ➡️",
                "error": "An error occurred:",
                "options": "Choose an option:"
            },
            "es": {
                "start": "¡Bienvenido al Instagram_Metrics Bot! Este bot te ayuda a obtener métricas de tu cuenta de Instagram. Por favor, elige una acción.",
                "login_prompt": "Ingresa tu nombre de usuario de Instagram:",
                "password_prompt": "Ingresa tu contraseña de Instagram:",
                "2fa_prompt": "Se requiere autenticación de dos factores. Por favor, envía el código 2FA.",
                "auth_success": "¡Autenticación exitosa! ✅",
                "auth_failed": "Autenticación fallida. Por favor, inténtalo de nuevo. ❌",
                "followers": "Mis seguidores 👥",
                "not_following_back": "No me siguen de vuelta ❌",
                "following_not_followed": "Sigo pero no me siguen ➡️",
                "error": "Ocurrió un error:",
                "options": "Elige una opción:"
            },
            "de": {
                "start": "Willkommen beim Instagram_Metrics Bot! Dieser Bot hilft Ihnen, Metriken von Ihrem Instagram-Konto abzurufen. Bitte wählen Sie eine Aktion.",
                "login_prompt": "Geben Sie Ihren Instagram-Benutzernamen ein:",
                "password_prompt": "Geben Sie Ihr Instagram-Passwort ein:",
                "2fa_prompt": "Eine Zwei-Faktor-Authentifizierung ist erforderlich. Bitte senden Sie den 2FA-Code.",
                "auth_success": "Erfolgreich authentifiziert! ✅",
                "auth_failed": "Authentifizierung fehlgeschlagen. Bitte versuchen Sie es erneut. ❌",
                "followers": "Meine Follower 👥",
                "not_following_back": "Folgt nicht zurück ❌",
                "following_not_followed": "Folge, aber wird nicht gefolgt ➡️",
                "error": "Ein Fehler ist aufgetreten:",
                "options": "Wählen Sie eine Option:"
            },
            "ja": {
                "start": "Instagram_Metrics Botへようこそ！ このボットは、あなたのInstagramアカウントからメトリクスデータを取得するのに役立ちます。 アクションを選択してください。",
                "login_prompt": "Instagramのユーザー名を入力してください：",
                "password_prompt": "Instagramのパスワードを入力してください：",
                "2fa_prompt": "二要素認証が必要です。2FAコードを送信してください。",
                "auth_success": "認証に成功しました！ ✅",
                "auth_failed": "認証に失敗しました。もう一度お試しください。 ❌",
                "followers": "私のフォロワー 👥",
                "not_following_back": "フォローされていない ❌",
                "following_not_followed": "フォローしているがフォローされていない ➡️",
                "error": "エラーが発生しました：",
                "options": "オプションを選択してください："
            }
        }
        return texts[self.language].get(key, key)

    def set_language(self, language_code, language):
        self.language_code = language_code
        self.language = language
