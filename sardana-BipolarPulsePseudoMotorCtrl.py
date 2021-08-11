'''This module contains the definition of a pseudo motor controller
that simultaneously sets the delay, pulse width and amplitude for a
two-channel pulse generator to generate symmetric bipolar pulses.'''

__all__ = ['BipolarPulse']

__docformat__ = 'restructuredtext'

from sardana.pool.controller import PseudoMotorController


class BipolarPulse(PseudoMotorController):
    '''A pseudo motor controller for handling bipolar pulse generator settings.
    It controls pulse width, delay and high/low levels for two separate pulser
    channels to produce a symmetric bipolar pulse like this:

        ---
       |   |
    ---    |    ---
           |   |
            ---
    
    In other words, for both output channels it sets:
    * equal pulse widths (`Width`)
    * equal high levels (`Amplitude / 2`)
    * 0 V low levels
    * first channel delay to `Delay`
    * second channel delay to `Delay + Width`
    
    This assumes that the complement (inverted) output of Channel 2 is used.
    '''

    gender = 'BipolarPulse'
    model = 'generic'
    organization = 'MBI Berlin'

    pseudo_motor_roles = 'Delay', 'Width', 'Amplitude'
    motor_roles = ('ch1_delay', 'ch2_delay', 'ch1_width', 'ch2_width',
                   'ch1_low', 'ch2_low', 'ch1_high', 'ch2_high',)

    def __init__(self, inst, props, *args, **kwargs):
        PseudoMotorController.__init__(self, inst, props, *args, **kwargs)
        self._log.debug('Created BipolarPulse %s', inst)

    def CalcPhysical(self, index, pseudo_pos, curr_physical_pos):
        delay, width, amplitude = pseudo_pos
        if index == 0:  # request ch1_delay
            ret = delay
        elif index == 1:  # request ch2_delay
            ret = delay + width
        elif index in [2, 3]:  # request any width
            ret = width
        elif index in [4, 5]:  # request any low level
            ret = 0
        elif index in [6, 7]:   # request any high level
            ret = amplitude / 2
        
        self._log.debug('BipolarPulse.CalcPhysical(%d, %s) -> %f',
                        index, pseudo_pos, ret)
        return ret

    def CalcPseudo(self, index, physical_pos, curr_pseudo_pos):
        if index == 0:  # request delay
            ret = physical_pos[0]
        elif index == 1:  # request width
            ret = physical_pos[2]
        elif index == 2:  # request amplitude
            ret = 2 * physical_pos[6]
        return ret
