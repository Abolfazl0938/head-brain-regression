import flet as ft
import joblib
import numpy as np

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

    # تنظیمات پنجره (ارتفاع را برای جا دادن فیلدها و نتیجه تنظیم کردیم)
    page.window.width = 450
    page.window.height = 750
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

    header_row = ft.Row(
        controls=[
            title,
            theme_btn,
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )

    subtitle = ft.Text(
        "پیش‌بینی وزن مغز بر اساس ویژگی‌های مدل",
        size=12,
        color=ft.Colors.GREY_600,
    )

    # ورودی‌ها
    head_size_input = ft.TextField(
        label="Head Size (cm³)",
        hint_text="مثال: 3500",
        keyboard_type=ft.KeyboardType.NUMBER,
    )

    gender_dropdown = ft.Dropdown(
        label="Gender",
        value="1",
        options=[
            ft.DropdownOption(key="1", text="Male (Code 1)"),
            ft.DropdownOption(key="2", text="Female (Code 2)"),
        ],
    )

    age_dropdown = ft.Dropdown(
        label="Age Range",
        value="1",
        options=[
            ft.DropdownOption(key="1", text="Age Group 1 (Code 1)"),
            ft.DropdownOption(key="2", text="Age Group 2 (Code 2)"),
        ],
    )

    result_text = ft.Text(
        "وزن پیش‌بینی‌شده مغز: هنوز محاسبه نشده است",
        size=14,
        weight=ft.FontWeight.BOLD,
        color=ft.Colors.BLUE_800,
    )

    # تابع محاسبه پیش‌بینی با مدل
    def handle_predict(e):
        if not model:
            result_text.value = "❌ خطا: مدل بارگذاری نشده است!"
            result_text.color = ft.Colors.RED
            page.update()
            return

        try:
            head_val = float(head_size_input.value.strip())
            gender_val = float(gender_dropdown.value)
            age_val = float(age_dropdown.value)

            # ترتیب ویژگی‌ها در مدل: ['Head Size(cm^3)', 'Gender', 'Age Range']
            features = np.array([[head_val, gender_val, age_val]])
            prediction = model.predict(features)[0]

            result_text.value = f"🧠 وزن تخمینی مغز: {prediction:.2f} گرم"
            result_text.color = ft.Colors.GREEN
        except ValueError:
            result_text.value = "⚠️ لطفاً یک عدد معتبر برای Head Size وارد کنید!"
            result_text.color = ft.Colors.RED
        except Exception as ex:
            result_text.value = f"❌ خطا در پیش‌بینی: {str(ex)}"
            result_text.color = ft.Colors.RED

        page.update()

    predict_btn = ft.Button(
        content=ft.Text("محاسبه وزن مغز"),
        on_click=handle_predict,
    )

    # بخش توضیحات درباره مدل
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
                head_size_input,
                gender_dropdown,
                age_dropdown,
                predict_btn,
                result_text,
                ft.Divider(),
                about_card,
            ],
            spacing=10,
        )
    )


if __name__ == "__main__":
    ft.run(main)
