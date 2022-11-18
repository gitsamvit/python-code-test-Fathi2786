import unittest
from typewise_alert import Context, ClassifyTempBreach, PassiveCooling, MedActiveCooling, HiActiveCooling

class TestClassifyTempBreach(unittest.TestCase):
    def setUp(self) -> None:
        self.context = Context()
        self.recepient = "a.bc@c.com"
        self.header = 0xfeed
    
    def _set_cooling_execute(self, cooling_type: str):
        self.context.set_battery_char(cooling_type())
        lower_limit, upper_limit = self.context.execute_battery_char()
        return lower_limit, upper_limit
    
    def test_passive_cooling_email(self):
        lower_limit, upper_limit = self._set_cooling_execute(PassiveCooling)
        breach_high = ClassifyTempBreach(100, lower_limit, upper_limit, 'TO_EMAIL')
        breach_low = ClassifyTempBreach(20, lower_limit, upper_limit, 'TO_EMAIL')
        breach_normal = ClassifyTempBreach(-5, lower_limit, upper_limit, 'TO_EMAIL')

        self.assertEqual(breach_high.clasify_temp_breach(), f'To: {self.recepient} \nHi, the temperature is too high')
        self.assertEqual(breach_low.clasify_temp_breach(), f'To: {self.recepient} \nHi, the temperature is normal')
        self.assertEqual(breach_normal.clasify_temp_breach(), f'To: {self.recepient} \nHi, the temperature is too low')
    
    def test_passive_cooling_controller(self):
        lower_limit, upper_limit = self._set_cooling_execute(PassiveCooling)
        normal = ClassifyTempBreach(30, lower_limit, upper_limit).clasify_temp_breach()
        high = ClassifyTempBreach(150, lower_limit, upper_limit).clasify_temp_breach()
        low = ClassifyTempBreach(5, lower_limit, upper_limit).clasify_temp_breach()

        self.assertEqual(normal, f'{self.header}, NORMAL')
        self.assertEqual(high, f'{self.header}, TOO_HIGH')
        self.assertEqual(low, f'{self.header}, TOO_LOW')

    def test_medactive_cooling_normal_error(self):
        lower_limit, upper_limit = self._set_cooling_execute(MedActiveCooling)
        normal_error = ClassifyTempBreach(100, lower_limit, upper_limit, 'TO_EMAIL')
        self.assertEqual(normal_error.clasify_temp_breach(), f'To: {self.recepient} \nHi, the temperature is too normal'
        )
    
    def test_passive_cooling_high_error(self):
        lower_limit, upper_limit = self._set_cooling_execute(PassiveCooling)
        high_error = ClassifyTempBreach(-5, lower_limit, upper_limit, 'TO_EMAIL')
        self.assertEqual(high_error.clasify_temp_breach(), f'To: {self.recepient} \nHi, the temperature is too high'
        )
    
    def test_medactive_cooling_controller(self):
        lower_limit, upper_limit = self._set_cooling_execute(MedActiveCooling)
        normal = ClassifyTempBreach(40, lower_limit, upper_limit).clasify_temp_breach()
        self.assertEqual(normal, f'{self.header}, NORMAL')
    
    def test_hiactive_cooling_email_error(self):
        lower_limit, upper_limit = self._set_cooling_execute(HiActiveCooling)
        breach_high = ClassifyTempBreach(150, lower_limit, upper_limit, 'TO_EMAIL')
        self.assertEqual(breach_high.clasify_temp_breach(), f'To: {self.recepient} \nHi, the temperature is too low')
    
    def test_empty_context(self):
        _, _ = self.context.set_battery_char()

if __name__ == '__main__':
    unittest.main()
