from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt, QSize
import webbrowser
import subprocess
from uuid import uuid1
import minecraft_launcher_lib

app = QApplication([])

# === Основное окно ===
window = QWidget()
window.setWindowTitle("Arm launcher")
window.setFixedSize(1400, 900)
window.setStyleSheet(open("style.qss", "r").read())
window.setWindowIcon(QIcon("img/creeper.jpg"))

main_layout = QHBoxLayout(window)
main_layout.setContentsMargins(0, 0, 0, 0)
main_layout.setSpacing(0)

# === Левая панель навигации ===
left_panel = QWidget()
left_panel.setFixedWidth(100)
left_panel.setObjectName("leftPanel")
left_layout = QVBoxLayout(left_panel)
left_layout.setContentsMargins(0, 30, 0, 30)
left_layout.setSpacing(30)
left_layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)

logo = QLabel()
logo.setPixmap(QPixmap("img/creeper.jpg").scaled(50, 50, Qt.KeepAspectRatio, Qt.SmoothTransformation))
logo.setAlignment(Qt.AlignCenter)
logo.setObjectName("logo")

btn_home = QPushButton()
btn_home.setIcon(QIcon("img/home.png"))
btn_home.setIconSize(QSize(50, 50))
btn_home.setObjectName("navButton")

btn_servers = QPushButton()
btn_servers.setIcon(QIcon("img/servers.png"))
btn_servers.setIconSize(QSize(40, 40))
btn_servers.setObjectName("navButton")

btn_settings = QPushButton()
btn_settings.setIcon(QIcon("img/settings.png"))
btn_settings.setIconSize(QSize(40, 40))
btn_settings.setObjectName("navButton")

left_layout.addWidget(logo)
left_layout.addWidget(btn_home)
left_layout.addWidget(btn_servers)
left_layout.addWidget(btn_settings)

# === Центральная часть (контент) ===
content = QWidget()
content.setObjectName("content")
content_layout = QHBoxLayout(content)
content_layout.setContentsMargins(50, 50, 50, 50)
content_layout.setSpacing(40)

# === Левая сторона контента ===
center_left = QVBoxLayout()
center_left.setAlignment(Qt.AlignTop)

title = QLabel('<span style="color: green;">Arm</span> launcher')
title.setObjectName("title")
subtitle = QLabel("лаунчер для майнкрафта")
subtitle.setObjectName("subtitle")

center_left.addWidget(title)
center_left.addWidget(subtitle)
center_left.addSpacing(20)

# === QStackedWidget для страниц ===
pages = QStackedWidget()

# ---------------------
# === Страница Home ===
# ---------------------
nickname_input = QLineEdit()
nickname_input.setPlaceholderText("Никнейм")
nickname_input.setObjectName("textField")

version_combo = QComboBox()
version_combo.setObjectName("comboBox")
for version in minecraft_launcher_lib.utils.get_version_list():
    version_combo.addItem(version["id"])

play_button = QPushButton("Играть")
play_button.setObjectName("playButton")

def start_minecraft():
    minecraft_directory = minecraft_launcher_lib.utils.get_minecraft_directory().replace("minecraft", "Armlauncher")
    version = version_combo.currentText()
    minecraft_launcher_lib.install.install_minecraft_version(versionid=version, minecraft_directory=minecraft_directory)

    nickname = nickname_input.text()
    if not nickname:
        return

    options = {
        "username": nickname,
        "uuid": str(uuid1()),
        "token": ""
    }

    subprocess.call(minecraft_launcher_lib.command.get_minecraft_command(version=version, minecraft_directory=minecraft_directory, options=options))

play_button.clicked.connect(start_minecraft)

about_button = QPushButton("Подробнее о лаунчере")
about_button.setObjectName("aboutButton")
about_button.clicked.connect(lambda: webbrowser.open("https://github.com/armen1357"))

home_page = QWidget()
home_layout = QVBoxLayout(home_page)
home_layout.addWidget(nickname_input)
home_layout.addWidget(version_combo)
home_layout.addWidget(play_button)
home_layout.addWidget(about_button)

pages.addWidget(home_page)

# ------------------------
# === Страница Server ===
# ------------------------
servers = ["mc.reallworld.ru", "funtime.su", "mc.raidmine.com", "mineblaze.net"]
server_urls = {
    "mc.reallworld.ru": "https://reallyworld.ru/",
    "funtime.su": "https://funtime.su/",
    "mc.raidmine.com": "https://raidmine.com/",
    "mineblaze.net": "https://mineblaze.net/"
}

server_page = QWidget()
server_layout = QVBoxLayout(server_page)

for srv in servers:
    row = QHBoxLayout()
    label = QLabel(srv)
    label.setObjectName("serverLabel")
    btn = QPushButton("Подробнее")
    btn.setObjectName("serverButton")
    btn.clicked.connect(lambda _, server=srv: webbrowser.open(server_urls[server]))
    row.addWidget(label)
    row.addStretch()
    row.addWidget(btn)

    frame = QWidget()
    frame.setLayout(row)
    frame.setObjectName("serverFrame")
    server_layout.addWidget(frame)

pages.addWidget(server_page)

# ----------------------------
# === Страница Settings ===
# ----------------------------
settings_page = QWidget()
settings_layout = QVBoxLayout(settings_page)
settings_layout.setAlignment(Qt.AlignTop)

# Язык
lang_label = QLabel("Язык")
lang_label.setObjectName("subtitle")
lang_combo = QComboBox()
lang_combo.addItems(["Русский", "Руссиан", "RUSSIAN", "RU", "Нормальный"])
lang_combo.setObjectName("comboBox_laun")

lang_container = QWidget()
lang_container_layout = QVBoxLayout(lang_container)
lang_container_layout.setSpacing(10)
lang_container_layout.addWidget(lang_label)
lang_container_layout.addWidget(lang_combo)

future_interface = QLabel("Добавим в будущем")
future_interface.setObjectName("future_interface")

# Тема
theme_label = QLabel("Тема")
theme_label.setObjectName("subtitle2")

theme_row = QHBoxLayout()
white_circle = QPushButton()
white_circle.setFixedSize(30, 30)
white_circle.setStyleSheet("background-color: white; border-radius: 15px;")
black_circle = QPushButton()
black_circle.setFixedSize(30, 30)
black_circle.setStyleSheet("background-color: black; border-radius: 15px;")

theme_row.addWidget(white_circle)
theme_row.addSpacing(20)
theme_row.addWidget(black_circle)

theme_container = QWidget()
theme_container_layout = QVBoxLayout(theme_container)
theme_container_layout.setSpacing(10)
theme_container_layout.addWidget(theme_label)
theme_container_layout.addLayout(theme_row)

settings_layout.addWidget(lang_container)
settings_layout.addWidget(future_interface)
settings_layout.addWidget(theme_container)

pages.addWidget(settings_page)

# === Обработчики переключения страниц ===
btn_home.clicked.connect(lambda: pages.setCurrentIndex(0))
btn_servers.clicked.connect(lambda: pages.setCurrentIndex(1))
btn_settings.clicked.connect(lambda: pages.setCurrentIndex(2))

# === Правая часть (персонаж) ===
character = QLabel()
character.setPixmap(QPixmap("img/skin.png").scaled(550, 800, Qt.KeepAspectRatio, Qt.SmoothTransformation))
character.setAlignment(Qt.AlignBottom | Qt.AlignRight)

# === Финальный макет ===
center_left.addWidget(pages)
content_layout.addLayout(center_left)
content_layout.addWidget(character)

main_layout.addWidget(left_panel)
main_layout.addWidget(content)

window.show()
app.exec_()