from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.dialog import MDDialog
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.screen import MDScreen
from kivymd.uix.card import MDCard
from kivy.uix.scrollview import ScrollView


class LostItemsApp(MDApp):

    def build(self):
        self.theme_cls.primary_palette = "BlueGray"
        self.theme_cls.theme_style = "Light"

        self.screen = MDScreen()

        layout = MDBoxLayout(
            orientation='vertical',
            padding=40,
            spacing=25,
            size_hint=(1, None),
            height=self.screen.height,
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )

        # Τίτλος
        title = MDLabel(
            text="Lost Items",
            halign="center",
            font_style="H4",
            size_hint_y=None,
            height=60
        )
        layout.add_widget(title)

        # Κουμπιά επιλογών
        for btn_text, callback in [
            ("Lost Items - Report", self.show_report_form),
            ("Lost Items - Found List", self.show_found_items)
        ]:
            button = MDRaisedButton(
                text=btn_text,
                size_hint_x=0.8,
                pos_hint={"center_x": 0.5}
            )
            button.bind(on_release=callback)
            layout.add_widget(button)

        self.screen.add_widget(layout)
        return self.screen

    def show_report_form(self, instance):
        self.description_input = MDTextField(
            hint_text="Item Description",
            size_hint_x=0.95,
            pos_hint={"center_x": 0.5}
        )
        self.date_input = MDTextField(
            hint_text="Date and Time Lost",
            size_hint_x=0.95,
            pos_hint={"center_x": 0.5}
        )
        self.comment_input = MDTextField(
            hint_text="Additional Comments",
            multiline=True,
            size_hint_x=0.95,
            pos_hint={"center_x": 0.5}
        )

        content = MDBoxLayout(
            orientation='vertical',
            spacing=15,
            padding=(10, 20),
            adaptive_height=True
        )

        for field in [self.description_input, self.date_input, self.comment_input]:
            content.add_widget(field)

        scroll = ScrollView(size_hint=(1, None), size=(self.screen.width, 300))
        scroll.add_widget(content)

        self.report_dialog = MDDialog(
            title="Report Lost Item",
            type="custom",
            content_cls=scroll,
            buttons=[
                MDRaisedButton(text="Attach", on_release=self.select_file),
                MDRaisedButton(text="Submit", on_release=self.submit_report),
                MDRaisedButton(text="Back", on_release=lambda x: self.report_dialog.dismiss())
            ],
        )
        self.report_dialog.open()

    def select_file(self, instance):
        self.file_manager = MDFileManager(
            exit_manager=self.exit_file_manager,
            select_path=self.select_path,
        )
        self.file_manager.show("/")

    def exit_file_manager(self, *args):
        self.file_manager.close()

    def select_path(self, path):
        self.exit_file_manager()
        self.attached_file = path
        print(f"Selected file: {path}")

    def submit_report(self, instance):
        description = self.description_input.text
        date = self.date_input.text

        if not description or not date:
            self.show_dialog("Error", "Please fill all required fields.")
            return

        self.show_dialog("Success", "Report submitted successfully.")
        self.report_dialog.dismiss()

    def show_found_items(self, instance):
        found_list = MDBoxLayout(orientation='vertical', padding=20, spacing=15)

        # Δημιουργία MDCard για το πορτοφόλι
        card = MDCard(
            orientation="vertical",
            size_hint=(None, None),
            size=("280dp", "150dp"),
            pos_hint={"center_x": 0.5},
            padding=10,
            spacing=10,
        )
        
        # Προσθήκη περιγραφής του αντικειμένου στο card
        card.add_widget(MDLabel(text="Found: Wallet - 2025-04-11", halign="center"))
        
        # Δημιουργία κουμπιού Identify μέσα στο card
        identify_button = MDRaisedButton(text="Identify", size_hint_x=0.6, pos_hint={"center_x": 0.5})
        identify_button.bind(on_release=lambda x: self.show_dialog("Identified", "You identified the Wallet!"))
        card.add_widget(identify_button)

        # Δημιουργία κουτιού που περιλαμβάνει το κουμπί Back
        buttons_layout = MDBoxLayout(
            orientation="horizontal",
            spacing=20,
            size_hint=(1, None),
            height="50dp",
            pos_hint={"center_x": 0.5}
        )

        back_button = MDRaisedButton(
            text="Back", size_hint_x=0.45, pos_hint={"center_y": 0.5}, on_release=lambda x: self.found_popup.dismiss()
        )

        buttons_layout.add_widget(back_button)

        # Κουτί για το "Found Items" που περιλαμβάνει το παρακάτω
        found_box = MDBoxLayout(
            orientation="vertical",
            spacing=20,
            size_hint=(1, None),
            height="250dp",
            pos_hint={"center_x": 0.5},
            padding=20
        )

        # Τίτλος "Found Items" (εμφανίζεται μόνο μία φορά στην κορυφή)
        found_title = MDLabel(
            text="Found Items",
            halign="center",
            font_style="H5",
            size_hint_y=None,
            height=40
        )

        found_box.add_widget(found_title)  # Προσθήκη του τίτλου στο κουτί
        found_box.add_widget(card)         # Προσθήκη του card με τα αντικείμενα
        found_box.add_widget(buttons_layout)

        # Δημιουργία και προσθήκη του κουμπιού "Back" στην περιοχή του layout
        self.found_popup = MDDialog(
            title="Found Items",  # Δεν χρειάζεται να επαναλάβεις το "Found Items" εδώ
            type="custom",
            content_cls=found_box,
            buttons=[],  # Δεν προσθέτουμε επιπλέον buttons εδώ γιατί έχουμε ήδη το buttons_layout
        )
        self.found_popup.open()

    def show_dialog(self, title, text):
        dialog = MDDialog(
            title=title,
            text=text,
            buttons=[MDRaisedButton(text="OK", on_release=lambda x: dialog.dismiss())]
        )
        dialog.open()


if __name__ == "__main__":
    LostItemsApp().run()
