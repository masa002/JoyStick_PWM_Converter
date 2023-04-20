import json
import pygame
import win32api
import numpy as np

class ControllerInput:
    def __init__(self):
        self.pwm_control_active = False
        self.deadzone = 0.1

        pygame.init()
        pygame.joystick.init()
        self.joystick = pygame.joystick.Joystick(0)
        self.joystick.init()

    def start(self):
        self.update()

    def start_pwm_control(self):
        self.pwm_control_active = True
        self.load_key_bindings()

    def stop_pwm_control(self):
        self.pwm_control_active = False

    def get_axis(self, axis):
        return self.joystick.get_axis(axis)

    def pwm_control(self, value, threshold):
        if abs(value) < threshold:
            return 0
        else:
            return np.interp(value, [-1, 1], [-100, 100])  # PWM周期の軸を-100〜100に変更
        
    def key_press(self, key):
        win32api.keybd_event(ord(key), 0, 0, 0)
        
    def pwm_button_click(self, value, axis):
        try:
            if value > 0:
                self.key_press(self.key_bindings[axis]["positive"])
            elif value < 0:
                self.key_press(self.key_bindings[axis]["negative"])
        except:
            # キーバインディングが設定されていない場合は何もしない
            pass


    def load_key_bindings(self):
        try:
            with open("config/key_bindings.json", "r") as f:
                self.key_bindings = json.load(f)
        except:
            self.key_bindings = {}

    def update(self, deadzone=None):
        if deadzone is None:
            deadzone = self.deadzone
        for event in pygame.event.get():
            pass

        if self.pwm_control_active:
            x_axis = self.get_axis(0)
            y_axis = self.get_axis(1)
            z_axis = self.get_axis(2)

            x_pwm = self.pwm_control(x_axis, self.deadzone)
            y_pwm = self.pwm_control(y_axis, self.deadzone)
            z_pwm = self.pwm_control(z_axis, self.deadzone)

            self.pwm_button_click(x_pwm, "X")
            self.pwm_button_click(y_pwm, "Y")
            self.pwm_button_click(z_pwm, "Z")

            print(f"X_PWM: {x_pwm}, Y_PWM: {y_pwm}, Z_PWM: {z_pwm}")