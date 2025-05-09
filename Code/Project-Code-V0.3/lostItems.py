from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.dialog import MDDialog
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.screen import MDScreen
from kivymd.uix.list import OneLineListItem, MDList
from kivymd.uix.scrollview import MDScrollView
from kivy.metrics import dp
from kivy.uix.scrollview import ScrollView

class LostItemsApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "BlueGray"
        self.theme_cls.theme_style = "Light"

        self.screen = MDScreen()
        self.main_layout = MDBoxLayout(
            orientation='vertical',
            padding=dp(20),
            spacing=dp(20),
            size_hint_y=None,
            adaptive_height=True
        )

        self.scroll_wrapper = MDScrollView()
        self.scroll_wrapper.add_widget(self.main_layout)
        self.screen.add_widget(self.scroll_wrapper)

        self.show_homepage()
        return self.screen

    def show_homepage(self):
        self.main_layout.clear_widgets()
        title = MDLabel(
            text="Αρχική Οθόνη",
            halign="center",
            font_style="H4",
            size_hint_y=None,
            height=dp(60)
        )
        self.main_layout.add_widget(title)

        lost_items_button = MDRaisedButton(
            text="Lost Items",
            pos_hint={"center_x": 0.5}
        )
        lost_items_button.bind(on_release=self.check_lost_items)
        self.main_layout.add_widget(lost_items_button)

    def check_lost_items(self, instance):
        self.lost_items = [
            {"name": "Πορτοφόλι", "date": "2025-04-11", "details": "Μαύρο δερμάτινο πορτοφόλι"},
            {"name": "Κλειδιά", "date": "2025-05-01", "details": "Δέσμη με 3 κλειδιά και μπρελόκ"}
        ]
        if not self.lost_items:
            self.show_dialog("Μήνυμα", "Δεν υπάρχουν διαθέσιμα χαμένα αντικείμενα.")
        else:
            self.show_lost_items_list()

    def show_lost_items_list(self):
        self.main_layout.clear_widgets()
        title = MDLabel(
            text="Λίστα Χαμένων Αντικειμένων",
            halign="center",
            font_style="H5",
            size_hint_y=None,
            height=dp(40)
        )
        self.main_layout.add_widget(title)

        scroll = ScrollView(size_hint=(1, None), size=(self.screen.width, dp(400)))
        list_view = MDList()
        for item in self.lost_items:
            list_item = OneLineListItem(
                text=f"{item['name']} - {item['date']}",
                on_release=lambda x, i=item: self.show_item_details(i)
            )
            list_view.add_widget(list_item)

        scroll.add_widget(list_view)
        self.main_layout.add_widget(scroll)

    def show_item_details(self, item):
        self.main_layout.clear_widgets()
        title = MDLabel(
            text="Λεπτομέρειες Αντικειμένου",
            halign="center",
            font_style="H5",
            size_hint_y=None,
            height=dp(40)
        )
        self.main_layout.add_widget(title)

        details_label = MDLabel(
            text=f"Όνομα: {item['name']}\nΗμερομηνία: {item['date']}\nΠεριγραφή: {item['details']}",
            halign="left",
            size_hint_y=None
        )
        self.main_layout.add_widget(details_label)

        identify_button = MDRaisedButton(
            text="Identify",
            pos_hint={"center_x": 0.5}
        )
        identify_button.bind(on_release=self.show_phone_input)
        self.main_layout.add_widget(identify_button)

    def show_phone_input(self, instance):
        self.phone_input = MDTextField(
            hint_text="Εισάγετε το κινητό σας τηλέφωνο",
            input_filter='int',
            max_text_length=10
        )
        self.dialog = MDDialog(
            title="Καταχώρηση Τηλεφώνου",
            type="custom",
            content_cls=self.phone_input,
            buttons=[
                MDFlatButton(text="Cancel", on_release=lambda x: self.dialog.dismiss()),
                MDFlatButton(text="Submit", on_release=self.validate_phone)
            ]
        )
        self.dialog.open()

    def validate_phone(self, instance):
        phone = self.phone_input.text.strip()
        if len(phone) == 10 and phone.isdigit():
            self.dialog.dismiss()
            self.show_dialog("Επιτυχία", "Η καταχώρηση τηλεφώνου ήταν επιτυχής.")
        else:
            self.dialog.dismiss()
            self.show_dialog("Σφάλμα", "Παρακαλώ εισάγετε έγκυρο αριθμό τηλεφώνου (10 ψηφία).")

    def show_dialog(self, title, text):
        dialog = MDDialog(
            title=title,
            text=text,
            buttons=[MDFlatButton(text="OK", on_release=lambda x: dialog.dismiss())]
        )
        dialog.open()

if __name__ == "__main__":
    LostItemsApp().run()
