import flet as ft
import requests
import json


class on_off(ft.UserControl):
    def __init__(self, num) -> None:
        super().__init__()
        self.num = num

    def build(self):
        self.on_off = ft.Switch(label="", on_change=self.switch_change,
                                width=100, height=60, value=bool(self.num))
        self.display_view = ft.Row(
            alignment="center",
            controls=[
                ft.Text(value="开关", size=22),
                self.on_off,
            ],
        )

        return self.display_view

    def switch_change(self, e):
        requests.post("http://81.68.216.118:9094/api/post/airset/"+"onoff",
                      json={"num": int(self.on_off.value)})
        self.num = int(self.on_off.value)
        pass


class Counter(ft.UserControl):
    def __init__(self, name, num, apiname) -> None:
        self.apiname = apiname
        self.name = name
        self.num = num
        super().__init__()

    def build(self):
        self.txt_number = ft.TextField(
            value=str(self.num), text_align=ft.TextAlign.CENTER, width=60, text_size=20, height=40, border=ft.InputBorder.UNDERLINE, keyboard_type=ft.KeyboardType.NUMBER, read_only=True)
        self.display_view = ft.Row(
            alignment="center",
            controls=[
                ft.Text(value=self.name, size=20),
                ft.IconButton(ft.icons.REMOVE, on_click=self.minus_click),
                self.txt_number,
                ft.IconButton(ft.icons.ADD, on_click=self.plus_click),
            ],
        )

        return self.display_view

    def minus_click(self, e):
        self.txt_number.value = str(int(self.txt_number.value) - 1)
        requests.post("http://81.68.216.118:9094/api/post/airset/"+self.apiname,
                      json={"num": int(self.txt_number.value)})
        super().update()

    def plus_click(self, e):
        self.txt_number.value = str(int(self.txt_number.value) + 1)
        requests.post("http://81.68.216.118:9094/api/post/airset/"+self.apiname,
                      json={"num": int(self.txt_number.value)})
        super().update()


class Modeset(ft.UserControl):
    def __init__(self, name, num, apiname) -> None:
        self.modetonum = {'自动': 0, '除湿': 1, '制冷': 2, '送风': 3, '制热': 4}
        self.numtomode = {0: '自动', 1: '除湿', 2: '制冷', 3: '送风', 4: '制热'}
        self.apiname = apiname
        self.name = name
        self.num = num
        super().__init__()

    def build(self):
        self.dd = ft.Dropdown(
            width=100,
            on_change=self.dd_change,
            options=[
                ft.dropdown.Option("自动"),
                ft.dropdown.Option("除湿"),
                ft.dropdown.Option("制冷"),
                ft.dropdown.Option("送风"),
                ft.dropdown.Option("制热"),
            ],
            value=self.numtomode[self.num],
            text_size=18,
            alignment=ft.alignment.center,
        )
        self.display_view = ft.Row(
            alignment="center",
            controls=[
                ft.Text(value=self.name+'        ', size=20),
                self.dd,
            ],
        )
        return self.display_view

    def dd_change(self, e):
        requests.post("http://81.68.216.118:9094/api/post/airset/mode",
                      json={"num": self.modetonum[self.dd.value]})
        print(self.dd.value)


class MainApp(ft.UserControl):
    def build(self):
        self.SwitchButton = ft.IconButton(
            icon=ft.icons.PAUSE_CIRCLE_FILLED_ROUNDED, icon_color="blue400", icon_size=20)
        x = requests.get("http://81.68.216.118:9094/api/get/airset")
        if (x.status_code == 200):
            x = x.json()
        else:
            x = {"temp": 24, "speed": 5, "pref": 1, "mode": 3, "on_off": 1}
        self.counters = ft.Column(alignment="center", controls=[])
        self.counters.controls.append(on_off(x["on_off"]))
        self.counters.controls.append(Counter("温度", x["temp"], "temp"))
        self.counters.controls.append(Counter("风速", x["speed"], "speed"))
        self.counters.controls.append(Modeset("模式", x["mode"], "mode"))
        self.display_view = self.counters

        return self.display_view


class here(ft.UserControl):
    def __init__(self, n):
        self.app = MainApp()

    def build(self):
        return


def main(page: ft.Page):
    page.title = "空调控制"
    page.window_width = 260
    page.window_height = 300
    page.horizontal_alignment = "center"
    page.scroll = "adaptive"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.update()

    app = MainApp()
    page.add(ft.Column(
        controls=[
            ft.Container(
                alignment=ft.alignment.center,
                content=app
            )
        ]
    ))
    page.update()

    page.add(ft.Column(
        controls=[
            ft.Container(
                alignment=ft.alignment.center,
                content=app
            )
        ]
    ))


if __name__ == "__main__":
    ft.app(target=main)
