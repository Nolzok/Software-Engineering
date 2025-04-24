from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.dialog import MDDialog
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.screen import MDScreen
from kivymd.uix.card import MDCard
from kivymd.uix.scrollview import ScrollView

class SearchEventsApp(MDApp):
    
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

        # Title
        title = MDLabel(
            text="Event Search",
            halign="center",
            font_style="H4",
            size_hint_y=None,
            height=60
        )
        layout.add_widget(title)

        # Search button
        search_button = MDRaisedButton(
            text="Search Events",
            size_hint_x=0.8,
            pos_hint={"center_x": 0.5}
        )
        search_button.bind(on_release=self.show_search_filters)
        layout.add_widget(search_button)

        self.screen.add_widget(layout)
        return self.screen

    def show_search_filters(self, instance):
        # Search filters and categories
        categories = ["Music", "Art", "Sports", "Technology", "Food"]
        
        filters_layout = MDBoxLayout(
            orientation='vertical',
            spacing=15,
            padding=20,
            adaptive_height=True
        )

        filter_label = MDLabel(
            text="Filter Events by Category",
            halign="center",
            font_style="H6"
        )
        filters_layout.add_widget(filter_label)

        for category in categories:
            button = MDRaisedButton(
                text=category,
                size_hint_x=0.8,
                pos_hint={"center_x": 0.5}
            )
            button.bind(on_release=lambda btn, category=category: self.search_by_category(category))
            filters_layout.add_widget(button)

        search_field = MDTextField(
            hint_text="Search by event name",
            size_hint_x=0.9,
            pos_hint={"center_x": 0.5}
        )
        filters_layout.add_widget(search_field)

        search_button = MDRaisedButton(
            text="Search",
            size_hint_x=0.8,
            pos_hint={"center_x": 0.5}
        )
        search_button.bind(on_release=lambda btn, search_field=search_field: self.search_by_keyword(search_field.text))
        filters_layout.add_widget(search_button)

        self.filters_dialog = MDDialog(
            title="Search Filters",
            type="custom",
            content_cls=filters_layout,
            buttons=[MDRaisedButton(text="Close", on_release=lambda x: self.filters_dialog.dismiss())],
        )
        self.filters_dialog.open()

    def search_by_category(self, category):
        # Example events by category
        events = {
            "Music": ["Rock Concert", "Pop Music Festival", "Jazz Night"],
            "Art": ["Art Exhibition", "Gallery Walk", "Sculpture Showcase"],
            "Sports": ["Football Match", "Basketball Tournament", "Tennis Open"],
            "Technology": ["Tech Conference", "AI Seminar", "VR Workshop"],
            "Food": ["Food Festival", "Vegan Cooking Class", "BBQ Party"]
        }

        result_events = events.get(category, [])
        if result_events:
            self.show_event_cards(result_events)
        else:
            self.show_dialog("Search Results", f"No events found in the {category} category.")
        self.filters_dialog.dismiss()

    def search_by_keyword(self, keyword):
        # Example events for keyword search
        events = {
            "Music": ["Rock Concert", "Pop Music Festival", "Jazz Night"],
            "Art": ["Art Exhibition", "Gallery Walk", "Sculpture Showcase"],
            "Sports": ["Football Match", "Basketball Tournament", "Tennis Open"],
            "Technology": ["Tech Conference", "AI Seminar", "VR Workshop"],
            "Food": ["Food Festival", "Vegan Cooking Class", "BBQ Party"]
        }

        result_events = []
        for category, event_list in events.items():
            for event in event_list:
                if keyword.lower() in event.lower():
                    result_events.append(f"{event} ({category})")

        if result_events:
            self.show_event_cards(result_events)
        else:
            self.show_dialog("Search Results", "No events found for the given keyword.")

        self.filters_dialog.dismiss()

    def show_event_cards(self, events):
        # Create cards for events with buttons
        event_cards_layout = MDBoxLayout(
            orientation='vertical',
            spacing=10,
            size_hint=(1, None),
            height=len(events) * 170,  # Height depends on the number of events
            padding=20
        )

        # Create a scrollable area for event cards
        scroll_view = ScrollView(
            size_hint=(1, None),
            height=500  # Set a fixed height for the scroll area
        )
        scroll_view.add_widget(event_cards_layout)

        for event in events:
            card = MDCard(
                orientation="vertical",
                size_hint=(None, None),
                size=("280dp", "150dp"),
                pos_hint={"center_x": 0.5},
                padding=10,
                spacing=10,
            )

            card.add_widget(MDLabel(text=event, halign="center"))

            buttons_layout = MDBoxLayout(
                orientation="horizontal",
                spacing=10,
                size_hint=(1, None),
                height="50dp",
                pos_hint={"center_x": 0.5}
            )

            volunteer_button = MDRaisedButton(text="Volunteer Form", size_hint_x=0.3, pos_hint={"center_y": 0.5})
            participant_button = MDRaisedButton(text="Participant Form", size_hint_x=0.3, pos_hint={"center_y": 0.5})
            details_button = MDRaisedButton(text="Details", size_hint_x=0.3, pos_hint={"center_y": 0.5})

            buttons_layout.add_widget(volunteer_button)
            buttons_layout.add_widget(participant_button)
            buttons_layout.add_widget(details_button)

            card.add_widget(buttons_layout)
            event_cards_layout.add_widget(card)

        self.event_cards_dialog = MDDialog(
            title="Event Results",
            type="custom",
            content_cls=scroll_view,
            buttons=[MDRaisedButton(text="Close", on_release=lambda x: self.event_cards_dialog.dismiss())],
        )
        self.event_cards_dialog.open()

    def show_dialog(self, title, text):
        dialog = MDDialog(
            title=title,
            text=text,
            buttons=[MDRaisedButton(text="OK", on_release=lambda x: dialog.dismiss())]
        )
        dialog.open()

if __name__ == "__main__":
    SearchEventsApp().run()
