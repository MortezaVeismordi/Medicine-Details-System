from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
import pandas as pd

file_path = 'Preprocessed_Medicine_Details.csv'  
try:
    medicine_data = pd.read_csv(file_path)
except FileNotFoundError:
    medicine_data = pd.DataFrame(columns=['Medicine Name', 'Composition', 'Uses', 'Side_effects',
                                          'Manufacturer', 'Excellent Review %', 'Average Review %', 'Poor Review %'])

class MedicineSearchApp(App):
    def build(self):
        self.title = "Medicine Database Search"
        self.medicine_names = medicine_data['Medicine Name'].dropna().tolist()

        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        self.layout.add_widget(Label(text="Medicine Database Search", font_size=20, bold=True, size_hint=(1, None), height=40))

        self.search_input = TextInput(hint_text="Enter Medicine Name", size_hint=(1, None), height=40, multiline=False)
        self.search_input.bind(text=self.update_scroll_list)
        self.layout.add_widget(self.search_input)

      
        self.scroll_layout = ScrollView(size_hint=(1, 0.6)) 
        self.grid = GridLayout(cols=1, size_hint_y=None, spacing=5)
        self.grid.bind(minimum_height=self.grid.setter('height'))
        self.scroll_layout.add_widget(self.grid)
        self.layout.add_widget(self.scroll_layout)

        self.populate_medicine_list(self.medicine_names[:100]) 

        button_layout = BoxLayout(size_hint=(1, None), height=40)
        search_button = Button(text="Search", on_press=self.search_medicine)
        reset_button = Button(text="Reset", on_press=self.reset_fields)
        button_layout.add_widget(search_button)
        button_layout.add_widget(reset_button)
        self.layout.add_widget(button_layout)

        self.info_labels = {}
        fields = ["Medicine Name", "Composition", "Uses", "Side Effects", "Manufacturer", "Reviews"]
        for field in fields:
            field_box = BoxLayout(orientation='vertical', size_hint=(1, None), height=60)
            field_label = Label(text=f"{field}:", font_size=16, size_hint=(1, None), height=30)
            self.info_labels[field] = Label(text="", font_size=14, size_hint=(1, None), height=30)
            field_box.add_widget(field_label)
            field_box.add_widget(self.info_labels[field])
            self.layout.add_widget(field_box)

        return self.layout

    def populate_medicine_list(self, medicine_names):
        """Populate the scrollable list with a limited number of medicine names."""
        self.grid.clear_widgets()  
        for name in medicine_names:
            btn = Button(text=name, size_hint_y=None, height=44)
            btn.bind(on_release=lambda btn: self.select_medicine(btn.text))
            self.grid.add_widget(btn)

    def update_scroll_list(self, instance, value):
        """Update the scrollable list dynamically based on input text."""
        if value.strip():
            suggestions = medicine_data[medicine_data['Medicine Name']
                                        .str.contains(f"^{value}", na=False, case=False)]['Medicine Name'].tolist()
        else:
            suggestions = self.medicine_names[:100]  
        self.populate_medicine_list(suggestions)

    def select_medicine(self, name):
        """Handle selection of a medicine from the scrollable list."""
        self.search_input.text = name  
        self.search_medicine(None)  

    def search_medicine(self, instance):
        """Search for medicine details and display results."""
        medicine_name = self.search_input.text.strip()
        if not medicine_name:
            self.show_popup("Error", "Please enter a medicine name")
            return

        results = medicine_data[medicine_data['Medicine Name'].str.contains(medicine_name, case=False, na=False)]
        if not results.empty:
            result = results.iloc[0]
            self.info_labels["Medicine Name"].text = result['Medicine Name']
            self.info_labels["Composition"].text = result['Composition']
            self.info_labels["Uses"].text = result['Uses']
            self.info_labels["Side Effects"].text = result['Side_effects']
            self.info_labels["Manufacturer"].text = result['Manufacturer']
            self.info_labels["Reviews"].text = f"Excellent: {result['Excellent Review %']}% | Average: {result['Average Review %']}% | Poor: {result['Poor Review %']}%"
        else:
            self.show_popup("Result", "No Medicine Found")

    def reset_fields(self, instance):
        """Reset all fields and input."""
        self.search_input.text = ""
        self.populate_medicine_list(self.medicine_names[:100]) 
        for label in self.info_labels.values():
            label.text = ""

    def show_popup(self, title, message):
        """Show a popup with the given title and message."""
        popup = Popup(title=title, content=Label(text=message), size_hint=(0.8, 0.4))
        popup.open()


if __name__ == "__main__":
    MedicineSearchApp().run()
