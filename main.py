import random
import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.progressbar import ProgressBar
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
from kivy.storage.jsonstore import JsonStore

# Эмулируем экран телефона на ПК
Window.size = (360, 640)

# Инициализируем локальную базу данных (файл сохранится на устройстве)
store = JsonStore('user_profile.json')

class OnboardingScreen(Screen):
    """Экран регистрации и расчета параметров"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        layout = BoxLayout(orientation='vertical', padding=20, spacing=12)
        
        layout.add_widget(Label(text="Регистрация пользователя", font_size='22sp', bold=True, size_hint_y=None, height=40))
        
        # Поля ввода данных
        layout.add_widget(Label(text="Ваше имя:", size_hint_y=None, height=20, halign='left'))
        self.name_input = TextInput(text="Александр", multiline=False, size_hint_y=None, height=40)
        layout.add_widget(self.name_input)
        
        layout.add_widget(Label(text="Возраст (лет):", size_hint_y=None, height=20))
        self.age_input = TextInput(text="45", input_filter='int', multiline=False, size_hint_y=None, height=40)
        layout.add_widget(self.age_input)
        
        layout.add_widget(Label(text="Рост (см):", size_hint_y=None, height=20))
        self.height_input = TextInput(text="196", input_filter='int', multiline=False, size_hint_y=None, height=40)
        layout.add_widget(self.height_input)
        
        layout.add_widget(Label(text="Вес (кг):", size_hint_y=None, height=20))
        self.weight_input = TextInput(text="114", input_filter='int', multiline=False, size_hint_y=None, height=40)
        layout.add_widget(self.weight_input)
        
        layout.add_widget(Label(text="Ежедневная нагрузка:", size_hint_y=None, height=20))
        self.activity_spinner = Spinner(
            text='Сидячая работа',
            values=('Сидячая работа', 'Умеренная активность', 'Средняя активность'),
            size_hint_y=None, height=40
        )
        layout.add_widget(self.activity_spinner)
        
        # Кнопка расчета
        calc_btn = Button(
            text="Рассчитать и войти", 
            background_color=get_color_from_hex('#2ECC71'),
            font_size='16sp', bold=True, size_hint_y=None, height=50
        )
        calc_btn.bind(on_press=self.calculate_and_save)
        layout.add_widget(calc_btn)
        
        self.add_widget(layout)

    def calculate_and_save(self, instance):
        # Получаем данные из полей ввода
        try:
            name = self.name_input.text
            age = int(self.age_input.text)
            height = int(self.height_input.text)
            weight = int(self.weight_input.text)
        except ValueError:
            return  # Если поля пустые или некорректные, ничего не делаем

        # Математика Миффлина-Сан Жеора (для мужчин)
        bmr = (10 * weight) + (6.25 * height) - (5 * age) + 5
        
        # Коэффициенты активности
        activity_type = self.activity_spinner.text
        if activity_type == 'Сидячая работа':
            coef = 1.2
        elif activity_type == 'Умеренная активность':
            coef = 1.375
        else:
            coef = 1.55
            
        calories_maintenance = int(bmr * coef)
        # Безболезненное похудение (дефицит ~15-20%)
        # Ограничиваем нижний порог уровнем базового метаболизма (BMR) для безопасности
        calories_weight_loss = max(int(calories_maintenance * 0.85), int(bmr))

        # Сохраняем профиль в базу данных на устройстве
        store.put('user', 
                  name=name, age=age, height=height, weight=weight, 
                  activity=activity_type, maintenance=calories_maintenance, 
                  limit=calories_weight_loss)
        
        # Передаем данные в главный экран и переключаемся
        app = App.get_running_app()
        app.main_screen.load_user_data()
        app.screen_manager.current = 'main'


class MainTrackerScreen(Screen):
    """Главный экран приложения (дневник калорий и активность)"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_calories = 0
        self.daily_limit = 2150 # Значение по умолчанию, обновится из базы
        
        self.mock_meals = [
            {"name": "Завтрак: 2 сосиски, сыр, томат, хлеб", "kcal": 580},
            {"name": "Обед: Борщ, рис, куриное филе", "kcal": 650},
            {"name": "Перекус: Кофе с молоком и круассан", "kcal": 420},
            {"name": "Ужин: Стейк из лосося с брокколи", "kcal": 510},
            {"name": "Перекус: Горсть фундука и бананы", "kcal": 310}
        ]

        main_layout = BoxLayout(orientation='vertical', padding=15, spacing=10)
        
        # Приветствие и лимиты
        self.welcome_label = Label(text="Привет!", font_size='18sp', bold=True, size_hint_y=None, height=30)
        main_layout.add_widget(self.welcome_label)
        
        self.limits_info_label = Label(text="", font_size='12sp', color=get_color_from_hex('#BDC3C7'), size_hint_y=None, height=30)
        main_layout.add_widget(self.limits_info_label)

        # Инфо-панель текущих калорий
        self.info_label = Label(text="", font_size='15sp', halign='center', size_hint_y=None, height=50)
        main_layout.add_widget(self.info_label)

        # Шкала прогресса
        self.progress_bar = ProgressBar(max=self.daily_limit, value=0, size_hint_y=None, height=15)
        main_layout.add_widget(self.progress_bar)

        # Блок штрафных отработок
        self.burn_label = Label(text="Вы в пределах нормы.\nТак держать!", font_size='14sp', color=get_color_from_hex('#2ECC71'), halign='center', size_hint_y=None, height=60)
        main_layout.add_widget(self.burn_label)

        # Дневник питания
        main_layout.add_widget(Label(text="Дневник питания за сегодня:", font_size='13sp', bold=True, size_hint_y=None, height=20, halign='left'))
        scroll_view = ScrollView(size_hint=(1, 1))
        self.history_layout = GridLayout(cols=1, spacing=5, size_hint_y=None)
        self.history_layout.bind(minimum_height=self.history_layout.setter('height'))
        scroll_view.add_widget(self.history_layout)
        main_layout.add_widget(scroll_view)

        # Кнопки
        buttons_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height=50)
        photo_btn = Button(text="📸 Сделать фото еды", background_color=get_color_from_hex('#3498DB'), font_size='15sp', bold=True)
        photo_btn.bind(on_press=self.simulate_photo_capture)
        
        reset_btn = Button(text="🔄 Сброс", background_color=get_color_from_hex('#E74C3C'), size_hint_x=0.25, font_size='13sp')
        reset_btn.bind(on_press=self.reset_day)
        
        buttons_layout.add_widget(photo_btn)
        buttons_layout.add_widget(reset_btn)
        main_layout.add_widget(buttons_layout)

        self.add_widget(main_layout)

    def load_user_data(self):
        """Загрузка рассчитанных данных из локального файла"""
        if store.exists('user'):
            user = store.get('user')
            self.daily_limit = user['limit']
            self.progress_bar.max = self.daily_limit
            
            self.welcome_label.text = f"Дневник питания: {user['name']}"
            self.limits_info_label.text = f"Для жизни: {user['maintenance']} ккал | Цель (похудение): {user['limit']} ккал"
            self.update_ui()

    def update_ui(self):
        left_calories = self.daily_limit - self.current_calories
        if left_calories >= 0:
            self.info_label.text = f"Съедено: {self.current_calories} / {self.daily_limit} ккал\nОсталось: {left_calories} ккал"
        else:
            self.info_label.text = f"Съедено: {self.current_calories} / {self.daily_limit} ккал\nПеребор: {abs(left_calories)} ккал!"
        self.update_burn_tasks()

    def simulate_photo_capture(self, instance):
        meal = random.choice(self.mock_meals)
        self.current_calories += meal['kcal']
        self.progress_bar.value = min(self.current_calories, self.daily_limit)
        
        meal_entry = Label(text=f"• {meal['name']} (+{meal['kcal']} ккал)", font_size='13sp', size_hint_y=None, height=25, halign='left', valign='middle')
        meal_entry.bind(size=meal_entry.setter('text_size'))
        self.history_layout.add_widget(meal_entry)
        
        self.update_ui()

    def update_burn_tasks(self):
        if self.current_calories > self.daily_limit:
            excess = self.current_calories - self.daily_limit
            steps_needed = int(excess * 15)
            squats_needed = int(excess * 2)
            
            self.burn_label.text = f"⚠️ ПРЕВЫШЕНИЕ НА {excess} ккал!\nОтработка: 🏃 {steps_needed} шагов ИЛИ 🏋️ {squats_needed} приседаний"
            self.burn_label.color = get_color_from_hex('#E67E22')
        else:
            self.burn_label.text = "Вы в пределах нормы.\nТак держать!"
            self.burn_label.color = get_color_from_hex('#2ECC71')

    def reset_day(self, instance):
        self.current_calories = 0
        self.progress_bar.value = 0
        self.history_layout.clear_widgets()
        self.update_ui()


class CalorieTrackerApp(App):
    def build(self):
        self.screen_manager = ScreenManager()
        
        # Создаем экраны
        self.onboarding_screen = OnboardingScreen(name='onboarding')
        self.main_screen = MainTrackerScreen(name='main')
        
        self.screen_manager.add_widget(self.onboarding_screen)
        self.screen_manager.add_widget(self.main_screen)
        
        # ЛОГИКА ПЕРВОГО ЗАПУСКА:
        # Если пользователь уже регистрировался — сразу открываем главный экран
        if store.exists('user'):
            self.main_screen.load_user_data()
            self.screen_manager.current = 'main'
        else:
            self.screen_manager.current = 'onboarding'
            
        return self.screen_manager

if __name__ == '__main__':
    CalorieTrackerApp().run()