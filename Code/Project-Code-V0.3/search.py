from kivy.metrics import dp
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.label import MDLabel
from kivymd.uix.list import OneLineListItem
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.dialog import MDDialog
from kivymd.uix.screen import MDScreen
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.card import MDCard

# Dummy database
event_db = {
    "Μουσική": [
        {"title": "Rock Festival", "details": "Συναυλία ροκ, 15 Ιουνίου, 10€"},
        {"title": "Jazz Night", "details": "Βραδιά Jazz, 20 Ιουνίου, 15€"},
    ],
    "Αθλητισμός": [
        {"title": "Μαραθώνιος", "details": "Αγώνας δρόμου, 1 Ιουλίου, δωρεάν"},
        {"title": "Αγώνας Ποδοσφαίρου", "details": "Τοπική ομάδα, 10€"},
    ],
}

filters = {
    "Ημερομηνία": lambda e: "Ιουνίου" in e["details"],
    "Τιμή": lambda e: "δωρεάν" in e["details"] or "10€" in e["details"],
}


class SearchApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Indigo"
        self.screen = MDScreen()

        main_layout = MDBoxLayout(orientation='vertical', spacing=dp(10))

        # Top row
        top_row = MDBoxLayout(size_hint_y=None, height=dp(60), spacing=dp(10), padding=dp(10))
        self.search_bar = MDTextField(hint_text="Αναζήτηση event...", mode="rectangle", size_hint_x=0.6)
        search_btn = MDRaisedButton(text="Αναζήτηση", on_release=self.search_keywords)
        self.filter_btn = MDFlatButton(text="Φίλτρα", on_release=self.show_filters)
        top_row.add_widget(self.search_bar)
        top_row.add_widget(search_btn)
        top_row.add_widget(self.filter_btn)

        self.results_layout = MDBoxLayout(orientation="vertical", spacing=dp(10), size_hint_y=None)
        self.results_layout.bind(minimum_height=self.results_layout.setter('height'))

        scroll_view = MDScrollView()
        scroll_view.add_widget(self.results_layout)

        main_layout.add_widget(top_row)
        main_layout.add_widget(scroll_view)
        self.screen.add_widget(main_layout)

        return self.screen

    def search_keywords(self, instance):
        self.results_layout.clear_widgets()
        keyword = self.search_bar.text.lower()
        matched_categories = set()

        # Μερική αντιστοίχιση με βάση το όνομα της κατηγορίας
        for category in event_db:
            if keyword in category.lower():
                matched_categories.add(category)

        # Αναζήτηση λέξης-κλειδιού στους τίτλους ή λεπτομέρειες των events
        for category, events in event_db.items():
            for event in events:
                if keyword in event["title"].lower() or keyword in event["details"].lower():
                    matched_categories.add(category)

        if not matched_categories:
            self.results_layout.add_widget(MDLabel(text="Δεν βρέθηκαν κατηγορίες.", halign="center", size_hint_y=None, height=dp(40)))
            return

        # Εμφάνιση κάθε κατηγορίας ως MDCard
        for cat in matched_categories:
            card = MDCard(orientation="vertical", padding=dp(10), size_hint_y=None, height=dp(100), md_bg_color=self.theme_cls.primary_light)
            box = MDBoxLayout(orientation="vertical")
            label = MDLabel(text=f"[b]{cat}[/b]", markup=True, font_style="H6", halign="center")
            btn = MDRaisedButton(text="Προβολή", size_hint=(1, None), height=dp(40), on_release=lambda x, c=cat: self.show_events(c))
            box.add_widget(label)
            box.add_widget(btn)
            card.add_widget(box)
            self.results_layout.add_widget(card)

    def show_events(self, category):
        self.results_layout.clear_widgets()
        events = event_db.get(category, [])

        if not events:
            self.results_layout.add_widget(MDLabel(text="Δεν βρέθηκαν events.", halign="center", size_hint_y=None, height=dp(40)))
            return

        for event in events:
            item = OneLineListItem(text=event["title"], on_release=lambda x, e=event: self.show_details(e))
            self.results_layout.add_widget(item)

    def show_details(self, event):
        self.dialog = MDDialog(
            title=event["title"],
            text=event["details"],
            buttons=[MDFlatButton(text="OK", on_release=lambda x: self.dialog.dismiss())]
        )
        self.dialog.open()

    def show_filters(self, instance):
        menu_items = [{"text": k, "on_release": lambda x=k: self.apply_filter(x)} for k in filters]
        self.menu = MDDropdownMenu(caller=self.filter_btn, items=menu_items, width_mult=4)
        self.menu.open()

    def apply_filter(self, filter_name):
        self.menu.dismiss()
        self.results_layout.clear_widgets()
        filter_func = filters[filter_name]

        matched = []
        for category, events in event_db.items():
            for e in events:
                if filter_func(e):
                    matched.append(e)

        if not matched:
            self.results_layout.add_widget(MDLabel(text="Δεν βρέθηκαν events με το φίλτρο.", halign="center", size_hint_y=None, height=dp(40)))
            return

        for e in matched:
            item = OneLineListItem(text=e["title"], on_release=lambda x, ev=e: self.show_details(ev))
            self.results_layout.add_widget(item)


SearchApp().run()
