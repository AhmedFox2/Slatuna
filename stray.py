from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QAction, QMessageBox
from PyQt5.QtGui import QIcon
import slatuna_tk
import os,sys

loc = os.path.dirname(__file__)
os.chdir(loc)

def main():
    def load_stylesheet(file_path):
        with open(file_path, "r",encoding="utf-8") as file:
            return file.read()

    # دالة تنفيذ الإجراء عند النقر على أيقونة شريط النظام
    def on_tray_icon_click(reason):
        # تحقق من السبب
        if reason == QSystemTrayIcon.Trigger:
            slatuna_tk.main()
        
    # إنشاء تطبيق
    app = QApplication([])

    # تعيين النمط من ملف CSS خارجي
    css_file_path = f"{loc}/assets/data/style.css"  # تأكد من أن المسار صحيح لملف CSS
    app.setStyleSheet(load_stylesheet(css_file_path))

    # التأكد من وجود الأيقونة في المسار الصحيح
    icon_path = f"{loc}/assets/Imgs/icon.ico"  # يمكنك تغيير المسار هنا إذا كان ملف الأيقونة في مسار مختلف

    # إنشاء أيقونة شريط النظام
    trayIcon = QSystemTrayIcon(QIcon(icon_path), parent=app)

    # إنشاء قائمة السياق الخاصة بالأيقونة
    trayMenu = QMenu()

    # إضافة عناصر متعددة للقائمة
    open_slatuna = QAction("Open slatuna", trayMenu)
    open_slatuna.triggered.connect(lambda: slatuna_tk.main())
    trayMenu.addAction(open_slatuna)

    # إنشاء قائمة فرعية
    settingsbutton = QAction("Settings", trayMenu)
    settingsbutton.triggered.connect(lambda: slatuna_tk.settings(root= lambda: slatuna_tk.main()))
    trayMenu.addAction(settingsbutton)

    # إضافة فاصل في القائمة
    trayMenu.addSeparator()

    # إضافة عنصر لخروج التطبيق
    exitAction = QAction("Exit", trayMenu)
    exitAction.triggered.connect(app.quit)
    trayMenu.addAction(exitAction)

    # إعداد قائمة السياق للأيقونة
    trayIcon.setContextMenu(trayMenu)

    # ربط إشارة النقر بالإجراء
    trayIcon.activated.connect(on_tray_icon_click)

    # عرض الأيقونة في شريط النظام
    trayIcon.show()

    # تشغيل التطبيق
    app.exec_()