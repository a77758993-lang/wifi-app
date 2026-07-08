from kivy.app import App
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView


class WifiScannerApp(App):

    def build(self):
        self.layout = BoxLayout(orientation="vertical", padding=20, spacing=10)
        title = Label(
            text="📡 اسکنر زنده وای‌فای",
            font_size="20sp",
            size_hint_y=None,
            height=50,
        )
        self.layout.add_widget(title)
        self.scroll = ScrollView()
        self.result_label = Label(
            text="در حال اسکن...", font_size="16sp", size_hint_y=None
        )
        self.result_label.bind(
            texture_size=lambda instance, value: setattr(
                instance, "height", value[1]
            )
        )
        self.scroll.add_widget(self.result_label)
        self.layout.add_widget(self.scroll)
        self.request_android_permissions()
        Clock.schedule_interval(self.scan_wifi, 3)
        return self.layout

    def request_android_permissions(self):
        try:
            from android.permissions import Permission, request_permissions

            request_permissions(
                [Permission.ACCESS_FINE_LOCATION, Permission.ACCESS_WIFI_STATE]
            )
        except ImportError:
            pass

    def scan_wifi(self, dt):
        try:
            from jnius import autoclass

            PythonActivity = autoclass("org.kivy.android.PythonActivity")
            Context = autoclass("android.content.Context")
            wifi_manager = PythonActivity.mActivity.getSystemService(
                Context.WIFI_SERVICE
            )
            wifi_manager.startScan()
            scan_results = wifi_manager.getScanResults()
            results_text = ""
            for i in range(scan_results.size()):
                item = scan_results.get(i)
                ssid = item.SSID if item.SSID else "[شبکه مخفی]"
                results_text += f"📶 {ssid}\n   قدرت سیگنال: {item.level} dBm\n\n"
            self.result_label.text = (
                results_text if results_text else "هیچ شبکه‌ای یافت نشد."
            )
        except Exception:
            self.result_label.text = "در حال راه‌اندازی سرویس وای‌فای..."


if __name__ == "__main__":
    WifiScannerApp().run()
