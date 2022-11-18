from abc import ABC, abstractmethod

class BatteryChar(ABC):
    @abstractmethod
    def execute(self) -> str:
        pass

class Context:
    strategy: BatteryChar

    def set_battery_char(self, strategy: BatteryChar=None) -> None:
        # print('strategy-->', strategy)
        if strategy is not None:
            self.strategy = strategy
        else:
            raise Exception("Strategy cannot be empty")
    
    def execute_battery_char(self):
        return self.strategy.execute()

class ClassifyTempBreach:
    def __init__(self, temp: int, lowerlimit: int, upperlimit: int, alert_type: str='TO_CONTROLLER') -> None:
        self.temp = temp
        self.lowerlimit = lowerlimit
        self.upperlimit = upperlimit
        self.alert_type = alert_type

    def infer_breach(self) -> str:
        # print('--->', self.temp, self.lowerlimit)
        if self.temp < self.lowerlimit:
            return 'TOO_LOW'
        elif self.temp > self.upperlimit:
            return 'TOO_HIGH'
        return 'NORMAL'
    
    def send_to_controller(self, breach_type: str):
        header = 0xfeed
        return f'{header}, {breach_type}'
    
    def send_to_email(self, breach_type):
        recepient = "a.bc@c.com"
        # print(breach_type)
        if breach_type == 'TOO_LOW':
            return f'To: {recepient} \nHi, the temperature is too low'
        elif breach_type == 'TOO_HIGH':
            return f'To: {recepient} \nHi, the temperature is too high'
        else:
            return f'To: {recepient} \nHi, the temperature is normal'

    def check_alert(self, breach_type: str):
        # print(self.alert_type, breach_type)
        if self.alert_type == 'TO_CONTROLLER':
            return self.send_to_controller(breach_type)
        elif self.alert_type == 'TO_EMAIL':
            return self.send_to_email(breach_type)

    def clasify_temp_breach(self):
        return self.check_alert(
            self.infer_breach()
        )

class PassiveCooling(BatteryChar):    
    def execute(self) -> int:
        self.lowerlimit = 10
        self.upperlimit = 35
        return self.lowerlimit, self.upperlimit        

class HiActiveCooling(BatteryChar):    
    def execute(self) -> int:
        self.lowerlimit = 0
        self.upperlimit = 45
        return self.lowerlimit, self.upperlimit

class MedActiveCooling(BatteryChar):    
    def execute(self) -> int:
        self.lowerlimit = 0
        self.upperlimit = 40
        return self.lowerlimit, self.upperlimit

# pasive_cooling = Context()
# pasive_cooling.set_battery_char(PassiveCooling())
# lower_limit, upper_limit = pasive_cooling.execute_battery_char()
# breach = ClassifyTempBreach(-5, lower_limit, upper_limit, 'TO_EMAIL')
# print(breach.clasify_temp_breach())