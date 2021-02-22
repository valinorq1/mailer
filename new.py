# -*- coding: utf-8 -*-
import time
import os
import sys

from PyQt5.QtWidgets import QFileDialog
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import *
from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon

from ui import Ui_MainWindow
from utils import split_list, captcha_three


class MailSender(QtWidgets.QMainWindow):
    def __init__(self):
        super(MailSender, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.init_UI()

        #  chrome driver path & options
        driver_path = os.getcwd()
        chrome_options = Options()
        chrome_options.add_argument('--log-level=3')
        chrome_options.add_argument("--start-maximized")
        self.driver = webdriver.Chrome(options=chrome_options,
                                       executable_path=os.getcwd() + './chromedriver')
        #self.driver = webdriver.Chrome(options=chrome_options, executable_path='/Users/aleksandrmoskalenko/Downloads/mailer/chromedriver')

    def init_UI(self):
        self.setWindowIcon(QIcon('mail.png'))
        self.ui.start_work.clicked.connect(self.main)
        self.ui.start_work.hide()
        self.ui.check_field.clicked.connect(self.check_all_field_data)
        self.ui.file_1_button.clicked.connect(self.load_first_file_path)
        self.ui.file_2_button_2.clicked.connect(self.load_second_file_path)
        self.ui.file_3_button.clicked.connect(self.load_third_file_path)
        self.ui.file_4_button.clicked.connect(self.load_forth_file_path)

    def close_win(self):
        self.close()

    def write_logs(self, log_text, status_color):
        if status_color == 'warning':
            self.ui.logs_data.appendHtml(
                f"<span style=\" font-size:10pt; font-weight:600; color:#ff0000;\" >{log_text} "
                f"<br />________________________</span>")
        elif status_color == 'success':
            self.ui.logs_data.appendHtml(
                f"<span style=\" font-size:10pt; font-weight:600; color:#169c16;\" >{log_text}"
                f"<br />________________________</span>")
        elif status_color == 'notif':
            self.ui.logs_data.appendHtml(
                f"<span style=\" font-size:10pt; font-weight:600; color:#169db8\" >{log_text}"
                f"<br />________________________</span>")

        else:
            self.ui.logs_data.appendHtml(
                f"<span style=\" font-size:10pt; font-weight:600; color:#e3b614;\" >{log_text}"
                f"<br />________________________</span>")

    def load_sender_list(self):
        sender = self.ui.send_from.toPlainText().split('\n')
        return sender

    def load_first_file_path(self):
        file_name, _ = QFileDialog.getOpenFileName(self, 'Open Image File',
                                                   "Image files (*.jpg *.jpeg *.gif,*.png, *.*)")
        self.ui.file_1.setText(file_name)

    def load_second_file_path(self):
        file_name, _ = QFileDialog.getOpenFileName(self, 'Open Image File',
                                                   "Image files (*.jpg *.jpeg *.gif,*.png, *.*)")
        self.ui.file_2.setText(file_name)

    def load_third_file_path(self):
        file_name, _ = QFileDialog.getOpenFileName(self, 'Open Image File',
                                                   "Image files (*.jpg *.jpeg *.gif,*.png, *.*)")
        self.ui.file_3.setText(file_name)

    def load_forth_file_path(self):
        file_name, _ = QFileDialog.getOpenFileName(self, 'Open Image File',
                                                   "Image files (*.jpg *.jpeg *.gif,*.png, *.*)")
        self.ui.file_4.setText(file_name)

    def load_receiver_list(self):
        receiver = self.ui.send_to.toPlainText().replace(' ', '').split('\n')
        return receiver

    def get_file_names(self):
        files = []
        if self.ui.file_1.text() == '':
            pass
        else:
            files.append(self.ui.file_1.text())

        if self.ui.file_2.text() == '':
            pass
        else:
            files.append(self.ui.file_2.text())

        if self.ui.file_3.text() == '':
            pass
        else:
            files.append(self.ui.file_3.text())

        if self.ui.file_4.text() == '':
            pass
        else:
            files.append(self.ui.file_4.text())

        for i in files:
            if '.' not in i:
                self.write_logs('Похоже где-то не указано разрешение файла..', 'info')
        return files

    def check_all_field_data(self):
        sender_email_list = self.load_sender_list()
        receiver_email_list = self.load_receiver_list()
        attachment_files = self.get_file_names()
        messages_subject = self.ui.message_subject.text()
        messages_text = self.ui.messages_text.toPlainText()
        attach_send_delay = int(self.ui.attach_delay.text())
        captcha_api_key = self.ui.captcha_api_key.text()

        if (len(sender_email_list) <= 0 or len(receiver_email_list) <= 0) or \
                (len(messages_subject) <= 0 or len(messages_text) <= 0) or (attach_send_delay <= 0) or \
                len(captcha_api_key) <= 0:
            self.write_logs('Похоже какое-то поле пустое(вложения можно оставить пустыми)', 'warning')
            self.ui.start_work.hide()

        elif sender_email_list and receiver_email_list and messages_subject \
                and messages_text and attach_send_delay >= 1:
            self.write_logs('Всё поля заполнены, можно начинать)', 'success')
            self.ui.start_work.show()

        if int(len(attachment_files)) < 0:
            self.write_logs('Внимание, письма будут без вложений. Вы не внесли никаких данных о вложениях', 'info')

    def my_send_mail(self, receiver, attach, subject, email_text, attach_send_delay, captcha_api_key):
        self.driver.find_element_by_xpath("//i[@class='b-toolbar__but__i'][contains(.,'Написать')]").click()
        time.sleep(3)
        #  Кому шлем

        to = self.driver.find_element_by_xpath("//input[contains(@name,'to')]")
        to.send_keys(receiver)
        to.send_keys(Keys.TAB)

        # тема
        subj = self.driver.find_element_by_xpath("//input[contains(@name,'subj')]")
        subj.send_keys(subject)
        subj.send_keys(Keys.TAB)
        # текст
        body_text = self.driver.find_element_by_xpath("//textarea[@aria-label='Тело письма']")
        body_text.send_keys(email_text)
        #  Вложения
        if len(attach) >= 1:
            for f in attach:
                self.driver.find_element_by_xpath("(//input[contains(@class,'file')])[1]").send_keys(f)
                #  .send_keys(f'/Users/aleksandrmoskalenko/Downloads/mailer/{f}')
                time.sleep(attach_send_delay)

        #  отправить
        self.driver.find_element_by_xpath("//input[contains(@name,'doit')]").click()
        time.sleep(3)
        if 'Чтобы отправить его, дождитесь завершения загрузки вложений или удалите их.' in self.driver.page_source:
            print('Похоже вложения не успели прогрузится, подождем загрузки(15 сек)')
            time.sleep(15)  # даем время на прогрузку
            try:
                #  закрываем окно с инфой о том, что не прогружены вложения
                webdriver.ActionChains(self.driver).send_keys(Keys.ESCAPE).perform()
                self.driver.find_element_by_xpath("//button[@data-lego='react'][contains(.,'Отправить')]").click()
                time.sleep(4)

            except NoSuchElementException:
                pass
                #  отправить
                #  self.driver.find_element_by_xpath("//button[@data-lego='react'][contains(.,'Отправить')]").click()
        if 'b-captcha' in self.driver.page_source:
            print('Поймали капчу')
            time.sleep(3)
            while True:
                captcha_solve_data = captcha_three(self.driver.page_source, captcha_api_key)
                time.sleep(5)
                # обрабатываем капчу
                captcha_input = self.driver.find_element_by_xpath("//input[contains(@name,'captcha_entered')]")
                captcha_input.send_keys(captcha_solve_data)
                #self.driver.find_element_by_xpath("(//input[@type='submit'])[3]").click()
                self.driver.find_element_by_xpath("(//input[contains(@name,'doit')])[1]").click()

                time.sleep(3)
                self.driver.find_element_by_xpath("//input[@name='doit']").click()
                time.sleep(3)
                if 'b-captcha' in self.driver.page_source:
                    print('Капча не верная, посылаем еще раз...')
                    time.sleep(5)
                    continue
                else:
                    break


        print(f'Отправили:{receiver}')
        time.sleep(3)

    def auth_mail(self, data_list, attach, subject, email_text, default_password_for_email,
                  attach_send_delay, captcha_api_key):
        for email, items in data_list.items():
            print(f'Авторизуемся с аккаунта: {email}')
            self.driver.get(
                'https://passport.yandex.ru/auth/welcome?from=mail&origin=hostroot_homer_auth_L_ru'
                '&retpath=https%3A%2F%2Fmail.yandex.ru%2F&backpath=https%3A%2F%2Fmail.yandex.ru%3Fnoretpath%3D1')
            time.sleep(5)
            if 'Выберите аккаунт для входа' in self.driver.page_source:
                self.driver.find_element_by_class_name('AddAccountButton-wrapper').click()
            self.driver.find_element_by_class_name('Textinput-Control').send_keys(email)  # поле логина
            self.driver.find_element_by_class_name('passp-sign-in-button').click()
            time.sleep(5)  # Ждем загрузки ебучего аякса
            src = self.driver.page_source
            if 'current-password' in src:
                self.driver.find_element_by_class_name('Textinput-Control').send_keys(default_password_for_email)
                self.driver.find_element_by_class_name('Button2').click()
                time.sleep(5)
            try:
                self.driver.find_element_by_xpath(
                    '/html/body/div/div/div[2]/div[2]/div/div/div[2]/div[3]/div/div/form/div[3]/button').click()
                time.sleep(7)
            except NoSuchElementException:
                pass
            if 'Все письма по полочкам' in self.driver.page_source:
                try:
                    self.driver.find_element_by_xpath(
                        '//*[@id="nb-1"]/body/div[7]/div/div/div/div/div/div/div/div[2]/div[4]/button[1]').click()
                except NoSuchElementException:
                    try:
                        self.driver.find_element_by_class_name('mail-Wizard-Close').click()
                    except NoSuchElementException:
                        self.driver.find_element_by_class_name('mail-Layout-Inner').send_keys(Keys.ESCAPE)
            self.driver.get('https://mail.yandex.ru/lite/')
            for item in items:
                if 'Написать' in self.driver.page_source:
                    self.my_send_mail(item, attach, subject, email_text, attach_send_delay, captcha_api_key)

        self.ui.logs_data.appendPlainText('Работа завершена')
        time.sleep(120)
        self.driver.close()

    def main(self):
        """ Собираем данные с полей """
        senders = self.load_sender_list()  # загружаем список аккаунтов откуда будем отправлять письма
        receiver = self.load_receiver_list()

        data_list = split_list(receiver, len(senders), senders)  # список со вложенными емайлами
        attachment_files = self.get_file_names()  # читаем файлы вложения
        subject = self.ui.message_subject.text()  # тема сообщений
        email_text = self.ui.messages_text.toPlainText()  # текст сообщений
        default_password_for_email = self.ui.default_password.text()  # стандартный пароль для аккаунтов-отправителей
        attach_send_delay = int(self.ui.attach_delay.text())  # зажержка перед отправление вложений
        captcha = self.ui.captcha_api_key.text()
        self.close_win()
        self.auth_mail(data_list, attachment_files, subject, email_text, default_password_for_email,
                       attach_send_delay, captcha)


app = QtWidgets.QApplication([])
application = MailSender()
application.show()
sys.exit(app.exec_())
