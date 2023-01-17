import flet as ft
import time
import requests


def main(page):
    ss=[0,0]
    ee=[0,0]
    page.title = "空调控制"

    week = ft.Text(
        "周一",
        size=30,
    )
    s_time = ft.Text("00:00", size=30)
    e_time = ft.Text("00:00", size=30)

    def dropdown_changed(e):
        week.value = dd.value
        print(week.value)
        page.update()

    def slider_changed(e):
        if swi.value == True:
            s_time.value = f"{str(int(hour.value))}:{str(int(min.value))}"
            ss=[f"{int(hour.value)}",f"{int(min.value)}"]
        else:
            e_time.value = f"{str(int(hour.value))}:{str(int(min.value))}"
            ee=[f"{int(hour.value)}",f"{int(min.value)}"]
        page.update()

    def add_clicked(e):
        t = ft.Text(
            color="blue200",
            size=30,
        )
        t.value = f"{week.value} {s_time.value}->{e_time.value}"
        m = ft.Row(
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                t,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )
        cc.controls.append(m)
        url = "http://81.68.216.118:9094/api/post/timeon/add"
        if week.value=="周一": num=1
        if week.value=="周二": num=2
        if week.value=="周三": num=3
        if week.value=="周四": num=4
        if week.value=="周五": num=5
        if week.value=="周六": num=6
        if week.value=="周日": num=7
        datas={"Weekday":num,"H_start":ss[0],"M_start":ss[1],"H_end":ee[0],"M_end":ee[1]}
        response=requests.post(url,data=datas)
        page.update()

    def add(a):
        week_=["周一","周二","周三","周四","周五","周六","周日"]
        url = "http://81.68.216.118:9094/api/get/timeon/"
        url+=str(a)
        response = requests.get(url)
        print(response.text)
        for i in response.json()["time"]:
            t = ft.Text(
                color="blue200",
                size=30,
            )
            t.value = f"{week_[a-1]} {i['H_start']}:{i['M_start']}->{i['H_end']}:{i['M_end']}"
            m = ft.Row(
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    t,
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            )
            cc.controls.append(m)
        page.update()

    def delete_clicked(e):
        for i in cc.controls:
            if i.controls[0].value[1]==week.value[1]:
                cc.controls.remove(i)
        for i in cc.controls:
            if i.controls[0].value[1]==week.value[1]:
                cc.controls.remove(i)
        url = "http://81.68.216.118:9094/api/post/timeon/deleteall/"
        if week.value=="周一": num=1
        if week.value=="周二": num=2
        if week.value=="周三": num=3
        if week.value=="周四": num=4
        if week.value=="周五": num=5
        if week.value=="周六": num=6
        if week.value=="周日": num=7
        url+=str(num)
        datas={}
        response=requests.post(url,data=datas)
        page.update()

    biaoti = ft.Text(
        value="空调时间控制",
        size=60,
        color="blue400",
        text_align=ft.TextAlign.CENTER,
    )

    r = ft.Row(
        [biaoti],
        alignment=ft.MainAxisAlignment.CENTER,
    )

    swi = ft.Switch(label="", value=True)
    dd = ft.Dropdown(
        on_change=dropdown_changed,
        label="做个选择吧",
        options=[
            ft.dropdown.Option("周一"),
            ft.dropdown.Option("周二"),
            ft.dropdown.Option("周三"),
            ft.dropdown.Option("周四"),
            ft.dropdown.Option("周五"),
            ft.dropdown.Option("周六"),
            ft.dropdown.Option("周日"),
        ],
    )

    rr = ft.Row(
        [dd, swi],
        alignment=ft.MainAxisAlignment.CENTER,
    )

    hour_t = ft.Row(
        controls=[
            ft.Text(
                "时",
                size=30,
                color="green400",
                text_align=ft.TextAlign.CENTER,
            ),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
    )
    hour = ft.Slider(
        min=0, max=23, divisions=23, label="{value}", on_change=slider_changed
    )
    min_t = ft.Row(
        controls=[
            ft.Text(
                "分",
                size=30,
                color="green400",
                text_align=ft.TextAlign.CENTER,
            ),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
    )
    min = ft.Slider(
        min=0, max=59, divisions=59, label="{value}", on_change=slider_changed
    )

    c = ft.Column(controls=[rr, hour_t, hour, min_t, min])

    kong = ft.Text(" ")

    btn = ft.FloatingActionButton(icon=ft.icons.ADD, on_click=add_clicked)
    fbtn = ft.FloatingActionButton(icon=ft.icons.DELETE, on_click=delete_clicked)

    rrr = ft.Row(
        [
            btn,
            fbtn,
        ],
        alignment=ft.MainAxisAlignment.CENTER,
    )

    r_ = ft.Row(
        controls=[
            week,
            kong,
            s_time,
            ft.Text("  ->  ", size=30),
            kong,
            e_time,
        ],
        alignment=ft.MainAxisAlignment.CENTER,
    )

    cc = ft.ListView(
        controls=[],
        expand=True,
        spacing=10,
        auto_scroll=True,
    )
    
    for i in range(1,8,1):
        print(i)
        add(i)
    
    page.add(r, c, r_, cc, rrr)


ft.app(target=main)
