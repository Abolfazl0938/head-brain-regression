import flet as ft
import joblib

# ۱. بارگذاری مدل رگرسیون
MODEL_PATH = "head_brain_model.joblib"
try:
    model = joblib.load(MODEL_PATH)
    print("✅ Model loaded successfully!")
except Exception as e:
    print(f"❌ Error loading model: {e}")
    model = None


def main(page: ft.Page):
    # تنظیمات ظاهری صفحه سازگار با Flet 1.0+
    page.title = "Head & Brain Weight Predictor"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20

    # تنظیمات پنجره
    page.window.width = 450
    page.window.height = 650
    page.window.resizable = False

    # تابع تغییر حالت روز و شب
    def toggle_theme(e):
        if page.theme_mode == ft.ThemeMode.LIGHT:
            page.theme_mode = ft.ThemeMode.DARK
            theme_btn.icon = ft.Icons.LIGHT_MODE
            theme_btn.tooltip = "تغییر به تم روشن"
        else:
            page.theme_mode = ft.ThemeMode.LIGHT
            theme_btn.icon = ft.Icons.DARK_MODE
            theme_btn.tooltip = "تغییر به تم تاریک"
        page.update()

    # دکمه سوئیچ تم
    theme_btn = ft.IconButton(
        icon=ft.Icons.DARK_MODE,
        tooltip="تغییر به تم تاریک",
        on_click=toggle_theme,
    )

    # عنوان بالای صفحه
    title = ft.Text(
        "🧠 Brain Weight Predictor",
        size=20,
        weight=ft.FontWeight.BOLD,
    )

    # ردیف بالای صفحه شامل عنوان و دکمه تم
    header_row = ft.Row(
        controls=[
            title,
            theme_btn,
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )

    subtitle = ft.Text(
        "پیش‌بینی وزن مغز بر اساس اندازه سر، جنسیت و رده سنی",
        size=12,
        color=ft.Colors.GREY_600,
    )

    status_text = ft.Text(
        "آماده برای دریافت ورودی..." if model else "خطا در بارگذاری مدل!",
        color=ft.Colors.GREEN if model else ft.Colors.RED,
        weight=ft.FontWeight.W_500,
    )

    # بخش توضیحات درباره مدل به زبان انگلیسی
    about_card = ft.Card(
        content=ft.Container(
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Icon(ft.Icons.INFO_OUTLINE, size=16),
                            ft.Text(
                                "About the Model:",
                                size=13,
                                weight=ft.FontWeight.BOLD,
                            ),
                        ],
                        spacing=5,
                    ),
                    ft.Text(
                        "This application uses a Linear Regression model. "
                        "It predicts the estimated Brain Weight based on "
                        "Head Size, Gender, and Age Range features.",
                        size=11,
                        color=ft.Colors.GREY_600,
                    ),
                ],
                spacing=6,
            ),
            padding=12,
        )
    )

    # چیدمان عناصر
    page.add(
        ft.Column(
            controls=[
                header_row,
                subtitle,
                ft.Divider(),
                status_text,
                ft.Divider(),
                about_card,
            ],
            spacing=10,
        )
    )


if __name__ == "__main__":
    ft.run(main)
