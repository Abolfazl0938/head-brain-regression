import flet as ft
import joblib
import numpy as np

# بارگذاری مدل رگرسیون
MODEL_PATH = "head_brain_model.joblib"

try:
    model = joblib.load(MODEL_PATH)
    print("✅ Model loaded successfully!")
except Exception as e:
    print(f"❌ Error loading model: {e}")
    model = None


def main(page: ft.Page):
    # تنظیمات صفحه
    page.title = "Head & Brain Weight Predictor"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20

    # تنظیمات پنجره
    page.window.width = 450
    page.window.height = 750
    page.window.resizable = False

    # تغییر حالت روشن و تاریک
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

    # دکمهٔ تغییر تم
    theme_btn = ft.IconButton(
        icon=ft.Icons.DARK_MODE,
        tooltip="تغییر به تم تاریک",
        on_click=toggle_theme,
    )

    # عنوان برنامه
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

    # ورودی اندازهٔ سر
    head_size_input = ft.TextField(
        label="Head Size (cm³)",
        hint_text="مثال: 3500",
        keyboard_type=ft.KeyboardType.NUMBER,
    )

    # انتخاب کد جنسیت
    gender_dropdown = ft.Dropdown(
        label="Gender",
        value="1",
        options=[
            ft.DropdownOption(key="1", text="Male (Code 1)"),
            ft.DropdownOption(key="2", text="Female (Code 2)"),
        ],
    )

    # انتخاب کد گروه سنی
    age_dropdown = ft.Dropdown(
        label="Age Range",
        value="1",
        options=[
            ft.DropdownOption(key="1", text="Age Group 1 (Code 1)"),
            ft.DropdownOption(key="2", text="Age Group 2 (Code 2)"),
        ],
    )

    # نمایش نتیجه یا خطا
    result_text = ft.Text(
        "وزن پیش‌بینی‌شده مغز: هنوز محاسبه نشده است",
        size=14,
        weight=ft.FontWeight.BOLD,
        color=ft.Colors.BLUE_800,
    )

    # اعتبارسنجی ورودی و محاسبهٔ پیش‌بینی
    def handle_predict(e):
        if model is None:
            result_text.value = "❌ Error: model was not loaded."
            result_text.color = ft.Colors.RED
            page.update()
            return

        raw_head_size = (head_size_input.value or "").strip()

        if not raw_head_size:
            result_text.value = "⚠️ Please enter the head size."
            result_text.color = ft.Colors.RED
            page.update()
            return

        try:
            head_val = float(raw_head_size)
        except ValueError:
            result_text.value = "⚠️ Head Size must be a valid number."
            result_text.color = ft.Colors.RED
            page.update()
            return

        if not np.isfinite(head_val) or head_val <= 0:
            result_text.value = "⚠️ Head Size must be a positive number."
            result_text.color = ft.Colors.RED
            page.update()
            return

        try:
            gender_val = float(gender_dropdown.value)
            age_val = float(age_dropdown.value)

            # ترتیب ویژگی‌ها در مدل:
            # Head Size(cm^3), Gender, Age Range
            features = np.array([[head_val, gender_val, age_val]])
            prediction = model.predict(features)[0]

            result_text.value = f"🧠 Estimated Brain Weight: {prediction:.2f} grams"
            result_text.color = ft.Colors.GREEN

        except Exception as ex:
            result_text.value = f"❌ Prediction error: {ex}"
            result_text.color = ft.Colors.RED

        page.update()

    # دکمهٔ محاسبه
    predict_btn = ft.Button(
        content=ft.Text("محاسبه وزن مغز"),
        on_click=handle_predict,
    )

    # توضیحات مدل
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

    # چیدمان عناصر برنامه
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
