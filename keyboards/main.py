from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

rates_button = KeyboardButton(text="Rates 📈")
rate_changes_button = KeyboardButton(text="Rate Changes 📊")
help_button = KeyboardButton(text="Help 🆘")

main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            rates_button,
            rate_changes_button
        ],
        [
            help_button
        ]
    ],
    resize_keyboard=True
)
